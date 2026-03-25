import json
import os
from ml.preprocess import run as preprocess_run
from ml.predict import predict_change
from db.db import insert_change

def run():
    print("Running ML Preprocessing...")
    preprocess_run()
    
    pairs_file = "data/processed/pairs.json"
    if not os.path.exists(pairs_file):
        print("No pairs found to process.")
        return
        
    with open(pairs_file, "r") as f:
        pairs = json.load(f)
        
    print(f"Running ML Predictions on {len(pairs)} pairs...")
    
    count = 0
    ml_results = {}
    for p in pairs:
        result = predict_change(p["old_text"], p["new_text"])
        
        insert_change(
            url=p["url"],
            snapshot_date=p["timestamp_new"],
            old_text=p["old_text"],
            new_text=p["new_text"],
            change_type=result["change_type"],
            confidence=result["confidence"]
        )
        key = f"{p['url']}_{p['timestamp_new']}"
        ml_results[key] = result["change_type"]
        count += 1
        
    with open("data/processed/ml_results.json", "w") as f:
        json.dump(ml_results, f, indent=2)
        
    print(f"✅ ML predictions for {count} pairs saved to database changes table and ml_results.json.")

if __name__ == "__main__":
    run()
