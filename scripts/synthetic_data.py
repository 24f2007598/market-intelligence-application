import json
import random
from datetime import datetime, timedelta

brands = ["samsung", "oppo"]

texts = [
    "Flagship smartphone priced at ₹{price} with premium camera and performance features.",
    "Mid-range device available at ₹{price} offering great battery life and display.",
    "Special offer: cashback up to ₹{discount} with exchange benefits.",
    "AI-powered camera and fast charging make this device highly competitive.",
    "Strong focus on design, performance, and user experience."
]

urls = {
    "samsung": [
        "https://www.samsung.com/in/smartphones/",
        "https://www.samsung.com/in/offer/"
    ],
    "oppo": [
        "https://www.oppo.com/in/smartphones/",
        "https://www.oppo.com/in/offers/"
    ]
}

data = []

base_date = datetime(2024, 1, 1)

for i in range(100):
    brand = random.choice(brands)
    url = random.choice(urls[brand])

    price = random.randint(15000, 120000)
    discount = random.randint(1000, 15000)

    text_template = random.choice(texts)

    text = text_template.format(price=price, discount=discount)

    snapshot = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")

    data.append({
        "brand": brand,
        "url": url,
        "snapshot": snapshot,
        "text": f"{brand.upper()} {text}"
    })

with open("data/raw/wayback.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Generated 100 synthetic records")