# 🌍 WikiWorldMap – Interactive Web App Overview

WikiWorldMap is an interactive web app that transforms the way users learn about countries. Instead of reading long paragraphs or searching manually, users can:

- Click on a country directly on a world map.
- Instantly view key stats, cultural information, notable personalities, and trivia.
- Explore global knowledge with a single click in a game-like interface.

The app is powered by real-time data from Wikipedia, Wikidata, and Wikivoyage, all through open APIs.



## 🔗 Live App Link

- **Live Demo URL**: https://zesty-fenglisu-a327c9.netlify.app/
- The application is deployed on **Netlify** as a static site.
- It works on all modern browsers and mobile devices.

---

## 👥 Team Details and Roles

**Team Name**: wikiexplorer_team45

| Team Member         | Contribution Area                                                                 |
|---------------------|------------------------------------------------------------------------------------|
| **Bala Sai Manikanta** | Coordinated the project roadmap, managed GitHub repository, deployment integration |
| **Aravind**             | Connected the application with Wikipedia, Wikidata, and Wikivoyage APIs            |
| **Sanjay Reddy**        | Developed the interactive Leaflet map UI and information display cards             |
| **Likitha**             | Focused on structured info retrieval, formatting of statistical and trivia content |
| **Vyshnavi**            | Led the UI/UX flow, designed intuitive interfaces, conducted user testing          |

---


---

## ❓ Problem Statement

Traditional learning platforms make geography and culture feel dull, repetitive, and static.  
Key issues:

- 📘 **Too much text** – Students often lose interest quickly.
- 🔍 **Hard to explore** – Users must search manually or follow long hyperlinks.
- 🎯 **Lack of engagement** – There’s little interactivity in existing apps or books.

**WikiWorldMap** solves this by introducing a **visual, interactive, and real-time experience** that makes learning geography **fun and engaging**, while still being informative.

---

## 🧩 Feature Table

| Feature Name           | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| 📍 **Interactive World Map**   | Clickable map interface built using Leaflet.js                                 |
| 🌎 **Country Overview**        | Displays name, capital, population, and area                                 |
| 🧠 **"Did You Know?" Trivia**  | Random fun fact that refreshes daily for each country                        |
| 🧳 **Culture & Festivals**     | Shows travel tips, local customs, and festivals from Wikivoyage              |
| 👨‍🎨 **Famous Personalities**  | Lists notable people born in the country via Wikidata                        |
| 🏳️ **National Flag & Stats**  | Shows real-time flag, GDP, population, and surface area from Wikidata        |
| 📊 **Infographics**           | Visual representation of stats like GDP, population via bar charts, etc.     |
| ❓ **Quiz Mode** *(Planned)*   | Users guess the country based on clues, with a scoring system (coming soon)  |

---

## 🔌 API Integration

### ✅ APIs Used:

1. **Wikipedia API**
   - Retrieves: Country descriptions, languages, history
   - Format: JSON with plain text and hyperlinks

2. **Wikivoyage API**
   - Retrieves: Travel and cultural information (festivals, tips)
   - Format: JSON or parsed wikitext

3. **Wikidata API**
   - Retrieves: Flags, population, GDP, official figures
   - Format: Structured SPARQL or JSON

### 🔄 Data Flow Diagram

```
User Clicks a Country on the Map
        ↓
Fetch Requests to Wikipedia, Wikivoyage, Wikidata APIs
        ↓
Data Responses (Raw JSON / Text)
        ↓
Unified Parser Processes and Formats Data
        ↓
UI Cards Update with Cleanly Displayed Content
        ↓
Trivia Box Refreshes with Random "Did You Know?" fact
```

---

## 🏗️ Technical Architecture

| Layer             | Stack / Library Used                                  |
|------------------|--------------------------------------------------------|
| **Frontend**      | HTML5, CSS3, Vanilla JavaScript                       |
| **Map Library**   | Leaflet.js for map rendering and popup handling       |
| **Data Fetching** | Fetch API with `async/await` for non-blocking requests|
| **Visualization** | Leaflet popups, icons, and SVG-based stat bars        |
| **Deployment**    | Netlify (continuous deployment from GitHub)           |
| **Code Management**| GitHub (private repo), future plans to open-source   |

---

## 🧱 Challenges & Solutions

| Challenge                            | Solution Implemented                                                  |
|--------------------------------------|------------------------------------------------------------------------|
| ⌛ API Latency                       | Added loaders/spinners and minimal client-side caching                 |
| 📱 Mobile UI Issues                 | Used media queries and responsive layouts for smaller screen sizes     |
| 🔄 Inconsistent Data Formats        | Built a unified JSON parser that standardizes input from all APIs      |
| 🧭 User Onboarding                  | Plan to include guided tooltips for first-time users                   |
| 🌐 Flag Resolution Variance         | Fetched vector-based flag URLs where possible for clarity              |

---

## 📊 User Testing & Feedback

### 👥 User Testing Details

- **Participants**: 6 individuals (2 students, 2 teachers, 2 travelers)
- **Time Spent**: ~10 minutes of active usage each
- **Method**: Screen interaction + Google Form for feedback

### 📝 Feedback Summary

| Category       | Avg. Rating (out of 5) | What Worked Well                     | Suggestions for Improvement                |
|----------------|------------------------|--------------------------------------|--------------------------------------------|
| Usability      | 4.5                    | Intuitive map clicks, no confusion   | Add "Back to map" or "Home" button         |
| Content Clarity| 4.6                    | Facts were concise & readable        | Add citation or "source" label for numbers |
| UI/UX Design   | 4.4                    | Smooth, clean layout                 | Improve flag resolution for some countries |
| Speed          | 4.3                    | Mostly fast                          | Slight lag noticed on slow networks        |

---

## 📢 Promotion Strategy

### 🎯 Target Audience

- 📚 High school and college students
- 🧑‍🏫 Teachers and educators
- 🧠 Trivia and quiz enthusiasts
- ✈️ Travel bloggers and planners

### 📈 Outreach Strategy

| Platform            | Action Plan                                                     |
|---------------------|------------------------------------------------------------------|
| Dev.to & Reddit     | Share detailed post with screenshots and feature highlights     |
| ProductHunt         | Submit as a demo app under “Education” or “Geography” tools     |
| Showwcase           | Post case study to gather developer interest                    |
| GitHub Discussions  | Gather ideas and feedback once repo is public                   |
| LinkedIn            | Connect with geography teachers and EdTech enthusiasts          |

---

## 🧾 Conclusion with License and Links

**WikiWorldMap** aims to gamify geography and knowledge discovery using interactive maps and structured APIs.  
By uniting spatial UI, rich data, and clean UX, it opens new possibilities for education, travel research, and self-learning.

---

### 🔗 Useful Links

- **Live Demo**: [https://zesty-fenglisu-a327c9.netlify.app/](https://zesty-fenglisu-a327c9.netlify.app/)  
  
- **License**: [MIT License](https://opensource.org/licenses/MIT)