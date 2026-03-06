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
import re
import json
import asyncio
import httpx
import chromadb
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

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
    for result in data.get("results", [])[:15]:  # Max 15 per type
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

async def fetch_brightdata_session(session: ClientSession, query: str) -> list:
    """Run a single Bright Data search query inside an existing MCP session."""
    print(f"🌐 Bright Data: '{query}'...")
    try:
        result = await session.call_tool("search_engine", {"query": query, "limit": 10})
        text = result.content[0].text if result.content else "{}"
        data = json.loads(text)
        places = []
        for item in data.get("organic", []):
            title = item.get("title", "").strip()
            desc = item.get("description", "").strip()
            link = item.get("link", "")
            if not title or not desc:
                continue
            # Clean title: strip trailing " - Site Name" patterns, truncate long titles
            name = title.split(" - ")[0].split(" | ")[0][:80].strip()
            place = {
                "id": f"brightdata_{abs(hash(link or title)) % 1000000}",
                "name": name,
                "category": guess_category(query),
                "subcategory": "Web Reference",
                "address": "Montgomery, AL",
                "neighborhood": "Montgomery",
                "description": f"{name}. {desc}"[:600],
                "hours": "Check website for current hours",
                "price_range": "$$",
                "points": 150,
                "tags": ["montgomery", "bright data", "web reference"],
                "source": "bright_data",
            }
            places.append(place)
            print(f"  ✅ {name[:60]}")
        return places
    except Exception as e:
        print(f"  ⚠️ Bright Data query error: {e}")
        return []


