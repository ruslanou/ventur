"""
Ventur — FastAPI Backend
Montgomery, Alabama City Exploration Passport App
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ── Setup ──────────────────────────────────────────────────────
app = FastAPI(title="Ventur API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ── System Prompt ──────────────────────────────────────────────
system_prompt = """
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

Real places in Montgomery to recommend:
- Cahaba Brewing Co. — craft beer, Bar stamp (150 pts)
- Central Restaurant — farm-to-table, Restaurant stamp (200 pts)
- Rosa Parks Museum — history, Attraction stamp (300 pts)
- Riverwalk Stadium — baseball, Attraction stamp (250 pts)
- Vintage Café — coffee & brunch, Restaurant stamp (100 pts)
- Sky Bar Rooftop — cocktails & views, Bar stamp (200 pts)
- Montgomery Zoo — family fun, Attraction stamp (250 pts)
- Dreamland BBQ — legendary BBQ since 1958, Restaurant stamp (150 pts)
- Legacy Museum — civil rights history, Attraction stamp (300 pts)
- Alabama State Capitol — historic landmark, Attraction stamp (200 pts)
- Vintage Year Restaurant — fine dining, Restaurant stamp (250 pts)
- Irish Bred Pub — craft beer & sports, Bar stamp (125 pts)
- National Memorial for Peace and Justice — powerful memorial, Attraction stamp (350 pts)
- Alabama Shakespeare Festival — world-class theater, Attraction stamp (250 pts)
- Renaissance Montgomery Hotel — luxury hotel, Hotel stamp (200 pts)

Always end responses with an encouraging line about collecting stamps and leveling up in Ventur!
"""

# ── Models ─────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str

# ── Routes ─────────────────────────────────────────────────────
@app.get("/")
def health_check():
    return {"status": "Ventur AI is running! ✈️"}

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
        full_prompt = f"{system_prompt}\n\nUser: {request.message}\n\nVentur AI:"
        response = model.generate_content(full_prompt)
        return ChatResponse(response=response.text, status="success")
    except Exception as e:
        return ChatResponse(response=f"Sorry, something went wrong: {str(e)}", status="error")
