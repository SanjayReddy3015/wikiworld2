# This is the entry point for Hugging Face Spaces
# The main application code should be saved as the main Python file

import streamlit as st
import requests
import json
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
import time
from typing import Dict, List, Optional, Tuple
import re

# Page configuration
st.set_page_config(
    page_title="🌍 Country Wikipedia Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language mappings for Wikipedia APIs
LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
    "Hindi": "hi",
    "Dutch": "nl",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Finnish": "fi",
    "Korean": "ko",
    "Thai": "th",
    "Vietnamese": "vi",
    "Turkish": "tr"
}

class WikimediaAPI:
    """Handler for various Wikimedia API endpoints"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CountryExplorer/1.0 (https://huggingface.co/spaces/)'
        })
        
    def get_wikipedia_summary(self, country: str, lang: str = "en") -> Dict:
        """Get Wikipedia summary for a country"""
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'titles': country,
            'prop': 'extracts|pageimages|info',
            'exintro': True,
            'explaintext': True,
            'exsectionformat': 'plain',
            'piprop': 'original',
            'inprop': 'url'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            if pages:
                page_id = list(pages.keys())[0]
                if page_id != '-1':
                    page = pages[page_id]
                    return {
                        'title': page.get('title', ''),
                        'extract': page.get('extract', ''),
                        'image': page.get('original', {}).get('source', ''),
                        'url': page.get('fullurl', '')
                    }
        except Exception as e:
            st.error(f"Error fetching Wikipedia data: {str(e)}")
        
        return {}
    
    def get_wikidata_info(self, country: str) -> Dict:
        """Get structured data from Wikidata"""
        url = "https://www.wikidata.org/w/api.php"
        
        # First, search for the entity
        search_params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'search': country,
            'language': 'en',
            'type': 'item',
            'limit': 1
        }
        
        try:
            response = self.session.get(url, params=search_params, timeout=10)
            search_data = response.json()
            
            if search_data.get('search'):
                entity_id = search_data['search'][0]['id']
                
                # Get entity data
                entity_params = {
                    'action': 'wbgetentities',
                    'format': 'json',
                    'ids': entity_id,
                    'languages': 'en'
                }
                
                entity_response = self.session.get(url, params=entity_params, timeout=10)
                entity_data = entity_response.json()
                
                if 'entities' in entity_data and entity_id in entity_data['entities']:
                    entity = entity_data['entities'][entity_id]
                    claims = entity.get('claims', {})
                    
                    # Extract useful information
                    info = {}
                    
                    # Population (P1082)
                    if 'P1082' in claims:
                        pop_claim = claims['P1082'][0]
                        if 'mainsnak' in pop_claim and 'datavalue' in pop_claim['mainsnak']:
                            info['population'] = pop_claim['mainsnak']['datavalue']['value']['amount']
                    
                    # Capital (P36)
                    if 'P36' in claims:
                        capital_claim = claims['P36'][0]
                        if 'mainsnak' in capital_claim and 'datavalue' in capital_claim['mainsnak']:
                            capital_id = capital_claim['mainsnak']['datavalue']['value']['id']
                            # Get capital name
                            capital_params = {
                                'action': 'wbgetentities',
                                'format': 'json',
                                'ids': capital_id,
                                'languages': 'en'
                            }
                            capital_response = self.session.get(url, params=capital_params, timeout=10)
                            capital_data = capital_response.json()
                            if 'entities' in capital_data and capital_id in capital_data['entities']:
                                capital_entity = capital_data['entities'][capital_id]
                                if 'labels' in capital_entity and 'en' in capital_entity['labels']:
                                    info['capital'] = capital_entity['labels']['en']['value']
                    
                    return info
                    
        except Exception as e:
            st.error(f"Error fetching Wikidata: {str(e)}")
        
        return {}
    
    def get_wikivoyage_info(self, country: str, lang: str = "en") -> Dict:
        """Get travel information from Wikivoyage"""
        url = f"https://{lang}.wikivoyage.org/w/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'titles': country,
            'prop': 'extracts|info',
            'exintro': True,
            'explaintext': True,
            'inprop': 'url'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            if pages:
                page_id = list(pages.keys())[0]
                if page_id != '-1':
                    page = pages[page_id]
                    return {
                        'title': page.get('title', ''),
                        'extract': page.get('extract', ''),
                        'url': page.get('fullurl', '')
                    }
        except Exception as e:
            st.error(f"Error fetching Wikivoyage data: {str(e)}")
        
        return {}

class LocationFinder:
    """Find places of interest using Nominatim"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="country_explorer")
    
    def get_country_coordinates(self, country: str) -> Optional[Tuple[float, float]]:
        """Get country center coordinates"""
        try:
            location = self.geolocator.geocode(country, timeout=10)
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            st.error(f"Error getting coordinates: {str(e)}")
        return None
    
    def find_places_of_interest(self, country: str, place_type: str) -> List[Dict]:
        """Find specific types of places in a country"""
        places = []
        
        # Query mappings for different place types
        query_map = {
            'restaurants': f'restaurant in {country}',
            'temples': f'temple in {country}',
            'tourist_attractions': f'tourist attraction in {country}',
            'transportation': f'airport OR "train station" in {country}',
            'hotels': f'hotel in {country}'
        }
        
        query = query_map.get(place_type, f'{place_type} in {country}')
        
        try:
            # Use Nominatim search
            results = self.geolocator.geocode(query, exactly_one=False, limit=10, timeout=15)
            
            if results:
                for result in results[:5]:  # Limit to 5 results
                    places.append({
                        'name': result.address.split(',')[0],
                        'address': result.address,
                        'lat': result.latitude,
                        'lon': result.longitude
                    })
        except Exception as e:
            st.error(f"Error finding places: {str(e)}")
        
        return places