async def fetch_brightdata_all(queries: list) -> list:
    """Open one MCP session and run all queries."""
    if not BRIGHT_DATA_TOKEN:
        print("⚠️ BRIGHT_DATA_TOKEN not set — skipping")
        return []
    url = f"https://mcp.brightdata.com/mcp?token={BRIGHT_DATA_TOKEN}"
    print("🌐 Connecting to Bright Data MCP...")
    try:
        async with streamablehttp_client(url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                print(f"  → {len(tools.tools)} tools available: {[t.name for t in tools.tools]}")
                all_places = []
                for query in queries:
                    places = await fetch_brightdata_session(session, query)
                    all_places.extend(places)
                    await asyncio.sleep(1)
                # Scrape TripAdvisor within the same session
                ta_places = await fetch_tripadvisor_restaurants(session)
                all_places.extend(ta_places)
                return all_places
    except Exception as e:
        print(f"  ⚠️ Bright Data MCP connection failed: {e}")
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
# 2b. TRIPADVISOR SCRAPE (via Bright Data)
# ─────────────────────────────────────────────

_TA_LINK_RE = re.compile(r'\\\[\n+([^\n\[\\]{2,80}?)\n+\]\\\(/Restaurant')
_TA_RATING_RE = re.compile(r'(\d+\.?\d*)\s+of\s+5\s+bubbles?')


def _ta_is_junk(name: str) -> bool:
    if name.startswith('(') or name[-1] in '.!?':
        return True
    generic = {'amazing', 'excellent', 'great', 'nice', 'good', 'love', 'best',
               'terrible', 'awful', 'ok', 'okay', 'wow', 'perfect'}
    return name.lower() in generic


def parse_tripadvisor_markdown(markdown: str) -> list:
    """Parse restaurant entries from TripAdvisor scraped markdown (escaped-bracket format)."""
    places = []
    seen = set()

    for m in _TA_LINK_RE.finditer(markdown):
        name = m.group(1).strip()
        if not name or len(name) < 3 or _ta_is_junk(name):
            continue

        # Find the closing ) of the URL link
        url_end = markdown.find(')', m.end())
        if url_end == -1 or url_end - m.end() > 200:
            continue
        after_link = url_end + 1

        # Rating must be within 80 chars of link end (real restaurant entries)
        ctx_tight = markdown[after_link: after_link + 80]
        rating_m = _TA_RATING_RE.search(ctx_tight)
        if not rating_m:
            continue
        rating = float(rating_m.group(1))
        if rating == 0:
            continue

        key = name.lower()
        if key in seen:
            continue
        seen.add(key)

        ctx = markdown[after_link: after_link + 400]
        reviews_m = re.search(r'\(([\d,]+)\s+reviews?\)', ctx)
        price_m = re.search(r'(\$+)', ctx)
        cuisine_m = re.search(r'([A-Za-z][A-Za-z ,&]{1,40}?)(\$+)', ctx)

        reviews = reviews_m.group(1).replace(',', '') if reviews_m else '0'
        price = price_m.group(1) if price_m else '$$'
        cuisine = cuisine_m.group(1).strip() if cuisine_m else ''
        if len(cuisine) > 40:
            cuisine = ''

        tags = ['montgomery', 'restaurant', 'tripadvisor']
        if cuisine:
            tags.extend([c.strip().lower() for c in cuisine.split(',')[:3]])
        if rating >= 4.5:
            tags.append('highly rated')
        elif rating >= 4.0:
            tags.append('top rated')

        desc_parts = [f"{name} — restaurant in Montgomery, Alabama."]
        if cuisine:
            desc_parts.append(f"Cuisine: {cuisine}.")
        if rating > 0:
            desc_parts.append(f"TripAdvisor rating: {rating}/5 ({reviews} reviews).")

        places.append({
            'id': f'tripadvisor_{abs(hash(name.lower())) % 1000000}',
            'name': name,
            'category': 'Restaurant',
            'subcategory': cuisine.split(',')[0].strip() if cuisine else 'Restaurant',
            'address': 'Montgomery, AL',
            'neighborhood': 'Montgomery',
            'description': ' '.join(desc_parts)[:600],
            'hours': 'Check TripAdvisor for current hours',
            'price_range': price,
            'points': 150,
            'rating': rating,
            'tags': tags,
            'source': 'tripadvisor',
        })

    return places


async def fetch_tripadvisor_restaurants(session: ClientSession) -> list:
    """Scrape TripAdvisor Montgomery restaurants page via Bright Data scrape_as_markdown."""
    print("🍽️  Scraping TripAdvisor Montgomery restaurants...")
    try:
        result = await session.call_tool('scrape_as_markdown', {
            'url': 'https://www.tripadvisor.com/Restaurants-g30712-Montgomery_Alabama.html'
        })
        text = result.content[0].text if result.content else ''
        if not text:
            print("  ⚠️ No content returned from TripAdvisor")
            return []
        places = parse_tripadvisor_markdown(text)
        print(f"  → {len(places)} restaurants parsed from TripAdvisor")
        for p in places:
            print(f"  ✅ {p['name']} ({p.get('rating', '?')}⭐ {p['price_range']})")
        return places
    except Exception as e:
        print(f"  ⚠️ TripAdvisor scrape error: {e}")
        return []


# ─────────────────────────────────────────────
# 3. MONTGOMERY OPEN DATA PORTAL
# ─────────────────────────────────────────────

async def fetch_montgomery_open_data():
    """Fetch official POI data from Montgomery Open Data Portal (CSV)."""
    print("🏛️ Fetching from Montgomery Open Data Portal (POI CSV)...")

    url = (
        "https://opendata.arcgis.com/api/v3/datasets/"
        "4c077a7c159a414983b5cd4b99f9f921_0/downloads/data"
        "?format=csv&spatialRefId=4326"
    )

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()

        lines = response.text.strip().splitlines()
        # Parse CSV manually (simple, no pandas needed)
        import csv, io
        reader = csv.DictReader(io.StringIO(response.text))
        places = []

        for row in reader:
            name = row.get("FACILITYID", "").strip()
            poi_type = row.get("Type", "").strip()
            address = row.get("FULLADDR", "Montgomery, AL").strip()
            description = row.get("Description", "").strip()
            obj_id = row.get("OBJECTID", "")

            if not name:
                continue

            place = {
                "id": f"opendata_{obj_id}",
                "name": name,
                "category": map_open_data_type(poi_type),
                "subcategory": poi_type or "Point of Interest",
                "address": f"{address}, Montgomery, AL" if address and "Montgomery" not in address else address,
                "neighborhood": "Montgomery",
                "description": description if description else f"{name} — an official Montgomery point of interest.",
                "hours": "Check website for hours",
                "price_range": "$",
                "points": 250,
                "tags": ["montgomery", "official city data", poi_type.lower()],
                "source": "montgomery_open_data",
            }
            places.append(place)
            print(f"  ✅ {name} ({poi_type})")

        print(f"  → {len(places)} official POIs loaded")
        return places

    except Exception as e:
        print(f"  ⚠️ Open Data fetch error: {e}")
        return []


async def fetch_montgomery_parks():
    """Fetch park data with amenities from Montgomery Open Data Portal (CSV)."""
    print("🌳 Fetching from Montgomery Parks & Trail dataset...")

    url = (
        "https://opendata.arcgis.com/api/v3/datasets/"
        "3a030d87c47d490ca32e72a963a3d0c0_0/downloads/data"
        "?format=csv&spatialRefId=4326"
    )

    AMENITY_FIELDS = [
        "SWIMMING", "HIKING", "FISHING", "PICNIC", "PLAYGROUND",
        "GOLF", "SOCCER", "BASEBALL", "SOFTBALL", "BASKETBALL",
        "TENNIS", "SKATEBOARD", "BOATING", "CAMPING", "PETS",
    ]

    try:
        import csv, io
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()

        reader = csv.DictReader(io.StringIO(response.text))
        places = []

        for row in reader:
            name = row.get("FACILITYID", "").strip()
            address = row.get("FULLADDR", "Montgomery, AL").strip()
            hours = row.get("OPERHOURS", "").strip()
            days = row.get("OPERDAYS", "").strip()
            area = row.get("PARKAREA", "").strip()
            obj_id = row.get("OBJECTID", "")

            if not name:
                continue

            amenities = [f.lower() for f in AMENITY_FIELDS if row.get(f, "N") == "Y"]

            hours_str = f"{days} {hours}".strip() if days or hours else "Check park hours"
            area_str = f"{float(area):.1f} acres" if area else ""
            amenity_str = ", ".join(amenities) if amenities else "general park"

            description = (
                f"{name} is a Montgomery city park"
                + (f" ({area_str})" if area_str else "")
                + f". Activities available: {amenity_str}."
                + (f" Hours: {hours_str}." if hours_str else "")
            )

            place = {
                "id": f"park_{abs(hash(name)) % 1000000}",
                "name": name,
                "category": "Attraction",
                "subcategory": "Park",
                "address": f"{address}, Montgomery, AL" if "Montgomery" not in address else address,
                "neighborhood": "Montgomery",
                "description": description,
                "hours": hours_str,
                "price_range": "Free",
                "points": 150,
                "tags": ["montgomery", "park", "outdoor"] + amenities,
                "source": "montgomery_parks",
            }
            places.append(place)
            print(f"  ✅ {name} ({amenity_str[:50]})")

        print(f"  → {len(places)} parks loaded")
        return places

    except Exception as e:
        print(f"  ⚠️ Parks fetch error: {e}")
        return []


def map_open_data_type(type_str: str) -> str:
    mapping = {
        "Museum": "Attraction",
        "Historical Place": "Attraction",
        "Arts Center": "Attraction",
        "Recreation": "Attraction",
        "Sports Field": "Attraction",
        "Theatre": "Attraction",
        "Zoo": "Attraction",
        "Farmer's Market": "Attraction",
    }
    return mapping.get(type_str, "Attraction")


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
            ("restaurant", "bbq southern soul food"),
            ("bar", None),
            ("night_club", None),
            ("cafe", None),
            ("tourist_attraction", None),
            ("museum", None),
            ("lodging", None),
            ("park", "Montgomery Alabama park"),
            ("stadium", None),
        ]
        for place_type, keyword in google_types:
            places = await fetch_google_places(place_type, keyword)
            all_places.extend(places)
            await asyncio.sleep(0.5)  # Rate limiting
    else:
        print("⚠️ GOOGLE_PLACES_API_KEY not found in .env — skipping")

    # ── Source 2: Bright Data MCP ──
    bright_queries = [
        "best restaurants Montgomery Alabama 2024",
        "top bars nightlife breweries Montgomery Alabama",
        "must visit tourist attractions museums Montgomery Alabama",
        "best hotels stay Montgomery Alabama",
    ]
    bright_places = await fetch_brightdata_all(bright_queries)
    all_places.extend(bright_places)

    # ── Source 3: Montgomery Open Data — POIs ──
    open_data_places = await fetch_montgomery_open_data()
    all_places.extend(open_data_places)

    # ── Source 3b: Montgomery Open Data — Parks ──
    park_places = await fetch_montgomery_parks()
    all_places.extend(park_places)

    # ── Source 4: Curated Montgomery Places (handpicked for passport) ──
    print("\n📋 Loading curated Montgomery places...")
    from montgomery_places import MONTGOMERY_PLACES
    for p in MONTGOMERY_PLACES:
        curated = {**p, "source": "curated"}
        all_places.append(curated)
        print(f"  ✅ {p['name']} ({p['category']})")
    print(f"  → {len(MONTGOMERY_PLACES)} curated places added")

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
