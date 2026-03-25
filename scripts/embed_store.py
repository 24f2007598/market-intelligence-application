from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import json
from utils.config import COLLECTION_NAME

client = QdrantClient("localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")


def run():
    with open("data/processed/chunks.json") as f:
        chunks = json.load(f)

    vectors = []
    payloads = []
    ids = []

    for i, c in enumerate(chunks):
        emb = model.encode(c["chunk"]).tolist()

        vectors.append(emb)
        payloads.append({
            "text": c["chunk"],
            "brand": c["brand"],
            "url": c.get("url", ""),
            "change_type": c.get("change_type", "no_change")
        })
        ids.append(i)

    # recreate collection
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"size": 384, "distance": "Cosine"}
    )

    client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=vectors,
        payload=payloads,
        ids=ids
    )

    print(f"✅ Uploaded {len(vectors)} vectors to Qdrant")


if __name__ == "__main__":
    run()

# from qdrant_client import QdrantClient
# from sentence_transformers import SentenceTransformer
# import json
# from utils.config import COLLECTION_NAME

# client = QdrantClient("localhost", port=6333)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def run():
#     with open("data/processed/chunks.json") as f:
#         chunks = json.load(f)

#     vectors = []
#     payloads = []

#     for i, c in enumerate(chunks):
#         emb = model.encode(c["chunk"]).tolist()

#         vectors.append((i, emb))
#         payloads.append({
#             "text": c["chunk"],
#             "brand": c["brand"]
#         })

#     client.recreate_collection(
#         collection_name=COLLECTION_NAME,
#         vectors_config={"size": 384, "distance": "Cosine"}
#     )

#     client.upload_collection(
#         collection_name=COLLECTION_NAME,
#         vectors=[v[1] for v in vectors],
#         payload=payloads,
#         ids=[v[0] for v in vectors]
#     )

# if __name__ == "__main__":
#     run()