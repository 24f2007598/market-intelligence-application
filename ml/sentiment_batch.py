from ml.sentiment import SentimentAnalyzer
from db.db import get_unlabeled_reviews, update_review_sentiment
import datetime

def process_sentiment_batch(batch_size=100):
    analyzer = SentimentAnalyzer()
    reviews = get_unlabeled_reviews(limit=batch_size)
    
    if not reviews:
        print("✅ No unlabeled reviews found.")
        return 0

    print(f"⚙️ Processing batch of {len(reviews)} reviews...")
    count = 0
    errors = 0

    for r in reviews:
        try:
            label, score = analyzer.predict(r["text"])
            update_review_sentiment(r["id"], label, score)
            count += 1
        except Exception as e:
            print(f"❌ Error processing review {r['id']}: {e}")
            errors += 1

    print(f"✅ Batch complete. Processed: {count}, Errors: {errors}")
    return count
