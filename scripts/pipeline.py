import os
import sys

def run():
    executable = sys.executable
    print("Step 1: Scraping Wayback...")
    os.system(f"PYTHONPATH=. {executable} scripts/scrape_wayback.py")

    print("Step 2: Scraping Gartner...")
    os.system(f"PYTHONPATH=. {executable} scripts/scrape_gartner.py")

    print("Step 3: Cleaning...")
    os.system(f"PYTHONPATH=. {executable} scripts/clean.py")

    print("Step 3.5: ML Change Classification...")
    os.system(f"PYTHONPATH=. {executable} scripts/run_ml.py")

    print("Step 4: Chunking...")
    os.system(f"PYTHONPATH=. {executable} scripts/chunk.py")

    print("Step 5: Embedding + Qdrant...")
    os.system(f"PYTHONPATH=. {executable} scripts/embed_store.py")

    print("Pipeline Complete.")

if __name__ == "__main__":
    run()