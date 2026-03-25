import json
import csv
import random

def prepare_dataset():
    with open("data/processed/auto_labeled.json", "r") as f:
        data = json.load(f)
        
    from collections import defaultdict
    by_label = defaultdict(list)
    
    seen = set()
    for row in data:
        t_hash = (row["old_text"], row["new_text"])
        if t_hash in seen: continue
        seen.add(t_hash)
        
        if len(row["old_text"]) < 10 and len(row["new_text"]) < 10:
            continue
            
        by_label[row["label"]].append(row)
        
    min_size = min([len(v) for v in by_label.values()] + [float('inf')])
    if min_size == 0 or min_size == float('inf'):
        print("Warning: some classes are empty! Using all available data.")
        balanced = [r for group in by_label.values() for r in group]
    else:
        balanced = []
        for v in by_label.values():
            balanced.extend(random.sample(v, min_size))
            
    with open("data/labeled_changes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["old_text", "new_text", "label"])
        for row in balanced:
            writer.writerow([row["old_text"], row["new_text"], row["label"]])
            
    print(f"✅ Prepared final dataset with {len(balanced)} rows.")
    
if __name__ == "__main__":
    prepare_dataset()