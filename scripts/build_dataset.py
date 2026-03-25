import json
import random

# ----------------------------
# STEP 1: Define base companies
# ----------------------------
companies = [
    {
        "name": "Stripe",
        "pricing": "2.9% + 30¢ per transaction",
        "target": "developers, startups, global businesses",
        "messaging": "developer-first, scalable, API-driven payments",
        "features": "payments, subscriptions, billing, global support",
        "positioning": "infrastructure for internet businesses"
    },
    {
        "name": "Shopify",
        "pricing": "starts at $39/month subscription",
        "target": "e-commerce businesses, small merchants",
        "messaging": "easy store setup, all-in-one commerce platform",
        "features": "store builder, themes, payments, logistics",
        "positioning": "entrepreneur-friendly commerce platform"
    },
    {
        "name": "OpenAI",
        "pricing": "usage-based per token",
        "target": "developers, AI startups, enterprises",
        "messaging": "cutting-edge AI, flexible APIs",
        "features": "LLMs, embeddings, APIs, fine-tuning",
        "positioning": "AI platform for building intelligent apps"
    }
]

# ----------------------------
# STEP 2: Generate synthetic data
# ----------------------------
def generate_synthetic_docs(companies, multiplier=5):
    docs = []

    for company in companies:
        for i in range(multiplier):

            docs.append({
                "url": company["name"],
                "text": f"""
                {company['name']} targets {company['target']}.
                Pricing model: {company['pricing']}.
                Messaging focuses on {company['messaging']}.
                Features include {company['features']}.
                Positioned as {company['positioning']}.
                """
            })

            docs.append({
                "url": company["name"],
                "text": f"""
                {company['name']} uses a pricing strategy of {company['pricing']} 
                which appeals to {company['target']}.
                Messaging emphasizes {company['messaging']}.
                """
            })

            docs.append({
                "url": company["name"],
                "text": f"""
                Competitor insight:
                {company['name']} differentiates itself through {company['features']}.
                Its positioning is {company['positioning']}.
                """
            })

            # Add variation (important for better RAG)
            docs.append({
                "url": company["name"],
                "text": f"""
                Analysis: {company['name']} targets {company['target']} 
                and monetizes via {company['pricing']}.
                Potential gap: may not fully address cost-sensitive users.
                """
            })

    return docs


# ----------------------------
# STEP 3: Load scraped data (optional)
# ----------------------------
from typing import Any, List, Dict

def load_scraped() -> List[Dict[str, Any]]:
    try:
        with open("data/raw_docs.json", "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except:
        return []


# ----------------------------
# STEP 4: Combine synthetic + scraped
# ----------------------------
def build_dataset():
    synthetic = generate_synthetic_docs(companies, multiplier=5)

    scraped = load_scraped()  # optional

    # Limit scraped influence (keep it small)
    scraped = scraped[:10]  # type: ignore

    combined = synthetic + scraped

    # shuffle for better distribution
    random.shuffle(combined)

    with open("data/raw_docs.json", "w") as f:
        json.dump(combined, f, indent=2)

    print(f"Dataset ready with {len(combined)} documents")


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    build_dataset()