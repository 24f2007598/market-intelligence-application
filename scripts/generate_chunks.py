import json
import random

brands = ["samsung", "oppo"]

chunks = []

templates = [
    "{brand} flagship smartphone priced at ₹{price} with premium camera, AMOLED display, and Snapdragon processor. Offers include cashback up to ₹{discount} and exchange bonuses.",
    "{brand} mid-range device at ₹{price} featuring long battery life, fast charging, and sleek design. Popular among young users.",
    "{brand} introduces AI-powered photography and improved night mode. Pricing starts at ₹{price} with EMI options available.",
    "{brand} festive sale includes discount of ₹{discount} and bundled accessories. Strong competition in pricing segment.",
    "{brand} focuses on camera innovation and performance. Device priced at ₹{price} with premium features and modern UI.",
    "{brand} offers fast charging technology and stylish design. Competitive pricing at ₹{price} attracts mid-range buyers.",
    "{brand} premium lineup includes flagship devices with cutting-edge hardware priced at ₹{price}.",
    "{brand} smartphones emphasize battery optimization and smooth performance at ₹{price}.",
    "{brand} marketing highlights camera quality and design aesthetics. Pricing around ₹{price} with seasonal offers.",
    "{brand} product strategy targets both premium and budget segments with prices ranging near ₹{price}."
]

for i in range(100):
    brand = random.choice(brands)
    price = random.randint(15000, 120000)
    discount = random.randint(1000, 15000)

    template = random.choice(templates)

    chunk_text = template.format(
        brand=brand.capitalize(),
        price=price,
        discount=discount
    )

    chunks.append({
        "brand": brand,
        "chunk": chunk_text
    })

with open("data/processed/chunks.json", "w") as f:
    json.dump(chunks, f, indent=2)

print(f"✅ Generated {len(chunks)} chunks directly")