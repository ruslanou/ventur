"""
Montgomery, Alabama — Ventur Places Dataset
Real places curated for the Ventur hackathon demo.
Load this into ChromaDB for RAG-powered AI recommendations.
"""

MONTGOMERY_PLACES = [
    # ── RESTAURANTS ──────────────────────────────────────────────
    {
        "id": "rest_001",
        "name": "Central Restaurant",
        "category": "Restaurant",
        "subcategory": "Farm-to-Table",
        "address": "129 Coosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Montgomery's premier farm-to-table dining experience. Chef-driven menu featuring locally sourced Alabama ingredients. Known for their Southern-inspired dishes with a modern twist. Perfect for date nights and special occasions.",
        "hours": "Tue-Sat 5pm-10pm",
        "price_range": "$$$",
        "points": 200,
        "tags": ["upscale", "southern", "farm-to-table", "date night", "downtown"],
    },
    {
        "id": "rest_002",
        "name": "Dreamland BBQ",
        "category": "Restaurant",
        "subcategory": "BBQ",
        "address": "101 Tallapoosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Legendary Alabama BBQ institution since 1958. Famous for their slow-smoked ribs, pulled pork, and homemade sauce. A Montgomery must-visit that locals swear by. James Beard recognized Alabama BBQ culture.",
        "hours": "Mon-Sun 11am-9pm",
        "price_range": "$$",
        "points": 150,
        "tags": ["bbq", "ribs", "casual", "iconic", "family-friendly", "lunch", "dinner"],
    },
    {
        "id": "rest_003",
        "name": "Vintage Year Restaurant",
        "category": "Restaurant",
        "subcategory": "Fine Dining",
        "address": "405 Cloverdale Rd, Montgomery, AL 36106",
        "neighborhood": "Cloverdale",
        "description": "Montgomery's most beloved fine dining restaurant housed in a historic building. Renowned wine list with over 800 selections. Classic American cuisine with European influences. A Montgomery landmark since 1992.",
        "hours": "Tue-Sat 6pm-10pm",
        "price_range": "$$$$",
        "points": 250,
        "tags": ["fine dining", "wine", "romantic", "historic", "special occasion"],
    },
    {
        "id": "rest_004",
        "name": "Alley Bar & Kitchen",
        "category": "Restaurant",
        "subcategory": "American",
        "address": "Register Alley, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Beloved downtown spot tucked in historic Register Alley. Known for creative cocktails, burgers, and live music on weekends. The go-to spot for downtown Montgomery nightlife and casual dining.",
        "hours": "Mon-Sun 11am-2am",
        "price_range": "$$",
        "points": 150,
        "tags": ["casual", "burgers", "live music", "nightlife", "cocktails", "downtown"],
    },
    {
        "id": "rest_005",
        "name": "Vintage Café",
        "category": "Restaurant",
        "subcategory": "Café & Brunch",
        "address": "301 Dexter Ave, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Charming café steps from the Alabama State Capitol. Perfect for breakfast and brunch with artisan coffee, fresh pastries, and creative egg dishes. Popular with state workers and tourists exploring downtown.",
        "hours": "Mon-Fri 7am-3pm, Sat-Sun 8am-2pm",
        "price_range": "$",
        "points": 100,
        "tags": ["breakfast", "brunch", "coffee", "pastries", "casual", "downtown"],
    },
    {
        "id": "rest_006",
        "name": "True Kitchen & Bar",
        "category": "Restaurant",
        "subcategory": "Contemporary American",
        "address": "359 Dexter Ave, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Contemporary American restaurant and bar in the heart of downtown. Known for creative small plates, craft cocktails, and an impressive happy hour. Great outdoor seating with views of downtown Montgomery.",
        "hours": "Mon-Thu 11am-10pm, Fri-Sat 11am-midnight",
        "price_range": "$$",
        "points": 175,
        "tags": ["contemporary", "cocktails", "happy hour", "outdoor seating", "downtown"],
    },

    # ── BARS & NIGHTLIFE ──────────────────────────────────────────
    {
        "id": "bar_001",
        "name": "Cahaba Brewing Company",
        "category": "Bar",
        "subcategory": "Craft Brewery",
        "address": "4500 5th Ave S, Montgomery, AL 36108",
        "neighborhood": "West Montgomery",
        "description": "Award-winning craft brewery that put Montgomery on the craft beer map. Taproom featuring rotating taps of their signature ales and lagers. Live music events, food trucks on weekends. Dog-friendly outdoor space.",
        "hours": "Wed-Thu 4pm-10pm, Fri 3pm-11pm, Sat 12pm-11pm, Sun 12pm-8pm",
        "price_range": "$$",
        "points": 150,
        "tags": ["craft beer", "brewery", "live music", "dog-friendly", "outdoor", "casual"],
    },
    {
        "id": "bar_002",
        "name": "Sky Bar Rooftop",
        "category": "Bar",
        "subcategory": "Rooftop Bar",
        "address": "88 Commerce St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Montgomery's premier rooftop bar with breathtaking 360-degree views of the city skyline and Alabama River. Signature cocktails inspired by Alabama heritage. Best spot to watch the sunset over Montgomery.",
        "hours": "Wed-Sun 5pm-midnight",
        "price_range": "$$$",
        "points": 200,
        "tags": ["rooftop", "cocktails", "views", "upscale", "date night", "sunset"],
    },
    {
        "id": "bar_003",
        "name": "Irish Bred Pub",
        "category": "Bar",
        "subcategory": "Irish Pub",
        "address": "130 Commerce St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Authentic Irish pub experience in downtown Montgomery. 20+ beers on draft, live Celtic music on weekends, and classic pub grub. Known for their St. Patrick's Day celebrations and sports viewing parties.",
        "hours": "Mon-Sun 11am-2am",
        "price_range": "$$",
        "points": 125,
        "tags": ["irish pub", "sports bar", "draft beer", "live music", "casual", "downtown"],
    },

    # ── ATTRACTIONS ───────────────────────────────────────────────
    {
        "id": "attr_001",
        "name": "Rosa Parks Museum",
        "category": "Attraction",
        "subcategory": "Civil Rights Museum",
        "address": "252 Montgomery St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Powerful museum at the exact site where Rosa Parks was arrested in 1955, sparking the Montgomery Bus Boycott. Features life-size reconstructions, original artifacts, and immersive exhibits about the Civil Rights Movement. A must-visit for all Montgomery visitors.",
        "hours": "Mon-Fri 9am-5pm, Sat 9am-3pm",
        "price_range": "$",
        "points": 300,
        "tags": ["civil rights", "history", "museum", "iconic", "educational", "must-visit"],
    },
    {
        "id": "attr_002",
        "name": "Riverwalk Stadium",
        "category": "Attraction",
        "subcategory": "Sports Venue",
        "address": "200 Coosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Home of the Montgomery Biscuits, the beloved Double-A baseball affiliate of the Tampa Bay Rays. One of the most beautiful minor league ballparks in America with stunning views of the Alabama River. Famous for its giant biscuit mascot and family-friendly atmosphere.",
        "hours": "Game days vary — check schedule",
        "price_range": "$",
        "points": 250,
        "tags": ["baseball", "sports", "family-friendly", "outdoor", "entertainment", "river views"],
    },
    {
        "id": "attr_003",
        "name": "Montgomery Zoo",
        "category": "Attraction",
        "subcategory": "Zoo",
        "address": "2301 Coliseum Pkwy, Montgomery, AL 36110",
        "neighborhood": "North Montgomery",
        "description": "40-acre zoological park home to over 500 animals representing 150+ species from around the world. Features the Mann Wildlife Learning Museum with Alabama wildlife exhibits. Popular Mann Museum and African plains habitat. Great for families and wildlife enthusiasts.",
        "hours": "Daily 9am-5pm",
        "price_range": "$$",
        "points": 250,
        "tags": ["zoo", "animals", "family-friendly", "outdoor", "educational", "kids"],
    },
    {
        "id": "attr_004",
        "name": "Alabama State Capitol",
        "category": "Attraction",
        "subcategory": "Historic Landmark",
        "address": "600 Dexter Ave, Montgomery, AL 36130",
        "neighborhood": "Downtown",
        "description": "The historic Alabama State Capitol where Jefferson Davis was inaugurated as President of the Confederacy in 1861. Also the endpoint of the famous Selma to Montgomery marches in 1965. Free tours available. One of the most historically significant buildings in American history.",
        "hours": "Mon-Fri 9am-5pm",
        "price_range": "Free",
        "points": 200,
        "tags": ["historic", "civil rights", "architecture", "free", "landmark", "history"],
    },
    {
        "id": "attr_005",
        "name": "National Memorial for Peace and Justice",
        "category": "Attraction",
        "subcategory": "Memorial & Museum",
        "address": "417 Caroline St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "The nation's first memorial dedicated to the legacy of enslaved Black Americans and victims of racial terror lynching. Created by the Equal Justice Initiative. Profoundly moving outdoor installation with 800 suspended steel monuments. One of the most important cultural sites in America.",
        "hours": "Wed-Mon 9am-5pm",
        "price_range": "$",
        "points": 350,
        "tags": ["memorial", "civil rights", "history", "must-visit", "powerful", "educational"],
    },
    {
        "id": "attr_006",
        "name": "Legacy Museum",
        "category": "Attraction",
        "subcategory": "Museum",
        "address": "115 Coosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Groundbreaking museum by the Equal Justice Initiative exploring the history of racial inequality in America from slavery to mass incarceration. Built on the site of a former warehouse where enslaved people were held. Features immersive technology and powerful narratives.",
        "hours": "Wed-Mon 9am-5pm",
        "price_range": "$$",
        "points": 300,
        "tags": ["museum", "civil rights", "history", "educational", "powerful", "must-visit"],
    },
    {
        "id": "attr_007",
        "name": "Dexter Avenue King Memorial Baptist Church",
        "category": "Attraction",
        "subcategory": "Historic Church",
        "address": "454 Dexter Ave, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Where Dr. Martin Luther King Jr. served as pastor from 1954-1960 and organized the Montgomery Bus Boycott. A National Historic Landmark and one of the most important sites of the Civil Rights Movement. Guided tours available of the historic church and Dr. King's basement office.",
        "hours": "Mon-Fri 10am-4pm",
        "price_range": "$",
        "points": 300,
        "tags": ["civil rights", "MLK", "historic", "church", "landmark", "tours"],
    },
    {
        "id": "attr_008",
        "name": "Alabama Shakespeare Festival",
        "category": "Attraction",
        "subcategory": "Theater & Arts",
        "address": "1 Festival Dr, Montgomery, AL 36117",
        "neighborhood": "East Montgomery",
        "description": "One of the largest Shakespeare festivals in the world and the official state theatre of Alabama. Two beautiful theaters set in the stunning 250-acre Blount Cultural Park. Year-round performances ranging from Shakespeare classics to contemporary works and musicals.",
        "hours": "Varies by performance",
        "price_range": "$$$",
        "points": 250,
        "tags": ["theater", "arts", "shakespeare", "culture", "entertainment", "upscale"],
    },

    # ── HOTELS ────────────────────────────────────────────────────
    {
        "id": "hotel_001",
        "name": "Renaissance Montgomery Hotel",
        "category": "Hotel",
        "subcategory": "Luxury Hotel",
        "address": "201 Tallapoosa St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Montgomery's premier luxury hotel connected to the Convention Center and RSA Activity Center. Elegant rooms with stunning city views, rooftop pool, and upscale dining. Steps from all major downtown attractions and the Alabama River.",
        "hours": "24/7",
        "price_range": "$$$",
        "points": 200,
        "tags": ["luxury", "hotel", "downtown", "rooftop pool", "convention", "business"],
    },
    {
        "id": "hotel_002",
        "name": "Marriott Autograph Collection — The Lattice",
        "category": "Hotel",
        "subcategory": "Boutique Hotel",
        "address": "100 Commerce St, Montgomery, AL 36104",
        "neighborhood": "Downtown",
        "description": "Boutique luxury hotel in a beautifully restored historic downtown building. Features locally-inspired design, craft cocktail bar, and farm-to-table restaurant. Walking distance to all major civil rights landmarks and riverfront attractions.",
        "hours": "24/7",
        "price_range": "$$$",
        "points": 200,
        "tags": ["boutique", "historic", "luxury", "hotel", "downtown", "walkable"],
    },
]

def get_all_places():
    return MONTGOMERY_PLACES

def get_places_by_category(category: str):
    return [p for p in MONTGOMERY_PLACES if p["category"].lower() == category.lower()]

def get_place_by_id(place_id: str):
    return next((p for p in MONTGOMERY_PLACES if p["id"] == place_id), None)

def get_places_as_documents():
    """Format places as text documents for ChromaDB ingestion."""
    docs = []
    for place in MONTGOMERY_PLACES:
        doc = f"""
Name: {place['name']}
Category: {place['category']} — {place['subcategory']}
Address: {place['address']}
Neighborhood: {place['neighborhood']}
Description: {place['description']}
Hours: {place['hours']}
Price Range: {place['price_range']}
Ventur Points: {place['points']} pts
Tags: {', '.join(place['tags'])}
        """.strip()
        docs.append({"id": place["id"], "text": doc, "metadata": place})
    return docs

if __name__ == "__main__":
    docs = get_places_as_documents()
    print(f"✅ {len(docs)} places ready to load into ChromaDB!")
    for doc in docs:
        print(f"  - [{doc['metadata']['category']}] {doc['metadata']['name']}")
