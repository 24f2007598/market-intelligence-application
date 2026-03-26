import random
import json
from datetime import datetime, timedelta
import uuid

# -----------------------------
# CONFIG
# -----------------------------
PRODUCTS = ["Samsung", "Oppo", "Apple", "OnePlus"]
URLS = [
    "https://www.samsung.com/pricing",
    "https://www.oppo.com/pricing",
    "https://www.apple.com/iphone",
    "https://www.oneplus.com/store"
]

CHANGE_TYPES = ["no_change", "pricing_change", "feature_change", "messaging_change"]

POSITIVE_TEMPLATES = [
    "The battery life is excellent and lasts all day",
    "Amazing camera quality, very sharp images",
    "Great value for money, highly recommend",
    "Smooth performance and fast UI",
    "Build quality feels premium and solid"
]

NEGATIVE_TEMPLATES = [
    "Battery drains too quickly",
    "Overpriced for the features offered",
    "Camera performance is disappointing",
    "UI is laggy and slow sometimes",
    "Not worth the price"
]

NEUTRAL_TEMPLATES = [
    "The phone works as expected",
    "Average performance overall",
    "Nothing exceptional but decent",
    "Standard features, nothing new",
]

FEATURES = [
    "AI camera enhancement",
    "Battery optimization",
    "Fast charging",
    "New UI design",
    "Security updates"
]

# -----------------------------
# HELPERS
# -----------------------------
def random_date():
    return datetime.now() - timedelta(days=random.randint(0, 30))

def generate_review_text(sentiment):
    if sentiment == "positive":
        base = random.choice(POSITIVE_TEMPLATES)
        return f"{base}. I really like this {random.choice(['phone', 'device'])}."
    elif sentiment == "negative":
        base = random.choice(NEGATIVE_TEMPLATES)
        return f"{base}. I regret buying this."
    else:
        base = random.choice(NEUTRAL_TEMPLATES)
        return f"{base}."

def generate_sentiment():
    return random.choices(
        ["positive", "negative", "neutral"],
        weights=[0.4, 0.3, 0.3]
    )[0]

# -----------------------------
# 1. GENERATE REVIEWS DATA
# -----------------------------
def generate_reviews(n=300):
    reviews = []

    for i in range(n):
        sentiment = generate_sentiment()
        rating = {
            "positive": random.randint(4, 5),
            "neutral": random.randint(2, 3),
            "negative": random.randint(1, 2)
        }[sentiment]

        reviews.append({
            "id": str(uuid.uuid4()),
            "product": random.choice(PRODUCTS),
            "review_text": generate_review_text(sentiment),
            "rating": rating,
            "sentiment_label": sentiment,
            "timestamp": random_date().isoformat()
        })

    return reviews

# -----------------------------
# 2. GENERATE CHANGE DATA
# -----------------------------
def generate_change_text(change_type):
    if change_type == "pricing_change":
        old_price = random.randint(500, 1000)
        new_price = old_price + random.randint(50, 200)
        return (
            f"Price is ${old_price}",
            f"Price updated to ${new_price}"
        )

    elif change_type == "feature_change":
        feature = random.choice(FEATURES)
        return (
            "This phone includes standard features",
            f"New feature added: {feature}"
        )

    elif change_type == "messaging_change":
        return (
            "Best phone for everyone",
            "The ultimate flagship experience for professionals"
        )

    else:
        text = "This is a product page with basic details"
        return (text, text)

def generate_changes(n=200):
    changes = []

    for _ in range(n):
        change_type = random.choice(CHANGE_TYPES)
        old_text, new_text = generate_change_text(change_type)

        changes.append({
            "url": random.choice(URLS),
            "old_text": old_text,
            "new_text": new_text,
            "change_type": change_type,
            "timestamp": random_date().isoformat()
        })

    return changes

# -----------------------------
# 3. GENERATE VECTOR DB CHUNKS
# -----------------------------
def generate_chunks(changes):
    chunks = []

    for change in changes:
        chunks.append({
            "text": change["new_text"],
            "metadata": {
                "url": change["url"],
                "timestamp": change["timestamp"],
                "change_type": change["change_type"]
            }
        })

    return chunks

# -----------------------------
# MAIN
# -----------------------------
def main():
    reviews = generate_reviews(300)
    changes = generate_changes(200)
    chunks = generate_chunks(changes)

    # Save files
    with open("data/processed/synthetic_reviews.json", "w") as f:
        json.dump(reviews, f, indent=2)

    with open("data/processed/synthetic_changes.json", "w") as f:
        json.dump(changes, f, indent=2)

    with open("data/processed/synthetic_chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)

    print("Synthetic data generated successfully!")

if __name__ == "__main__":
    main()