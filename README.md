LIVE APP:: https://zesty-fenglisu-a327c9.netlify.app/



# 🧭 WikiExplorer

WikiExplorer is an interactive map-based web application that allows users to click anywhere on the globe and instantly explore information about that location using real-time data from Wikipedia and other Wikimedia APIs.

🚀 Built for the WikiVerse Hackathon — IIIT Hyderabad (30 June 2025)

---

## 🌍 Project Idea

Despite the rich and freely available content on Wikimedia platforms, it is often accessed in static and text-heavy formats. WikiExplorer reimagines this by transforming Wikipedia into a dynamic, geographic knowledge experience. By combining map interaction with Wikipedia summaries, it helps users explore the world visually — one click at a time.

----

## 🎯 Features

- 🗺️ Interactive world map (powered by Leaflet.js)
- 🔍 Click anywhere to identify location name via reverse geocoding
- 📖 Fetch real-time Wikipedia summaries for cities/countries
- 🔗 View full article with a link to Wikipedia
- 🌐 No login or database — lightweight and purely client-side
- 🌐 Multi-language support (Wikipedia in different languages)

----

## 🧰 Tech Stack

- HTML, CSS, JavaScript
- Leaflet.js (open-source map rendering)
- OpenStreetMap (tiles & geocoding)
- Wikipedia REST API (summary endpoint)
- Nominatim API (reverse geocoding)

---

## 🧠 How It Works

1. User clicks on any point on the map.
2. App uses Nominatim (OpenStreetMap) to convert coordinates into a place name.
3. Wikipedia’s REST API is queried using that name.
4. Summary + article link is shown in a popup.

---

## 📦 Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/your-username/wiki-explorer.git
cd wiki-explorer
Open index.html in your browser:

bash
Copy
Edit
open index.html  # or double-click the file
No backend or npm required. Works offline once loaded.

📚 Wikimedia APIs Used
Wikipedia REST Summary API
https://en.wikipedia.org/api/rest_v1/page/summary/{title}

OpenStreetMap Nominatim (Reverse Geocoding)
https://nominatim.openstreetmap.org/reverse

✨ Future Enhancements
🖼️ Fetch images from Wikimedia Commons

📊 Show facts like population from Wikidata

🧳 Add travel tips from Wikivoyage


📱 PWA support for mobile offline use

👥 Team
Bala Sai Manikanta
Aravind
Sanjay reddy
Likitha
Vyshnavi
Soham