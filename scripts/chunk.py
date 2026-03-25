import json
from tqdm import tqdm

CHUNK_SIZE = 300  # words
OVERLAP = 50

def chunk_text(text, chunk_size=120, overlap=30):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks
    
# load raw data
with open("data/raw_docs.json", "r") as f:
    docs = json.load(f)

all_chunks = []

for doc in tqdm(docs):
    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "id": f"{doc['url']}_{i}",
            "text": chunk,
            "source": doc["url"]
        })

# save chunks
with open("data/chunks.json", "w") as f:
    json.dump(all_chunks, f, indent=2)

print("Saved to data/chunks.json")