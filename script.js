/* --------------------------- script.js --------------------------- */
// Map centred so the whole world is in view
const map = L.map("map").setView([20, 0], 2);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors",
}).addTo(map);

/* ---------- Language list (16 Indian langs grouped) ---------- */
const languages = {
  en: "English",
  hi: "हिन्दी (Hindi)",
  bn: "বাংলা (Bengali)",
  te: "తెలుగు (Telugu)",
  mr: "मराठी (Marathi)",
  ta: "தமிழ் (Tamil)",
  gu: "ગુજરાતી (Gujarati)",
  kn: "ಕನ್ನಡ (Kannada)",
  ml: "മലയാളം (Malayalam)",
  or: "ଓଡ଼ିଆ (Odia)",
  pa: "ਪੰਜਾਬੀ (Punjabi)",
  as: "অসমীয়া (Assamese)",
  ur: "اردو (Urdu)",
  sa: "संस्कृत (Sanskrit)",
  ne: "नेपाली (Nepali)",
  si: "සිංහල (Sinhala)",
  my: "မြန်မာ (Myanmar)",
  es: "Español",
  fr: "Français",
  de: "Deutsch",
  it: "Italiano",
  pt: "Português",
  ru: "Русский",
  ja: "日本語",
  zh: "中文",
  ar: "العربية",
  ko: "한국어",
  nl: "Nederlands",
  sv: "Svenska",
  tr: "Türkçe",
};

function initializeLanguageSelector() {
  const sel = document.getElementById("language-selector");
  if (!sel) return;

  const indian = [
    "hi","bn","te","mr","ta","gu","kn",
    "ml","or","pa","as","ur","sa","ne","si","my"
  ];

  const makeGroup = (label) => {
    const g = document.createElement("optgroup");
    g.label = label;
    return g;
  };

  const indianGroup = makeGroup("Indian & South-Asian Languages");
  indian.forEach(c => {
    const o = document.createElement("option");
    o.value = c; o.textContent = languages[c];
    indianGroup.appendChild(o);
  });
  sel.appendChild(indianGroup);

  const otherGroup = makeGroup("Other Languages");
  Object.keys(languages)
    .filter(c => !indian.includes(c))
    .forEach(c => {
      const o = document.createElement("option");
      o.value = c; o.textContent = languages[c];
      otherGroup.appendChild(o);
    });
  sel.appendChild(otherGroup);

  sel.value = "en";           // default
}

/* ---------- Single-pin state ---------- */
let currentMarker = null;
let lastPlace = null;

/* Optional custom pin (uses default Leaflet icon here) */
const pinIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.8.0/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.8.0/dist/images/marker-shadow.png",
  iconSize:   [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
  className: "pulse"
});

/* ---------- Map click handler ---------- */
map.on("click", async ({ latlng }) => {
  const { lat, lng } = latlng;

  // Keep only one pin
  if (currentMarker) {
    map.removeLayer(currentMarker);
    currentMarker = null;
  }
  currentMarker = L.marker([lat, lng], { icon: pinIcon }).addTo(map);

  document.getElementById("info").textContent = "🔄 Fetching location info…";

  const place = (await getPlaceName(lat, lng)) || "Unknown location";
  lastPlace = place;

  await getWikiSummary(place, getSelectedLanguage());
  currentMarker.bindPopup(place).openPopup();
});

/* ---------- City-level reverse geocode + fallback ---------- */
async function getPlaceName(lat, lon) {
  const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&zoom=10`;
  try {
    const r = await fetch(url, { headers: { "User-Agent": "WikiLoc/1.0" } });
    if (!r.ok) throw new Error(r.statusText);
    const d = await r.json();
    if (d.address)
      return (
        d.address.city ||
        d.address.town ||
        d.address.village ||
        d.address.state ||
        d.address.country
      );
  } catch (e) {
    console.error("Nominatim error", e);
  }
  return fallbackCity(lat, lon);
}

async function fallbackCity(lat, lon) {
  const coord = `${lat.toFixed(3)}${lon < 0 ? lon.toFixed(3) : "+" + lon.toFixed(3)}`;
  const url =
    `https://geodb-free-service.wirefreethought.com/v1/geo/locations/${coord}/nearbyCities?limit=1&radius=50`;
  try {
    const r = await fetch(url);
    const j = await r.json();
    if (j.data && j.data.length) return j.data[0].city;
  } catch (e) {
    console.error("GeoDB error", e);
  }
  return null;
}

/* ---------- Wikipedia summary with English fallback ---------- */
async function getWikiSummary(place, lang = "en") {
  const url = `https://${lang}.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(place)}`;
  try {
    const r = await fetch(url);
    if (!r.ok) {
      if (lang !== "en") {
        document.getElementById("info").textContent =
          `⚠️ No article in ${languages[lang]}. Trying English…`;
        return getWikiSummary(place, "en");
      }
      throw new Error(r.statusText);
    }
    const d = await r.json();
    if (d.extract) {
      document.getElementById("info").innerHTML = `
        <div class="language-indicator">${languages[lang] || lang.toUpperCase()}</div>
        <h3>${d.title}</h3>
        <p>${d.extract}</p>
        <a class="wiki-link" href="${d.content_urls.desktop.page}" target="_blank" rel="noopener">
          🔗 Read more on Wikipedia
        </a>`;
    } else {
      document.getElementById("info").textContent =
        `❌ No article for “${place}” in ${languages[lang]}`;
    }
  } catch (e) {
    console.error("Wikipedia API error", e);
    if (lang !== "en") {
      document.getElementById("info").textContent =
        `⚠️ Error in ${languages[lang]}. Trying English…`;
      return getWikiSummary(place, "en");
    }
    document.getElementById("info").textContent = "⚠️ Error fetching Wikipedia data.";
  }
}

/* ---------- Helpers ---------- */
function getSelectedLanguage() {
  const s = document.getElementById("language-selector");
  return s ? s.value : "en";
}

/* ---------- Language-change listener ---------- */
function wireLanguageSwitch() {
  const s = document.getElementById("language-selector");
  s.addEventListener("change", () => {
    const lang = s.value;
    if (lastPlace) getWikiSummary(lastPlace, lang);
    if (currentMarker) currentMarker.bindPopup(lastPlace).openPopup();
  });
}

/* ---------- Boot ---------- */
document.addEventListener("DOMContentLoaded", () => {
  initializeLanguageSelector();
  wireLanguageSwitch();
});
