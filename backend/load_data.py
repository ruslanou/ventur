"""
Ventur — Load Montgomery Places into ChromaDB
Run this once to populate the vector database.
Usage: python load_data.py
"""

import chromadb
from montgomery_places import get_places_as_documents

def load_places_to_chromadb():
    print("🚀 Starting ChromaDB data load...")

    # Initialize ChromaDB (stores locally in ./chroma_db folder)
    client = chromadb.PersistentClient(path="./chroma_db")

    # Delete existing collection if it exists (for clean reloads)
    try:
        client.delete_collection("montgomery_places")
        print("🗑️  Cleared existing collection")
    except:
        pass

    # Create fresh collection
    collection = client.create_collection(
        name="montgomery_places",
        metadata={"hnsw:space": "cosine"}
    )

    # Get all places formatted as documents
    docs = get_places_as_documents()

    # Prepare data for ChromaDB
    ids = []
    documents = []
    metadatas = []

    for doc in docs:
        ids.append(doc["id"])
        documents.append(doc["text"])
        metadatas.append({
            "name": doc["metadata"]["name"],
            "category": doc["metadata"]["category"],
            "subcategory": doc["metadata"]["subcategory"],
            "address": doc["metadata"]["address"],
            "neighborhood": doc["metadata"]["neighborhood"],
            "hours": doc["metadata"]["hours"],
            "price_range": doc["metadata"]["price_range"],
            "points": doc["metadata"]["points"],
            "tags": ", ".join(doc["metadata"]["tags"]),
        })

    # Load into ChromaDB
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"✅ Successfully loaded {len(ids)} places into ChromaDB!")
    print("\n📍 Places loaded:")
    for doc in docs:
        print(f"  [{doc['metadata']['category']}] {doc['metadata']['name']}")

    # Quick test query
    print("\n🧪 Testing search: 'best place for craft beer'")
    results = collection.query(
        query_texts=["best place for craft beer"],
        n_results=3
    )
    print("Top results:")
    for i, meta in enumerate(results["metadatas"][0]):
        print(f"  {i+1}. {meta['name']} ({meta['category']})")

    print("\n🎉 ChromaDB is ready for Ventur AI!")

if __name__ == "__main__":
    load_places_to_chromadb()
