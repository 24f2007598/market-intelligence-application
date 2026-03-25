import json
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def extract_numbers(text):
    return set(re.findall(r'\d+', text))

def compute_eda():
    with open("data/processed/pairs.json", "r") as f:
        pairs = json.load(f)

    if not pairs:
        print("No pairs found!")
        return

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"Computing EDA for {len(pairs)} pairs...")

    old_texts = [p["old_text"] for p in pairs]
    new_texts = [p["new_text"] for p in pairs]

    old_embs = model.encode(old_texts)
    new_embs = model.encode(new_texts)

    eda_pairs = []

    for i in range(len(pairs)):
        sim = cosine_similarity(old_embs[i].reshape(1, -1), new_embs[i].reshape(1, -1))[0][0]

        old_text = pairs[i]["old_text"].lower()
        new_text = pairs[i]["new_text"].lower()

        len_diff = len(new_text) - len(old_text)

        keywords = ["₹", "price", "discount", "offer", "feature", "premium", "battery", "camera"]
        keyword_diffs = {}
        for kw in keywords:
            kw_old = old_text.count(kw)
            kw_new = new_text.count(kw)
            keyword_diffs[kw] = kw_new - kw_old
            
        nums_old = extract_numbers(old_text)
        nums_new = extract_numbers(new_text)
        numbers_changed = bool(nums_new - nums_old or nums_old - nums_new)

        enriched_pair = {
            **pairs[i],
            "similarity": float(sim),
            "length_difference": len_diff,
            "keyword_diffs": keyword_diffs,
            "numbers_changed": numbers_changed
        }
        eda_pairs.append(enriched_pair)

    sims = [p["similarity"] for p in eda_pairs]
    print(f"Average Similarity: {np.mean(sims):.4f}")
    print(f"Min Similarity: {np.min(sims):.4f}")
    print(f"Pairs with numbers changed: {sum(1 for p in eda_pairs if p['numbers_changed'])}")

    with open("data/processed/eda_pairs.json", "w") as f:
        json.dump(eda_pairs, f, indent=2)

    print("✅ Saved to data/processed/eda_pairs.json")

if __name__ == "__main__":
    compute_eda()