import json

def chunk_text(text, size=300):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def run():
    with open("data/processed/cleaned_docs.json") as f:
        docs = json.load(f)

    chunks = []

    for d in docs:
        for c in chunk_text(d["cleaned_text"]):
            chunks.append({
                "brand": d["brand"],
                "chunk": c
            })

    with open("data/processed/chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)

if __name__ == "__main__":
    run()