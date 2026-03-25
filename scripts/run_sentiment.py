from ml.sentiment_batch import process_sentiment_batch
import os
import json
import datetime

def run():
    print("🚀 Starting Sentiment Analysis Runner...")
    total_processed = 0
    
    while True:
        processed = process_sentiment_batch(batch_size=100)
        if processed == 0:
            break
        total_processed += processed

    print(f"🎉 Pipeline finished. Total reviews classified: {total_processed}")

    # Logging
    os.makedirs("data/logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "sentiment_analysis",
        "processed_count": total_processed
    }
    with open("data/logs/sentiment.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    run()
