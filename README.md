# ✈️ Ventur — City Exploration Passport App

> Explore Montgomery. Collect Stamps. Level Up. Win Rewards.

Ventur is a gamified city exploration passport app for **Montgomery, Alabama**. Users discover local restaurants, bars, and attractions by collecting digital stamps — powered by AI recommendations and real city data.

**Live App:** [ventur-app.vercel.app](https://ventur-app.vercel.app)

---

## 🎯 Features

- 📖 **Digital Passport** — Collect stamps at local venues by scanning QR codes
- 🤖 **AI City Guide** — Gemini-powered chat recommends the best places to visit
- 🏆 **Gamified Levels** — Explorer → Adventurer → Pathfinder → Legend
- 🗺️ **Real City Data** — Powered by Google Places API with real photos
- 🎁 **Rewards** — Earn points and unlock exclusive offers from local businesses
- 📱 **PWA** — Installable as a native app on any phone

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite (PWA) |
| Backend | FastAPI (Python 3.11) |
| AI Model | Google Gemini 2.5 Flash Lite |
| Vector Database | ChromaDB (RAG) |
| Live Web Data | Bright Data MCP |
| Backend Deploy | Google Cloud Run |
| Frontend Deploy | Vercel |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Node.js 18+

### Backend

```bash
git clone https://github.com/ruslanou/ventur.git
cd ventur/backend

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Add API keys
cp .env.example .env

# Load Montgomery data into ChromaDB
python load_data.py

# Start server
uvicorn main:app --reload
```

### Frontend

```bash
cd ventur/frontend
npm install
npm run dev
```

### Environment Variables

```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_PLACES_API_KEY=your_google_places_key
BRIGHT_DATA_TOKEN=your_bright_data_token
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/chat` | AI city guide chat (RAG-powered) |
| GET | `/places` | All places (`?category=` filter) |
| GET | `/places/{place_id}` | Single place details |
| POST | `/stamp` | Collect a stamp |
| GET | `/profile/{user_id}` | User level, points, and stamps |
| GET | `/place-photo/{place_id}` | Google Places photo proxy |
| GET | `/docs` | Swagger UI |

---

## 🎮 Level System

| Level | Points Required |
|---|---|
| 🌱 Explorer | 0 pts |
| ⚡ Adventurer | 500 pts |
| 🔥 Pathfinder | 1,000 pts |
| 👑 Legend | 2,000 pts |

---

## 📍 Montgomery Places

**24 curated venues** available for stamp collection in the passport:
- 🍽️ Restaurants — Central, Dreamland BBQ, Vintage Year, True Kitchen, Brick & Tin, Niffer's Place...
- 🍸 Bars — Cahaba Brewing, Sky Bar Rooftop, Irish Bred Pub, The Vine Wine Bar...
- 🏛️ Attractions — Rosa Parks Museum, Legacy Museum, State Capitol, MLK Church, Fitzgerald Museum, Old Alabama Town...
- 🏨 Hotels — Renaissance Montgomery, The Lattice...

**290+ venues** indexed in ChromaDB — used by the AI Guide to answer questions about the wider Montgomery area.

---

## 📱 Install as App

1. Open the live URL in Chrome on your phone
2. Tap **Menu → Add to Home screen**
3. Opens fullscreen like a native app

---

## 🏆 Built For

Hackathon — March 2026

---

## 📄 License

MIT — see [LICENSE](LICENSE)
