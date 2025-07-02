import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
import re
from typing import Tuple, Dict, List, Optional

# Page setup
st.set_page_config(page_title="🌍 Country Wikipedia Explorer", page_icon="🌍", layout="wide")

# Language options
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Hindi": "hi",
    "Arabic": "ar",
    "Chinese": "zh",
    "Russian": "ru",
    "Japanese": "ja",
}

# API wrapper class
class WikiAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "WikiExplorerApp"})

    def get_summary(self, country: str, lang: str = "en") -> Dict:
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|pageimages|info",
            "titles": country,
            "exintro": True,
            "explaintext": True,
            "inprop": "url",
            "piprop": "original",
        }
        try:
            res = self.session.get(url, params=params, timeout=10).json()
            pages = res.get("query", {}).get("pages", {})
            page = next(iter(pages.values()))
            return {
                "title": page.get("title", ""),
                "extract": page.get("extract", ""),
                "image": page.get("original", {}).get("source", ""),
                "url": page.get("fullurl", ""),
            }
        except Exception as e:
            st.error(f"Wikipedia error: {e}")
            return {}

    def get_wikidata(self, country: str) -> Dict:
        base_url = "https://www.wikidata.org/w/api.php"
        try:
            # Search item
            res = self.session.get(base_url, params={
                "action": "wbsearchentities", "format": "json",
                "search": country, "language": "en", "limit": 1
            }).json()
            if not res["search"]:
                return {}
            qid = res["search"][0]["id"]

            # Get claims
            res = self.session.get(base_url, params={
                "action": "wbgetentities", "format": "json", "ids": qid
            }).json()
            claims = res["entities"][qid]["claims"]

            info = {}
            if "P1082" in claims:  # Population
                amount = claims["P1082"][0]["mainsnak"]["datavalue"]["value"]["amount"]
                info["population"] = f"{int(float(amount)):,}"
            if "P36" in claims:  # Capital
                capital_qid = claims["P36"][0]["mainsnak"]["datavalue"]["value"]["id"]
                cap_res = self.session.get(base_url, params={
                    "action": "wbgetentities", "format": "json", "ids": capital_qid
                }).json()
                info["capital"] = cap_res["entities"][capital_qid]["labels"]["en"]["value"]
            return info
        except Exception as e:
            st.error(f"Wikidata error: {e}")
            return {}

# Location handling
class LocationFinder:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="WikiExplorer")

    def get_coords(self, country: str) -> Optional[Tuple[float, float]]:
        try:
            loc = self.geolocator.geocode(country, timeout=10)
            return (loc.latitude, loc.longitude) if loc else None
        except Exception as e:
            st.error(f"Geolocation error: {e}")
            return None

    def get_places(self, country: str, place_type: str) -> List[Dict]:
        try:
            results = self.geolocator.geocode(f"{place_type} in {country}", exactly_one=False, limit=5, timeout=10)
            return [
                {
                    "name": r.address.split(",")[0],
                    "address": r.address,
                    "lat": r.latitude,
                    "lon": r.longitude,
                } for r in results
            ] if results else []
        except Exception as e:
            st.error(f"Nominatim search error: {e}")
            return []

# Mapping function
def create_map(center: Tuple[float, float], places: List[Dict], color: str = "blue"):
    m = folium.Map(location=center, zoom_start=6)
    folium.Marker(center, tooltip="Country Center", icon=folium.Icon(color="red")).add_to(m)
    for p in places:
        folium.Marker(
            [p["lat"], p["lon"]],
            popup=f"<b>{p['name']}</b><br>{p['address']}",
            icon=folium.Icon(color=color),
        ).add_to(m)
    return m

# Main UI
def main():
    st.title("🌍 Country Wikipedia Explorer")
    st.sidebar.header("Search Configuration")
    
    lang = st.sidebar.selectbox("Language", list(LANGUAGE_CODES.keys()), index=0)
    country = st.sidebar.text_input("Enter Country Name", "France")
    place_type = st.sidebar.selectbox("Places of Interest", ["restaurants", "temples", "tourist attractions", "hotels", "transportation"])
    
    if st.sidebar.button("Explore"):
        wiki = WikiAPI()
        loc = LocationFinder()

        with st.spinner("Fetching data..."):
            summary = wiki.get_summary(country, LANGUAGE_CODES[lang])
            facts = wiki.get_wikidata(country)
            coords = loc.get_coords(country)
            places = loc.get_places(country, place_type)

        if summary:
            st.header(f"📖 {summary['title']}")
            if summary.get("image"):
                st.image(summary["image"], use_column_width=True)
            st.write(summary["extract"])
            if summary.get("url"):
                st.markdown(f"[Read more on Wikipedia]({summary['url']})")

        if facts:
            st.subheader("📊 Quick Facts")
            if "capital" in facts:
                st.markdown(f"**Capital**: {facts['capital']}")
            if "population" in facts:
                st.markdown(f"**Population**: {facts['population']}")

        if coords:
            st.subheader("🗺️ Places of Interest")
            m = create_map(coords, places, color="green")
            folium_static(m)

if __name__ == "__main__":
    main()
