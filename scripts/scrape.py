import requests
from bs4 import BeautifulSoup
import json

urls = [
    "https://stripe.com/pricing",
    "https://www.shopify.com/pricing",
    "https://openai.com/api/pricing"
]

def scrape_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator=" ", strip=True)
        return text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

data = []

for url in urls:
    print(f"Scraping: {url}")
    text = scrape_text(url)
    data.append({
        "url": url,
        "text": text
    })

with open("data/raw_docs.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved to data/raw_docs.json")