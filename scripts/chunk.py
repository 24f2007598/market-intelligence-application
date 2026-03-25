import json
import os

def chunk_text(text, size=300):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def run():
    with open("data/processed/cleaned_docs.json") as f:
        docs = json.load(f)

    if os.path.exists("data/processed/ml_results.json"):
        with open("data/processed/ml_results.json") as f:
            ml_results = json.load(f)
    else:
        ml_results = {}

    chunks = []

    for d in docs:
        key = f"{d['url']}_{d['snapshot']}"
        change_type = ml_results.get(key, "no_change")
        
        for c in chunk_text(d["cleaned_text"]):
            chunks.append({
                "brand": d["brand"],
                "url": d["url"],
                "snapshot": d["snapshot"],
                "change_type": change_type,
                "chunk": c
            })

    with open("data/processed/chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)

if __name__ == "__main__":
    run()