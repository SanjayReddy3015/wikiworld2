---
title: Country Wikipedia Explorer
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.35.0"
app_file: app.py
pinned: false
---

# 🌍 Country Wikipedia Explorer

An interactive Streamlit app that helps users explore countries through Wikipedia summaries, Wikidata facts, and Folium-based maps with places of interest.

## ✨ Features

- 🌐 Multilingual Wikipedia summaries
- 🏛️ Capital and population from Wikidata
- 🗺️ Interactive map with:
  - 🍽️ Restaurants
  - 🏛️ Temples
  - 🎭 Tourist Attractions
  - 🚇 Transportation
  - 🏨 Hotels

## ⚙️ Tech Stack

- Streamlit
- Folium (Leaflet.js)
- Geopy + Nominatim
- Wikipedia / Wikidata / Wikivoyage APIs

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
