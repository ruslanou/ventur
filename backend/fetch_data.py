"""
Ventur — Real Data Fetcher
Pulls live Montgomery data from:
1. Google Places API
2. Bright Data MCP (web scraping)
3. Montgomery Open Data Portal
Then loads everything into ChromaDB.

Usage: python fetch_data.py
"""

import os
import json
import asyncio
import httpx
import chromadb
from dotenv import load_dotenv

load_dotenv()

GOOGLE_PLACES_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
BRIGHT_DATA_TOKEN = os.getenv("BRIGHT_DATA_TOKEN")

# Montgomery, AL coordinates
MONTGOMERY_LAT = 32.3792
MONTGOMERY_LNG = -86.3077
SEARCH_RADIUS = 5000  # 5km radius

# ─────────────────────────────────────────────
# 1. GOOGLE PLACES API
# ─────────────────────────────────────────────

async def fetch_google_places(place_type: str, keyword: str = None):
    """Fetch places from Google Places API near Montgomery, AL"""
    print(f"🔍 Fetching {place_type}s from Google Places API...")

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{MONTGOMERY_LAT},{MONTGOMERY_LNG}",
        "radius": SEARCH_RADIUS,
        "type": place_type,
        "key": GOOGLE_PLACES_KEY,
    }
    if keyword:
        params["keyword"] = keyword

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    if data.get("status") != "OK":
        print(f"  ⚠️ Google Places error: {data.get('status')} — {data.get('error_message', '')}")
        return []

    places = []
    for result in data.get("results", [])[:10]:  # Max 10 per type
        place = {
            "id": f"google_{result['place_id']}",
            "name": result.get("name", ""),
            "category": map_google_type(place_type),
            "subcategory": place_type.replace("_", " ").title(),
            "address": result.get("vicinity", "Montgomery, AL"),
            "neighborhood": "Montgomery",
            "description": f"{result.get('name', '')} — a highly rated {place_type.replace('_', ' ')} in Montgomery, Alabama. Rating: {result.get('rating', 'N/A')}/5 ({result.get('user_ratings_total', 0)} reviews).",
            "hours": "See Google Maps for hours",
            "price_range": "$" * (result.get("price_level", 2) or 2),
            "points": calculate_points(place_type),
            "rating": result.get("rating", 0),
            "tags": extract_tags(result, place_type),
            "source": "google_places",
        }
        places.append(place)
        print(f"  ✅ {place['name']} ({place['rating']}⭐)")

    return places


def map_google_type(place_type: str) -> str:
    mapping = {
        "restaurant": "Restaurant",
        "bar": "Bar",
        "tourist_attraction": "Attraction",
        "museum": "Attraction",
        "lodging": "Hotel",
        "night_club": "Bar",
        "cafe": "Restaurant",
        "park": "Attraction",
    }
    return mapping.get(place_type, "Place")


def calculate_points(place_type: str) -> int:
    points_map = {
        "restaurant": 150,
        "bar": 150,
        "tourist_attraction": 300,
        "museum": 300,
        "lodging": 200,
        "night_club": 150,
        "cafe": 100,
        "park": 200,
    }
    return points_map.get(place_type, 100)


def extract_tags(result: dict, place_type: str) -> list:
    tags = [place_type.replace("_", " ")]
    if result.get("rating", 0) >= 4.5:
        tags.append("highly rated")
    if result.get("price_level", 2) <= 1:
        tags.append("budget friendly")
    elif result.get("price_level", 2) >= 3:
        tags.append("upscale")
    types = result.get("types", [])
    for t in types[:3]:
        if t not in ["point_of_interest", "establishment", "food"]:
            tags.append(t.replace("_", " "))
    return tags


# ─────────────────────────────────────────────
# 2. BRIGHT DATA MCP
# ─────────────────────────────────────────────

