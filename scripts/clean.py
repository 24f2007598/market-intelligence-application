import json
import re

def clean_text(t):
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def run():
    with open("data/raw/wayback.json") as f:
        docs = json.load(f)

    cleaned = []

    for d in docs:
        # ✅ handle missing text safely
        raw_text = d.get("text", "")

        if not raw_text:
            continue

        cleaned.append({
            "brand": d["brand"],
            "url": d["url"],
            "snapshot": d["snapshot"],
            "cleaned_text": clean_text(raw_text)
        })

    with open("data/processed/cleaned_docs.json", "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Cleaned {len(cleaned)} documents")


if __name__ == "__main__":
    run()

# import json
# import re

# def clean_text(t):
#     t = re.sub(r"\s+", " ", t)
#     return t.strip()

# def run():
#     with open("data/raw/wayback.json") as f:
#         docs = json.load(f)

#     cleaned = []

#     for d in docs:
#         cleaned.append({
#             **d,
#             "cleaned_text": clean_text(d["text"])
#         })

#     with open("data/processed/cleaned_docs.json", "w") as f:
#         json.dump(cleaned, f, indent=2)

# if __name__ == "__main__":
#     run()