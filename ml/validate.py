import pandas as pd
import numpy as np
from ml.predict import predict_change
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def validate():
    df = pd.read_csv("data/labeled_changes.csv")
    if len(df) == 0:
        print("No validation data.")
        return
        
    y_true = df["label"].values
    y_pred = []
    
    label_map_inv = {"no_change": 0, "pricing_change": 1, "feature_change": 2, "messaging_change": 3}
    
    print("Running predictions on validation set...")
    for _, row in df.iterrows():
        res = predict_change(row["old_text"], row["new_text"])
        y_pred.append(label_map_inv[res["change_type"]])
        
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    
    print("="*40)
    print(f"Validation Accuracy: {acc:.4f}")
    print("="*40)
    print("Confusion Matrix:")
    print(cm)
    print("="*40)
    print("Sample Predictions:")
    
    samples = df.sample(min(5, len(df)))
    for _, row in samples.iterrows():
        res = predict_change(row["old_text"], row["new_text"])
        print(f"\nOld: {row['old_text'][:50]}...")
        print(f"New: {row['new_text'][:50]}...")
        print(f"True Label: {row['label']} | Predicted: {res['change_type']} (Conf: {res['confidence']:.2f})")

if __name__ == "__main__":
    validate()