async def fetch_brightdata(query: str):
    """Fetch live Montgomery data using Bright Data web search"""
    print(f"🌐 Bright Data searching: '{query}'...")

    url = f"https://mcp.brightdata.com/mcp?token={BRIGHT_DATA_TOKEN}"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "search_engine",
            "arguments": {
                "query": query,
                "limit": 5
            }
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            data = response.json()

        results = data.get("result", {}).get("content", [])
        places = []

        for item in results:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                place = {
                    "id": f"brightdata_{abs(hash(text)) % 100000}",
                    "name": extract_name_from_text(text, query),
                    "category": guess_category(query),
                    "subcategory": "Live Web Data",
                    "address": "Montgomery, AL",
                    "neighborhood": "Montgomery",
                    "description": text[:500] if text else "Popular Montgomery destination.",
                    "hours": "Check website for current hours",
                    "price_range": "$$",
                    "points": 150,
                    "tags": ["montgomery", "live data"],
                    "source": "bright_data",
                }
                if place["name"]:
                    places.append(place)
                    print(f"  ✅ Found: {place['name']}")

        return places

    except Exception as e:
        print(f"  ⚠️ Bright Data error: {e}")
        return []


def extract_name_from_text(text: str, query: str) -> str:
    """Extract a place name from scraped text"""
    lines = text.strip().split("\n")
    for line in lines[:3]:
        line = line.strip()
        if line and len(line) < 60 and len(line) > 3:
            return line
    return query.replace("Montgomery AL", "").strip()


def guess_category(query: str) -> str:
    query_lower = query.lower()
    if any(w in query_lower for w in ["restaurant", "food", "eat", "dining", "bbq", "cafe"]):
        return "Restaurant"
    elif any(w in query_lower for w in ["bar", "brewery", "pub", "cocktail", "nightlife"]):
        return "Bar"
    elif any(w in query_lower for w in ["museum", "attraction", "historic", "tour", "park"]):
        return "Attraction"
    elif any(w in query_lower for w in ["hotel", "stay", "lodging"]):
        return "Hotel"
    return "Place"


# ─────────────────────────────────────────────
# 3. MONTGOMERY OPEN DATA PORTAL
# ─────────────────────────────────────────────

async def fetch_montgomery_open_data():
    """Fetch points of interest from Montgomery Open Data ArcGIS API"""
    print("🏛️ Fetching from Montgomery Open Data Portal...")

    # ArcGIS REST API for Montgomery POIs
    url = "https://services.arcgis.com/PkLBxBKhHZkW9fhr/arcgis/rest/services/PointofInterest/FeatureServer/0/query"
    params = {
        "where": "1=1",
        "outFields": "*",
        "f": "json",
        "resultRecordCount": 50,
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params)
            data = response.json()

        if "error" in data:
            print(f"  ⚠️ Open Data error: {data['error']}")
            return []

        features = data.get("features", [])
        places = []

        for feature in features:
            attrs = feature.get("attributes", {})
            name = attrs.get("Name") or attrs.get("NAME") or attrs.get("name", "")
            if not name:
                continue

            place = {
                "id": f"opendata_{attrs.get('OBJECTID', abs(hash(name)))}",
                "name": name,
                "category": map_open_data_type(attrs.get("Type") or attrs.get("TYPE", "")),
                "subcategory": attrs.get("SubType") or attrs.get("SUBTYPE") or "Point of Interest",
                "address": attrs.get("Address") or attrs.get("ADDRESS") or "Montgomery, AL",
                "neighborhood": attrs.get("Neighborhood") or "Montgomery",
                "description": attrs.get("Description") or attrs.get("DESCRIPTION") or f"{name} — a point of interest in Montgomery, Alabama.",
                "hours": attrs.get("Hours") or "Check website for hours",
                "price_range": "$$",
                "points": 200,
                "tags": ["montgomery", "official", "point of interest"],
                "source": "montgomery_open_data",
            }
            places.append(place)
            print(f"  ✅ {place['name']} ({place['category']})")

        return places

    except Exception as e:
        print(f"  ⚠️ Open Data fetch error: {e}")
        return []


def map_open_data_type(type_str: str) -> str:
    type_lower = (type_str or "").lower()
    if any(w in type_lower for w in ["restaurant", "food", "dining"]):
        return "Restaurant"
    elif any(w in type_lower for w in ["bar", "pub", "brewery"]):
        return "Bar"
    elif any(w in type_lower for w in ["museum", "historic", "park", "recreation"]):
        return "Attraction"
    elif any(w in type_lower for w in ["hotel", "lodging"]):
        return "Hotel"
    return "Attraction"


