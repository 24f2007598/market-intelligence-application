import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

class ChangeClassifier:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.classifier = LogisticRegression(max_iter=1000)
        
    def get_diff_vector(self, old_text, new_text):
        emb_old = self.embedding_model.encode([old_text])[0]
        emb_new = self.embedding_model.encode([new_text])[0]
        return np.abs(emb_new - emb_old)
