import json
from collections import defaultdict
import os

def run():
    if not os.path.exists("data/processed/cleaned_docs.json"):
        print("clean_docs.json not found! Run scripts/clean.py first.")
        return

    with open("data/processed/cleaned_docs.json", "r") as f:
        docs = json.load(f)

    by_url = defaultdict(list)
    for d in docs:
        by_url[d["url"]].append(d)

    pairs = []

    for url, group in by_url.items():
        # Sort chronologically
        group.sort(key=lambda x: str(x.get("snapshot", "")))

        for i in range(len(group) - 1):
            old_doc = group[i]
            new_doc = group[i+1]

            # Only pair if they are different snapshots
            if old_doc["snapshot"] != new_doc["snapshot"]:
                pairs.append({
                    "url": url,
                    "timestamp_old": old_doc["snapshot"],
                    "timestamp_new": new_doc["snapshot"],
                    "old_text": old_doc["cleaned_text"],
                    "new_text": new_doc["cleaned_text"]
                })

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/pairs.json", "w") as f:
        json.dump(pairs, f, indent=2)

    print(f"✅ Generated {len(pairs)} chronological snapshot pairs.")

if __name__ == "__main__":
    run()
