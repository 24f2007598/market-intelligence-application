from playwright.sync_api import sync_playwright
from db.db import insert_review
import json

URL = "https://www.gartner.com/reviews/market/global-smartphones"

def scrape():
    reviews = []
    seen = set()

    def handle_response(response):
        try:
            # ✅ Capture ALL JSON responses
            if "application/json" in response.headers.get("content-type", ""):
                data = response.json()

                # DEBUG (keep this for now)
                print("📡 JSON API:", response.url)

                def extract_text(obj):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if isinstance(v, str):
                                if len(v) > 50:
                                    yield v
                            else:
                                yield from extract_text(v)

                    elif isinstance(obj, list):
                        for item in obj:
                            yield from extract_text(item)

                for text in extract_text(data):
                    if text in seen:
                        continue

                    seen.add(text)

                    insert_review("gartner", "smartphones", text)
                    reviews.append(text)

        except Exception:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("response", handle_response)

        print("⏳ Loading Gartner page...")
        page.goto(URL, timeout=60000, wait_until="domcontentloaded")

        # Trigger API calls
        for i in range(10):
            print(f"🔄 Scrolling {i+1}")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000)

        browser.close()

    with open("data/raw/gartner.json", "w") as f:
        json.dump(reviews, f, indent=2)

    print(f"✅ Stored {len(reviews)} reviews")


if __name__ == "__main__":
    scrape()


# from playwright.sync_api import sync_playwright
# from db.db import insert_review
# import json

# URL = "https://www.gartner.com/reviews/market/global-smartphones"

# def scrape():
#     reviews = []

#     def handle_response(response):
#         try:
#             if "reviews" in response.url and response.status == 200:
#                 data = response.json()

#                 print("📡 API Hit:", response.url)

#                 if isinstance(data, dict):
#                     for key in ["reviews", "data", "results"]:
#                         if key in data:
#                             for r in data[key]:
#                                 text = ""

#                                 if isinstance(r, dict):
#                                     text = (
#                                         r.get("reviewText")
#                                         or r.get("comment")
#                                         or (r.get("pros", "") + " " + r.get("cons", ""))
#                                     )

#                                 if text and len(text) > 20:
#                                     insert_review("gartner", "smartphones", text)
#                                     reviews.append(text)

#         except Exception as e:
#             print("⚠️ Response parse error:", e)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()

#         page.on("response", handle_response)

#         print("⏳ Loading Gartner page...")

#         # ✅ FIXED HERE
#         page.goto(URL, timeout=60000, wait_until="domcontentloaded")

#         # Scroll to trigger API calls
#         for i in range(8):
#             print(f"🔄 Scrolling {i+1}")
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             page.wait_for_timeout(3000)

#         browser.close()

#     with open("data/raw/gartner.json", "w") as f:
#         json.dump(reviews, f, indent=2)

#     print(f"✅ Stored {len(reviews)} reviews")


# if __name__ == "__main__":
#     scrape()



# from playwright.sync_api import sync_playwright
# from db.db import insert_review
# import json

# URL = "https://www.gartner.com/reviews/market/global-smartphones"

# def scrape():
#     reviews = []

#     def handle_response(response):
#         try:
#             # 👇 Gartner API responses contain "reviews"
#             if "reviews" in response.url and response.status == 200:
#                 data = response.json()

#                 # print for debugging once
#                 print("📡 API Hit:", response.url)

#                 if isinstance(data, dict):
#                     # Try common review keys
#                     for key in ["reviews", "data", "results"]:
#                         if key in data:
#                             for r in data[key]:
#                                 text = ""

#                                 # Try extracting review text safely
#                                 if isinstance(r, dict):
#                                     text = (
#                                         r.get("reviewText")
#                                         or r.get("comment")
#                                         or r.get("pros", "") + " " + r.get("cons", "")
#                                     )

#                                 if text and len(text) > 20:
#                                     insert_review("gartner", "smartphones", text)
#                                     reviews.append(text)

#         except Exception as e:
#             print("⚠️ Response parse error:", e)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()

#         # 👇 Listen to ALL network responses
#         page.on("response", handle_response)

#         print("⏳ Loading Gartner page...")
#         page.goto(URL, timeout=60000, wait_until="networkidle")

#         # 👇 Scroll to trigger API calls
#         for i in range(6):
#             print(f"🔄 Scrolling {i+1}")
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             page.wait_for_timeout(3000)

#         browser.close()

#     # Save locally
#     with open("data/raw/gartner.json", "w") as f:
#         json.dump(reviews, f, indent=2)

#     print(f"✅ Stored {len(reviews)} reviews")


# if __name__ == "__main__":
#     scrape()


# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
# from db.db import insert_review
# import json

# URL = "https://www.gartner.com/reviews/market/global-smartphones"

# def scrape():
#     reviews = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()

#         print("⏳ Loading page...")
#         page.goto(URL, timeout=60000, wait_until="domcontentloaded")

#         # 👇 Scroll multiple times to load reviews
#         for i in range(5):
#             print(f"🔄 Scrolling {i+1}")
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             page.wait_for_timeout(3000)

#         html = page.content()
#         soup = BeautifulSoup(html, "html.parser")

#         # 🔍 DEBUG: check if content exists
#         print("Page length:", len(html))

#         # Try multiple selectors (Gartner changes structure often)
#         seen = set()

#         blocks = soup.find_all("p")

#         for b in blocks:
#             text = b.get_text(strip=True)

#             if len(text) < 30:
#                 continue

#             if text in seen:
#                 continue

#             seen.add(text)

#             insert_review("gartner", "smartphones", text)
#             reviews.append(text)

#         browser.close()

#     with open("data/raw/gartner.json", "w") as f:
#         json.dump(reviews, f, indent=2)

#     print(f"✅ Stored {len(reviews)} reviews")


# if __name__ == "__main__":
#     scrape()


# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
# from db.db import insert_review
# import json

# URL = "https://www.gartner.com/reviews/market/global-smartphones"

# def scrape():
#     reviews = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(URL, timeout=30000)

#         html = page.content()
#         soup = BeautifulSoup(html, "html.parser")

#         blocks = soup.select(".review")

#         for b in blocks:
#             text = b.get_text(strip=True)

#             insert_review("gartner", "smartphones", text)

#             reviews.append(text)

#         browser.close()

#     with open("data/raw/gartner.json", "w") as f:
#         json.dump(reviews, f, indent=2)

#     print(f"✅ Stored {len(reviews)} reviews")


# if __name__ == "__main__":
#     scrape()


# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
# import json

# URL = "https://www.gartner.com/reviews/market/global-smartphones"

# def scrape():
#     reviews = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(URL, timeout=60000)

#         html = page.content()
#         soup = BeautifulSoup(html, "html.parser")

#         blocks = soup.select(".review")

#         for b in blocks:
#             text = b.get_text(strip=True)

#             reviews.append({
#                 "source": "gartner",
#                 "text": text
#             })

#         browser.close()

#     with open("data/raw/gartner.json", "w") as f:
#         json.dump(reviews, f, indent=2)

# if __name__ == "__main__":
#     scrape()