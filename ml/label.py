import json

def get_label(pair):
    sim = pair["similarity"]
    num_changed = pair["numbers_changed"]
    kwd = pair["keyword_diffs"]
    ldiff = abs(pair["length_difference"])
    
    if sim > 0.95 and not num_changed:
        return 0 # no_change
        
    if num_changed or kwd.get("₹", 0) != 0 or kwd.get("price", 0) != 0 or kwd.get("discount", 0) != 0:
        return 1 # pricing_change
        
    if ldiff > 10 or kwd.get("feature", 0) != 0 or kwd.get("camera", 0) != 0 or kwd.get("battery", 0) != 0:
        return 2 # feature_change
        
    return 3 # messaging_change
    
def auto_label():
    with open("data/processed/eda_pairs.json", "r") as f:
        pairs = json.load(f)
        
    labeled = []
    distribution = {0:0, 1:0, 2:0, 3:0}
    
    for p in pairs:
        label = get_label(p)
        distribution[label] += 1
        
        labeled.append({
            "url": p["url"],
            "timestamp_old": p["timestamp_old"],
            "timestamp_new": p["timestamp_new"],
            "old_text": p["old_text"],
            "new_text": p["new_text"],
            "label": label
        })
        
    with open("data/processed/auto_labeled.json", "w") as f:
        json.dump(labeled, f, indent=2)
        
    print(f"✅ Auto-labeled {len(labeled)} pairs.")
    print(f"Distribution: {distribution}")
    
if __name__ == "__main__":
    auto_label()