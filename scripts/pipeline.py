import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SNAPSHOT_DIR = "data/snapshots"
CHUNK_FILE = "data/chunks.json"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# ----------------------------
# STEP 1: SCRAPE
# ----------------------------
def scrape(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)

        html = page.content()
        browser.close()
        return html


# ----------------------------
# STEP 2: CLEAN
# ----------------------------
def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.extract()

    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ----------------------------
# STEP 3: CHUNK
# ----------------------------
def chunk_text(text, chunk_size=120, overlap=30):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


# ----------------------------
# STEP 4: LOAD PREVIOUS SNAPSHOT
# ----------------------------
def load_previous(url):
    filename = os.path.join(SNAPSHOT_DIR, f"{url.replace('/', '_')}.json")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)

    return None


# ----------------------------
# STEP 5: SAVE SNAPSHOT
# ----------------------------
def save_snapshot(url, content):
    filename = os.path.join(SNAPSHOT_DIR, f"{url.replace('/', '_')}.json")

    snapshot = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "content": content
    }

    with open(filename, "w") as f:
        json.dump(snapshot, f, indent=2)

    return snapshot


# ----------------------------
# STEP 6A: PRICE DETECTION
# ----------------------------
def extract_prices(text):
    return re.findall(r"(?:\$|USD|₹)\s?\d+(?:\.\d+)?", text)


def detect_price_changes(old, new):
    old_prices = set(extract_prices(old))
    new_prices = set(extract_prices(new))

    changes = []

    for price in new_prices - old_prices:
        changes.append(f"New price detected: {price}")

    for price in old_prices - new_prices:
        changes.append(f"Price removed: {price}")

    return changes


# ----------------------------
# STEP 6B: MESSAGING DETECTION
# ----------------------------
KEYWORDS = ["AI", "automation", "secure", "fast", "enterprise", "scale", "real-time"]

def detect_messaging_changes(old, new):
    changes = []

    for kw in KEYWORDS:
        if kw.lower() not in old.lower() and kw.lower() in new.lower():
            changes.append(f"New messaging angle detected: {kw}")

    return changes


# ----------------------------
# STEP 6C: FEATURE CHANGES
# ----------------------------
def detect_feature_changes(old, new):
    old_sentences = set(old.split(". "))
    new_sentences = set(new.split(". "))

    added = new_sentences - old_sentences
    removed = old_sentences - new_sentences

    changes = []

    for a in list(added)[:3]:
        changes.append(f"New feature/content: {a[:100]}")

    for r in list(removed)[:3]:
        changes.append(f"Removed content: {r[:100]}")

    return changes


# ----------------------------
# STEP 7: MAIN PROCESS
# ----------------------------
def process_url(url):
    print(f"Processing: {url}")

    html = scrape(url)
    cleaned = clean_html(html)

    prev = load_previous(url)

    price_changes = []
    messaging_changes = []
    feature_changes = []

    if prev:
        price_changes = detect_price_changes(prev["content"], cleaned)
        messaging_changes = detect_messaging_changes(prev["content"], cleaned)
        feature_changes = detect_feature_changes(prev["content"], cleaned)

    snapshot = save_snapshot(url, cleaned)

    # chunking
    chunks = chunk_text(cleaned)

    chunk_data = []
    for i, chunk in enumerate(chunks):
        chunk_data.append({
            "url": url,
            "timestamp": snapshot["timestamp"],
            "chunk_id": f"{url}_{i}",
            "text": chunk
        })

    # append to chunks file
    if os.path.exists(CHUNK_FILE):
        with open(CHUNK_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(chunk_data)

    with open(CHUNK_FILE, "w") as f:
        json.dump(existing, f, indent=2)

    return {
        "url": url,
        "timestamp": snapshot["timestamp"],
        "changes": {
            "price_changes": price_changes,
            "messaging_changes": messaging_changes,
            "feature_changes": feature_changes
        },
        "summary": f"{len(price_changes)} price, {len(messaging_changes)} messaging, {len(feature_changes)} feature changes detected"
    }


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    urls = [
        "https://stripe.com/pricing",
        "https://www.shopify.com/pricing",
        "https://openai.com/api/pricing"
    ]

    results = []

    for url in urls:
        result = process_url(url)
        results.append(result)

    print(json.dumps(results, indent=2))