def create_map(center_coords: Tuple[float, float], places: List[Dict], place_type: str):
    """Create a folium map with markers"""
    m = folium.Map(location=center_coords, zoom_start=6)
    
    # Add center marker
    folium.Marker(
        center_coords,
        popup="Country Center",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(m)
    
    # Color mapping for different place types
    color_map = {
        'restaurants': 'orange',
        'temples': 'purple',
        'tourist_attractions': 'green',
        'transportation': 'blue',
        'hotels': 'pink'
    }
    
    color = color_map.get(place_type, 'gray')
    
    # Add place markers
    for place in places:
        folium.Marker(
            [place['lat'], place['lon']],
            popup=f"<b>{place['name']}</b><br>{place['address']}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    return m

def main():
    st.title("🌍 Country Wikipedia Explorer")
    st.markdown("Explore countries through Wikipedia and discover places of interest!")
    
    # Initialize APIs
    wiki_api = WikimediaAPI()
    location_finder = LocationFinder()
    
    # Sidebar configuration
    st.sidebar.header("🔧 Configuration")
    
    # Language selection
    selected_language = st.sidebar.selectbox(
        "Select Language",
        options=list(LANGUAGE_CODES.keys()),
        index=0
    )
    lang_code = LANGUAGE_CODES[selected_language]
    
    # Country input
    country = st.sidebar.text_input(
        "Enter Country Name",
        value="France",
        help="Enter the name of the country you want to explore"
    )
    
    # Place type selection
    place_types = {
        "🍽️ Restaurants": "restaurants",
        "🏛️ Temples": "temples",
        "🎭 Tourist Attractions": "tourist_attractions",
        "🚇 Transportation": "transportation",
        "🏨 Hotels": "hotels"
    }
    
    selected_place_type = st.sidebar.selectbox(
        "Places of Interest",
        options=list(place_types.keys())
    )
    place_type = place_types[selected_place_type]
    
    if st.sidebar.button("🔍 Explore Country", type="primary"):
        if country:
            # Create columns for layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.header(f"📖 {country} - Wikipedia ({selected_language})")
                
                # Get Wikipedia summary
                with st.spinner("Fetching Wikipedia information..."):
                    wiki_data = wiki_api.get_wikipedia_summary(country, lang_code)
                
                if wiki_data:
                    if wiki_data.get('image'):
                        st.image(wiki_data['image'], caption=wiki_data['title'], use_column_width=True)
                    
                    st.subheader(wiki_data.get('title', country))
                    
                    # Display extract
                    extract = wiki_data.get('extract', '')
                    if extract:
                        # Truncate if too long
                        if len(extract) > 1500:
                            extract = extract[:1500] + "..."
                        st.write(extract)
                    
                    if wiki_data.get('url'):
                        st.markdown(f"[Read full article on Wikipedia]({wiki_data['url']})")
                else:
                    st.warning(f"No Wikipedia article found for '{country}' in {selected_language}")
            
            with col2:
                st.header("📊 Quick Facts")
                
                # Get Wikidata information
                with st.spinner("Fetching country data..."):
                    wikidata_info = wiki_api.get_wikidata_info(country)
                
                if wikidata_info:
                    if 'capital' in wikidata_info:
                        st.metric("🏛️ Capital", wikidata_info['capital'])
                    
                    if 'population' in wikidata_info:
                        pop = wikidata_info['population'].replace('+', '')
                        try:
                            pop_num = int(float(pop))
                            st.metric("👥 Population", f"{pop_num:,}")
                        except:
                            st.metric("👥 Population", pop)
                
                # Wikivoyage travel info
                st.subheader("✈️ Travel Information")
                with st.spinner("Fetching travel information..."):
                    wikivoyage_data = wiki_api.get_wikivoyage_info(country, lang_code)
                
                if wikivoyage_data and wikivoyage_data.get('extract'):
                    travel_info = wikivoyage_data['extract']
                    if len(travel_info) > 500:
                        travel_info = travel_info[:500] + "..."
                    st.write(travel_info)
                    
                    if wikivoyage_data.get('url'):
                        st.markdown(f"[More travel info]({wikivoyage_data['url']})")
            
            # Map section
            st.header(f"🗺️ {selected_place_type} in {country}")
            
            # Get country coordinates
            with st.spinner("Getting location data..."):
                coords = location_finder.get_country_coordinates(country)
            
            if coords:
                # Find places of interest
                with st.spinner(f"Finding {selected_place_type.lower()}..."):
                    places = location_finder.find_places_of_interest(country, place_type)
                
                if places:
                    # Create and display map
                    map_obj = create_map(coords, places, place_type)
                    folium_static(map_obj, width=1200, height=500)
                    
                    # Display places in a table
                    st.subheader(f"📍 Found {len(places)} {selected_place_type}")
                    
                    places_df = pd.DataFrame(places)
                    st.dataframe(
                        places_df[['name', 'address']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning(f"No {selected_place_type.lower()} found for {country}")
                    
                    # Still show country map
                    simple_map = folium.Map(location=coords, zoom_start=6)
                    folium.Marker(
                        coords,
                        popup=f"{country}",
                        icon=folium.Icon(color='red', icon='star')
                    ).add_to(simple_map)
                    folium_static(simple_map, width=1200, height=500)
            else:
                st.error(f"Could not find location data for {country}")
        else:
            st.warning("Please enter a country name")
    
    # Footer with information about APIs used
    st.markdown("---")
    st.markdown("""
    **Data Sources:**
    - 📖 Wikipedia API for country information
    - 🗂️ Wikidata API for structured data
    - ✈️ Wikivoyage API for travel information
    - 📍 Nominatim (OpenStreetMap) for location data
    
    **Supported Languages:** English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Arabic, Hindi, and more!
    """)

if __name__ == "__main__":
    main()
