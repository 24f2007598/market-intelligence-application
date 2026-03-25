import pandas as pd
import numpy as np
import pickle
import os
from ml.model import ChangeClassifier

def train():
    df = pd.read_csv("data/labeled_changes.csv")
    
    if len(df) == 0:
        print("Dataset is empty. Cannot train.")
        return
        
    print(f"Training on {len(df)} samples...")
    model = ChangeClassifier()
    
    X = []
    y = df["label"].values
    
    for _, row in df.iterrows():
        diff = model.get_diff_vector(row["old_text"], row["new_text"])
        X.append(diff)
        
    X = np.array(X)
    
    print("Fitting logistic regression...")
    model.classifier.fit(X, y)
    
    print("Train Accuracy:", model.classifier.score(X, y))
    
    os.makedirs("models", exist_ok=True)
    with open("models/change_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
        
    print("✅ Model trained and saved to models/change_classifier.pkl")

if __name__ == "__main__":
    train()