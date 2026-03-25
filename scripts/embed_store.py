import json
import chromadb
from sentence_transformers import SentenceTransformer

# ----------------------------
# INIT
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(name="competitor_data")

# ----------------------------
# LOAD CHUNKS
# ----------------------------
with open("data/chunks.json", "r") as f:
    chunks = json.load(f)

# ----------------------------
# PREPARE DATA
# ----------------------------
documents = []
metadatas = []
ids = []

for i, chunk in enumerate(chunks):
    documents.append(chunk["text"])
    metadatas.append({"source": chunk["source"]})
    ids.append(f"{chunk['id']}_{i}")

# ----------------------------
# GENERATE EMBEDDINGS
# ----------------------------
print("Generating embeddings...")
embeddings = model.encode(documents, show_progress_bar=True)

# ----------------------------
# STORE IN CHROMA
# ----------------------------
print("Storing in ChromaDB...")
collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
    ids=ids
)



print("✅ Embeddings stored successfully!")