from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        # Uses RoBERTa tailored for short-text sentiment
        self.analyzer = pipeline(
            "sentiment-analysis", 
            model="cardiffnlp/twitter-roberta-base-sentiment-latest", 
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
            top_k=None # get all probabilities
        )

    def predict(self, text):
        results = self.analyzer(text[:512]) # safe truncation
        
        best = max(results[0], key=lambda x: x["score"])
        
        label = best["label"].lower()
        score = best["score"]
        
        return label, score