# ─────────────────────────────────────────────
# 4. LOAD INTO CHROMADB
# ─────────────────────────────────────────────

def deduplicate_places(places: list) -> list:
    """Remove duplicates based on similar names"""
    seen_names = set()
    unique = []
    for place in places:
        name_key = place["name"].lower().strip()[:20]
        if name_key not in seen_names and place["name"]:
            seen_names.add(name_key)
            unique.append(place)
    return unique


def place_to_document(place: dict) -> str:
    """Convert place dict to text document for ChromaDB"""
    return f"""
Name: {place['name']}
Category: {place['category']} — {place['subcategory']}
Address: {place['address']}
Neighborhood: {place['neighborhood']}
Description: {place['description']}
Hours: {place['hours']}
Price Range: {place['price_range']}
Ventur Points: {place['points']} pts
Tags: {', '.join(place.get('tags', []))}
Source: {place.get('source', 'unknown')}
    """.strip()


def load_to_chromadb(places: list):
    """Load all places into ChromaDB"""
    print(f"\n💾 Loading {len(places)} places into ChromaDB...")

    client = chromadb.PersistentClient(path="./chroma_db")

    try:
        client.delete_collection("montgomery_places")
        print("🗑️  Cleared existing collection")
    except:
        pass

    collection = client.create_collection(
        name="montgomery_places",
        metadata={"hnsw:space": "cosine"}
    )

    ids, documents, metadatas = [], [], []

    for place in places:
        ids.append(str(place["id"]))
        documents.append(place_to_document(place))
        metadatas.append({
            "name": place["name"],
            "category": place["category"],
            "address": place["address"],
            "points": place["points"],
            "source": place.get("source", "unknown"),
            "tags": ", ".join(place.get("tags", [])),
        })

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"✅ {len(ids)} places loaded into ChromaDB!")

    # Quick test
    print("\n🧪 Test search: 'best BBQ in Montgomery'")
    results = collection.query(query_texts=["best BBQ in Montgomery"], n_results=3)
    for meta in results["metadatas"][0]:
        print(f"  → {meta['name']} ({meta['category']}) [{meta['source']}]")


# ─────────────────────────────────────────────
# 5. MAIN — RUN ALL SOURCES
# ─────────────────────────────────────────────

async def main():
    print("🚀 Ventur Real Data Fetcher Starting...\n")
    all_places = []

    # ── Source 1: Google Places ──
    if GOOGLE_PLACES_KEY:
        google_types = [
            ("restaurant", None),
            ("bar", None),
            ("tourist_attraction", None),
            ("museum", None),
        ]
        for place_type, keyword in google_types:
            places = await fetch_google_places(place_type, keyword)
            all_places.extend(places)
            await asyncio.sleep(0.5)  # Rate limiting
    else:
        print("⚠️ GOOGLE_PLACES_API_KEY not found in .env — skipping")

    # ── Source 2: Bright Data ──
    if BRIGHT_DATA_TOKEN:
        bright_queries = [
            "best restaurants Montgomery AL 2024",
            "top bars nightlife Montgomery Alabama",
            "must visit attractions Montgomery AL",
        ]
        for query in bright_queries:
            places = await fetch_brightdata(query)
            all_places.extend(places)
            await asyncio.sleep(1)  # Rate limiting
    else:
        print("⚠️ BRIGHT_DATA_TOKEN not found in .env — skipping")

    # ── Source 3: Montgomery Open Data ──
    open_data_places = await fetch_montgomery_open_data()
    all_places.extend(open_data_places)

    # ── Deduplicate & Load ──
    unique_places = deduplicate_places(all_places)
    print(f"\n📊 Summary:")
    print(f"  Total fetched: {len(all_places)}")
    print(f"  After dedup:   {len(unique_places)}")

    if unique_places:
        load_to_chromadb(unique_places)
        # Save to JSON for reference
        with open("fetched_places.json", "w") as f:
            json.dump(unique_places, f, indent=2)
        print(f"\n💾 Saved to fetched_places.json for reference")
        print("\n🎉 All done! Ventur AI is now powered by real Montgomery data!")
    else:
        print("\n⚠️ No places fetched! Check your API keys in .env")


if __name__ == "__main__":
    asyncio.run(main())
