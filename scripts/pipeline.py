import os

def run():
    print("Step 1: Scraping Wayback...")
    os.system("python scripts/scrape_wayback.py")

    print("Step 2: Scraping Gartner...")
    os.system("python scripts/scrape_gartner.py")

    print("Step 3: Cleaning...")
    os.system("python scripts/clean.py")

    print("Step 4: Chunking...")
    os.system("python scripts/chunk.py")

    print("Step 5: Embedding + Qdrant...")
    os.system("python scripts/embed_store.py")

    print("Pipeline Complete.")

if __name__ == "__main__":
    run()