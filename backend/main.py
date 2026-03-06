"""
Ventur — FastAPI Backend
Montgomery, Alabama City Exploration Passport App
Day 3: ChromaDB RAG + /places, /stamp, /profile endpoints
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv

from montgomery_places import MONTGOMERY_PLACES, get_place_by_id

load_dotenv()

# ── Setup ──────────────────────────────────────────────────────
app = FastAPI(title="Ventur API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ── ChromaDB ───────────────────────────────────────────────────
chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    collection = chroma_client.get_collection("montgomery_places")
    print(f"✅ ChromaDB loaded: {collection.count()} places")
except Exception as e:
    print(f"⚠️  ChromaDB not found — run fetch_data.py first. Error: {e}")
    collection = None

# ── In-Memory User Store (hackathon demo) ─────────────────────
# { user_id: { "points": int, "stamps": [place_id, ...], "level": str } }
users: dict = {}

LEVEL_THRESHOLDS = [
    (0,    "Explorer 🌱"),
    (500,  "Adventurer ⚡"),
    (1000, "Pathfinder 🔥"),
    (2000, "Legend 👑"),
]

def get_level(points: int) -> str:
    level = "Explorer 🌱"
    for threshold, name in LEVEL_THRESHOLDS:
        if points >= threshold:
            level = name
    return level

def get_or_create_user(user_id: str) -> dict:
    if user_id not in users:
        users[user_id] = {"points": 0, "stamps": [], "level": "Explorer 🌱"}
    return users[user_id]

# ── System Prompt ──────────────────────────────────────────────
BASE_SYSTEM_PROMPT = """
You are Ventur AI, a fun and friendly city exploration guide for Montgomery, Alabama.

You help users discover the best hospitality experiences in the city including:
- Restaurants and cafes
- Bars and nightlife
- Tourist attractions and activities
- Local events and entertainment
- Hotels and accommodations

Your personality is:
- Enthusiastic and adventurous 🌟
- Like a knowledgeable local friend
- Always encouraging users to explore and collect stamps
- Short and punchy responses — no long paragraphs

When recommending places always include:
- Place name
- What makes it special
- What type of stamp/points they can earn

Always end responses with an encouraging line about collecting stamps and leveling up in Ventur!
"""

def build_rag_context(query: str) -> str:
    """Query ChromaDB and return relevant places as context."""
    if collection is None:
        return ""
    try:
        results = collection.query(query_texts=[query], n_results=5)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        if not docs:
            return ""
        lines = ["Here are the most relevant Montgomery places for this query:\n"]
        for doc, meta in zip(docs, metas):
            lines.append(f"---\n{doc}\n")
        return "\n".join(lines)
    except Exception as e:
        print(f"⚠️  ChromaDB query error: {e}")
        return ""

# ── Request/Response Models ────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str

class StampRequest(BaseModel):
    user_id: str
    place_id: str

class StampResponse(BaseModel):
    success: bool
    message: str
    points_earned: int
    total_points: int
    total_stamps: int
    level: str
    place_name: str

# ── Routes ─────────────────────────────────────────────────────
@app.get("/")
def health_check():
    chroma_count = collection.count() if collection else 0
    return {
        "status": "Ventur AI is running! ✈️",
        "version": "2.0.0",
        "places_in_db": chroma_count,
    }

@app.get("/test-gemini")
def test_gemini():
    try:
        response = model.generate_content(
            "Say one exciting sentence about exploring Montgomery, Alabama."
        )
        return {"message": response.text, "status": "Gemini is working! ✅"}
    except Exception as e:
        return {"error": str(e), "status": "Gemini failed ❌"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        rag_context = build_rag_context(request.message)
        context_section = f"\n\n{rag_context}" if rag_context else ""
        full_prompt = f"{BASE_SYSTEM_PROMPT}{context_section}\n\nUser: {request.message}\n\nVentur AI:"
        response = model.generate_content(full_prompt)
        return ChatResponse(response=response.text, status="success")
    except Exception as e:
        return ChatResponse(response=f"Sorry, something went wrong: {str(e)}", status="error")

@app.get("/places")
def get_places(category: Optional[str] = None):
    """Return all passport places. Filter by category: Restaurant, Bar, Attraction, Hotel."""
    places = MONTGOMERY_PLACES
    if category:
        places = [p for p in places if p["category"].lower() == category.lower()]
    return {"places": places, "count": len(places)}

@app.get("/places/{place_id}")
def get_place(place_id: str):
    """Return a single place by ID."""
    place = get_place_by_id(place_id)
    if not place:
        raise HTTPException(status_code=404, detail=f"Place '{place_id}' not found")
    return place

@app.post("/stamp", response_model=StampResponse)
def stamp_place(request: StampRequest):
    """Record a QR scan stamp for a user at a place."""
    place = get_place_by_id(request.place_id)
    if not place:
        raise HTTPException(status_code=404, detail=f"Place '{request.place_id}' not found")

    user = get_or_create_user(request.user_id)

    if request.place_id in user["stamps"]:
        return StampResponse(
            success=False,
            message=f"You already stamped {place['name']}! Find a new place to explore.",
            points_earned=0,
            total_points=user["points"],
            total_stamps=len(user["stamps"]),
            level=user["level"],
            place_name=place["name"],
        )

    # Award stamp + points
    user["stamps"].append(request.place_id)
    user["points"] += place["points"]
    user["level"] = get_level(user["points"])

    return StampResponse(
        success=True,
        message=f"🎉 Stamp collected! You visited {place['name']}!",
        points_earned=place["points"],
        total_points=user["points"],
        total_stamps=len(user["stamps"]),
        level=user["level"],
        place_name=place["name"],
    )

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    """Return user profile: level, points, stamps, and stamped place details."""
    user = get_or_create_user(user_id)
    stamped_places = [get_place_by_id(pid) for pid in user["stamps"] if get_place_by_id(pid)]
    total_available = len(MONTGOMERY_PLACES)
    completion_pct = round(len(stamped_places) / total_available * 100, 1)

    next_level_info = None
    for threshold, level_name in LEVEL_THRESHOLDS:
        if threshold > user["points"]:
            next_level_info = {"level": level_name, "points_needed": threshold - user["points"]}
            break

    return {
        "user_id": user_id,
        "level": user["level"],
        "points": user["points"],
        "stamps_collected": len(stamped_places),
        "stamps_available": total_available,
        "completion_percent": completion_pct,
        "next_level": next_level_info,
        "stamped_places": stamped_places,
    }
