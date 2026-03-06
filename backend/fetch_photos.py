"""
Fetch Google Places photo references for all 19 Montgomery places.
Adds 'photo_ref' field to each place in montgomery_places.py.

Run: python fetch_photos.py
"""

import os
import re
import requests
from dotenv import load_dotenv
from montgomery_places import MONTGOMERY_PLACES

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def find_photo_ref(place_name: str, address: str) -> str | None:
    """Find Place from Text → get photo_reference."""
    query = f"{place_name}, {address}"

    # Step 1: Find Place
    find_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    resp = requests.get(find_url, params={
        "input": query,
        "inputtype": "textquery",
        "fields": "place_id,name,photos",
        "key": API_KEY,
    })
    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        print(f"  ❌ Not found: {place_name}")
        return None

    candidate = candidates[0]
    photos = candidate.get("photos", [])
    if photos:
        return photos[0]["photo_reference"]

    # Step 2: If no photos in findplace, try Place Details
    place_id = candidate.get("place_id")
    if not place_id:
        return None

    detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
    resp2 = requests.get(detail_url, params={
        "place_id": place_id,
        "fields": "photos",
        "key": API_KEY,
    })
    detail = resp2.json().get("result", {})
    photos2 = detail.get("photos", [])
    if photos2:
        return photos2[0]["photo_reference"]

    return None


def update_montgomery_places(photo_map: dict):
    """Rewrite montgomery_places.py injecting photo_ref into each place dict."""
    filepath = os.path.join(os.path.dirname(__file__), "montgomery_places.py")
    with open(filepath, "r") as f:
        content = f.read()

    for place_id, photo_ref in photo_map.items():
        if not photo_ref:
            continue
        # Insert photo_ref after the "points" line for this place
        # We'll use a regex that finds the place block and adds photo_ref if not already there
        pattern = rf'("id": "{place_id}".*?"points": \d+,)'
        replacement = rf'\1\n        "photo_ref": "{photo_ref}",'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        if new_content != content:
            content = new_content
        else:
            print(f"  ⚠️  Could not inject photo_ref for {place_id} (may already exist or pattern mismatch)")

    with open(filepath, "w") as f:
        f.write(content)
    print("\n✅ montgomery_places.py updated with photo_ref fields!")


def main():
    if not API_KEY:
        print("❌ GOOGLE_PLACES_API_KEY not set in .env")
        return

    print(f"Fetching photos for {len(MONTGOMERY_PLACES)} places...\n")
    photo_map = {}

    for place in MONTGOMERY_PLACES:
        if place.get("photo_ref"):
            print(f"  ⏭️  Skipping {place['name']} (already has photo_ref)")
            photo_map[place["id"]] = place["photo_ref"]
            continue

        print(f"  📷 {place['name']}...", end=" ", flush=True)
        ref = find_photo_ref(place["name"], place["address"])
        if ref:
            print(f"✅ got ref ({ref[:30]}...)")
        else:
            print("❌ no photo found")
        photo_map[place["id"]] = ref

    update_montgomery_places(photo_map)

    print("\nPhoto references fetched:")
    for pid, ref in photo_map.items():
        status = "✅" if ref else "❌"
        print(f"  {status} {pid}: {ref[:40] + '...' if ref else 'none'}")


if __name__ == "__main__":
    main()
