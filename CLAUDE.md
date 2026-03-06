# Ventur — Claude Code Context File
> Read this file first before doing anything. This is the full project context.

---

## 🎯 Project Overview

**Ventur** is a gamified city exploration passport app for **Montgomery, Alabama**.
Users collect digital stamps by visiting local restaurants, bars, attractions, and hotels by scanning QR codes.
They earn points and level up. Businesses pay to be featured and offer rewards.

**Hackathon Deadline: March 9, 2026**
**Today: Day 2 — March 5, 2026**
**Team: 1 Software Engineer + 1 PM**

---

## 🗂️ Project Structure

```
ventur-backend/
├── main.py                  ✅ FastAPI app — DONE
├── requirements.txt         ✅ Dependencies — DONE
├── montgomery_places.py     ✅ 20 hardcoded Montgomery places — DONE
├── fetch_data.py            🔄 Real data fetcher — IN PROGRESS (Day 2)
├── load_data.py             🔄 ChromaDB loader (fallback) — DONE
├── .env                     ✅ API keys — DONE
├── chroma_db/               📅 Created after fetch_data.py runs
└── venv/                    ✅ Python 3.11 virtual environment

ventur-frontend/
└── ventur-prototype.jsx     ✅ React UI prototype — DONE (dark navy/gold theme)
```

---

## 🔑 Environment Variables (.env)

```
GEMINI_API_KEY=<already set>
GOOGLE_PLACES_API_KEY=<already set>
BRIGHT_DATA_TOKEN=<already set>
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (ventur-prototype.jsx) |
| Backend | FastAPI (Python 3.11) |
| AI Model | Google Gemini 2.5 Flash Lite |
| AI Orchestration | LangChain (Day 3) |
| Vector Database | ChromaDB |
| Live Web Data | Bright Data MCP |
| Backend Deploy | Google Cloud Run (Day 5) |
| Frontend Deploy | Vercel (Day 5) |

---

## ✅ What's Already Done (Day 1)

- [x] Python 3.11 installed via Homebrew
- [x] Virtual environment created (`venv/`)
- [x] All dependencies installed
- [x] FastAPI server running on `localhost:8000`
- [x] Gemini AI connected and responding (model: `gemini-2.5-flash-lite`)
- [x] `/chat` and `/test-gemini` endpoints working
- [x] Ventur AI system prompt updated
- [x] `montgomery_places.py` — 20 real Montgomery places dataset created
- [x] React UI prototype done (dark navy/gold passport theme)

---

## 🔄 Day 2 Goal — IN PROGRESS

**Goal: Fetch real Montgomery data from 3 sources → Load into ChromaDB → Update AI to use it**

### Step 1: Run fetch_data.py ← START HERE
```bash
cd ventur-backend
source venv/bin/activate
python fetch_data.py
```

This fetches from:
1. **Google Places API** — real restaurants, bars, attractions near Montgomery
2. **Bright Data MCP** — live web search results
3. **Montgomery Open Data Portal** — official city POI data

Expected output:
- `chroma_db/` folder created
- `fetched_places.json` saved
- ChromaDB populated with real places

### Step 2: Update main.py to use ChromaDB
After fetch_data.py works, update the `/chat` endpoint in `main.py` to:
1. Query ChromaDB for relevant places based on user message
2. Add those places as context to Gemini prompt
3. Return AI response grounded in real Montgomery data

### Step 3: Test the AI
Ask: "What are the best restaurants in Montgomery?"
Should return real places with real addresses from ChromaDB.

---

## 📅 Remaining Days Plan

### Day 3 — March 6
- Build LangChain RAG pipeline
- Connect Bright Data MCP for live real-time data
- Test AI with 10 real user questions
- PM: Complete pitch deck

### Day 4 — March 7
- Connect React frontend to FastAPI backend
- Replace hardcoded chat in React with real API calls
- Update `sendMessage()` to call `POST localhost:8000/chat`
- UI polish and bug fixes

### Day 5 — March 8
- Deploy FastAPI to Google Cloud Run
- Deploy React to Vercel
- Set $20 billing alert on Google Cloud
- Full end-to-end testing

### Day 6 — March 9 (Submission)
- Final bug fixes (1 hour max)
- Record 2-3 min demo video
- Write project description
- Submit!

---

## 🚀 Key Commands

```bash
# Activate environment
cd ventur-backend
source venv/bin/activate

# Start server
uvicorn main:app --reload

# Run data fetcher
python fetch_data.py

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/test-gemini
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "best restaurants in Montgomery"}'
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/test-gemini` | Test Gemini connection |
| POST | `/chat` | Main AI chat — body: `{"message": "string"}` |
| GET | `/docs` | Swagger UI |

---

## 🏙️ Montgomery Places Data

`montgomery_places.py` contains 20 real places:
- 6 Restaurants (Central, Dreamland BBQ, Vintage Year, Alley Bar, Vintage Café, True Kitchen)
- 3 Bars (Cahaba Brewing, Sky Bar Rooftop, Irish Bred Pub)
- 8 Attractions (Rosa Parks Museum, Legacy Museum, Capitol, MLK Church, Zoo, Shakespeare Festival, etc.)
- 2 Hotels (Renaissance, The Lattice)

Each place has: id, name, category, subcategory, address, neighborhood, description, hours, price_range, points, tags

---

## 🎮 App Features (React Prototype)

- **Onboarding**: 3 screens (Welcome, Collect Stamps, Level Up)
- **Passport Tab**: Grid of place cards with stamped/unstamped states
- **Explore Tab**: Browse by category (Restaurant, Bar, Attraction)
- **Guide Tab**: AI chat powered by Gemini
- **Profile Tab**: Level, points, stamps, progression
- **Place Modal**: Details + QR scan simulation

### Level System
| Level | Points |
|---|---|
| Explorer 🌱 | 0 pts |
| Adventurer ⚡ | 500 pts |
| Pathfinder 🔥 | 1,000 pts |
| Legend 👑 | 2,000 pts |

---

## ⚠️ Known Issues & Fixes

| Problem | Fix |
|---|---|
| Gemini 404 error | Use model: `gemini-2.5-flash-lite` |
| Gemini 429 quota | Activate Google Cloud billing (Rp5M credit available) |
| Python not found | Use `python3` instead of `python` |
| Port 8000 in use | Add `--port 8001` to uvicorn command |
| pydantic build error | Python 3.14 incompatible — use Python 3.11 |

---

## 💡 Important Notes

- Always activate venv before running any Python commands
- The `.env` file has all 3 API keys already set
- `fetch_data.py` is the priority for Day 2
- If Bright Data or Open Data fails, `montgomery_places.py` is the fallback
- ChromaDB stores data locally in `./chroma_db/` folder
- Google Cloud has Rp5,036,251 credit expiring April 16, 2026

---

*Last updated: March 5, 2026 — End of Day 2 setup*
*Created by Claude.ai — for handoff to Claude Code*
