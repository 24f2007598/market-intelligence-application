import pickle
import numpy as np

def load_model():
    with open("models/change_classifier.pkl", "rb") as f:
        return pickle.load(f)

model = None

def predict_change(old_text, new_text):
    global model
    if model is None:
        try:
            model = load_model()
        except FileNotFoundError:
            return {"change_type": "unknown", "confidence": 0.0}
        
    diff = model.get_diff_vector(old_text, new_text)
    
    pred_probs = model.classifier.predict_proba([diff])[0]
    pred_label = int(np.argmax(pred_probs))
    confidence = float(np.max(pred_probs))
    
    label_map = {0: "no_change", 1: "pricing_change", 2: "feature_change", 3: "messaging_change"}
    
    return {
        "change_type": label_map.get(pred_label, "unknown"),
        "confidence": confidence
    }
