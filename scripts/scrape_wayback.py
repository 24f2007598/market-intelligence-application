from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from utils.wayback import get_snapshots
from db.db import insert_competitor, insert_page, insert_document
import json
import datetime

TARGETS = {
    "samsung": [
        "https://www.samsung.com/in/smartphones/",
        "https://www.samsung.com/in/offer/"
    ],
    "oppo": [
        "https://www.oppo.com/in/smartphones/",
        "https://www.oppo.com/in/offers/"
    ]
}

def get_page_type(url):
    if "offer" in url:
        return "pricing"
    elif "smartphones" in url:
        return "product"
    return "landing"


def scrape():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for brand, urls in TARGETS.items():
            print(f"\n🔹 Processing {brand}")

            competitor_id = insert_competitor(brand)

            for url in urls:
                snapshots = get_snapshots(url, limit=2)

                if not snapshots:
                    print(f"⚠️ No snapshots for {url}")
                    continue

                for snap in snapshots:
                    page = browser.new_page()

                    try:
                        print(f"⏳ {snap}")

                        page.goto(snap, timeout=30000, wait_until="domcontentloaded")

                        html = page.content()
                        soup = BeautifulSoup(html, "html.parser")
                        text = soup.get_text(separator=" ", strip=True)

                        page_id = insert_page(
                            competitor_id,
                            url,
                            get_page_type(url),
                            datetime.datetime.now()
                        )

                        insert_document(page_id, text, text)

                        results.append({
                            "brand": brand,
                            "url": url,
                            "snapshot": snap
                        })

                        print(f"✅ Stored in DB")

                    except Exception as e:
                        print(f"❌ Failed: {e}")

                    finally:
                        page.close()

        browser.close()

    with open("data/raw/wayback.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n🎉 Done. Records: {len(results)}")


if __name__ == "__main__":
    scrape()




# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
# from utils.wayback import get_snapshots
# import json

# print("🚀 Script started")

# TARGETS = {
#     "samsung": [
#         "https://www.samsung.com/in/smartphones/",
#         "https://www.samsung.com/in/offer/"
#     ],
#     "oppo": [
#         "https://www.oppo.com/in/smartphones/",
#         "https://www.oppo.com/in/offers/"
#     ]
# }

# def scrape():
#     results = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)

#         for brand, urls in TARGETS.items():
#             for url in urls:
#                 snapshots = get_snapshots(url)

#                 if not snapshots:
#                     print(f"⚠️ No snapshots for {url}")
#                     continue

#                 for snap in snapshots:
#                     page = browser.new_page()

#                     try:
#                         print(f"⏳ Loading: {snap}")

#                         page.goto(snap, timeout=30000, wait_until="domcontentloaded")

#                         html = page.content()
#                         soup = BeautifulSoup(html, "html.parser")
#                         text = soup.get_text(separator=" ", strip=True)

#                         results.append({
#                             "brand": brand,
#                             "url": url,
#                             "snapshot": snap,
#                             "text": text
#                         })

#                         print(f"✅ Scraped: {snap}")

#                         # SAVE PROGRESS (important)
#                         with open("data/raw/wayback.json", "w") as f:
#                             json.dump(results, f, indent=2)

#                     except Exception as e:
#                         print(f"❌ Failed: {snap} -> {e}")

#                     finally:
#                         page.close()

#         browser.close()

#     print(f"🎉 Done. Total records: {len(results)}")
    
# if __name__ == "__main__":
#     scrape()