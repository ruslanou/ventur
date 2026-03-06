# ✈️ Ventur — City Exploration Passport App

> Explore Montgomery. Collect Stamps. Level Up. Win Rewards.

Ventur is a gamified city exploration passport app for **Montgomery, Alabama**. Users discover local restaurants, bars, and attractions by collecting digital stamps — powered by AI recommendations and real-time city data.

---

## 🎯 Features

- 📖 **Digital Passport** — Collect stamps at local venues by scanning QR codes
- 🤖 **AI City Guide** — Gemini-powered chat recommends the best places to visit
- 🏆 **Gamified Levels** — Explorer → Adventurer → Pathfinder → Legend
- 🗺️ **Real City Data** — Powered by Google Places API, Bright Data MCP, and Montgomery Open Data
- 🎁 **Rewards** — Earn points and unlock exclusive offers from local businesses

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI (Python 3.11) |
| AI Model | Google Gemini 2.5 Flash Lite |
| Vector Database | ChromaDB |
| AI Orchestration | LangChain |
| Live Web Data | Bright Data MCP |
| Deployment | Google Cloud Run + Vercel |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Node.js 18+

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ventur-backend.git
cd ventur-backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env

# Run the server
uvicorn main:app --reload
```

### Environment Variables

Create a `.env` file with:
```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_PLACES_API_KEY=your_google_places_key
BRIGHT_DATA_TOKEN=your_bright_data_token
```

### Load Montgomery Data into ChromaDB

```bash
# Fetch real data from all sources
python fetch_data.py

# Or load hardcoded places (fallback)
python load_data.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/test-gemini` | Test Gemini connection |
| POST | `/chat` | AI city guide chat |
| GET | `/docs` | Swagger UI |

### Example Chat Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the best restaurants in Montgomery?"}'
```

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

Ventur features 20+ real Montgomery venues across categories:
- 🍽️ Restaurants (Central Restaurant, Dreamland BBQ, Vintage Year...)
- 🍸 Bars (Cahaba Brewing Co., Sky Bar Rooftop, Irish Bred Pub...)
- 🏛️ Attractions (Rosa Parks Museum, Legacy Museum, State Capitol...)
- 🏨 Hotels (Renaissance Montgomery, The Lattice...)

---

## 🏆 Built For

This project was built for a hackathon — March 2026.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
