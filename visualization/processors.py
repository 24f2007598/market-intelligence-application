import pandas as pd
from visualization.data_loader import *

def process_category_distribution():
    results = get_ml_results()
    if not results: return pd.DataFrame()
    df = pd.DataFrame(list(results.values()), columns=["category"])
    return df.groupby("category").size().reset_index(name="count")

def process_change_frequency():
    pairs = get_pairs()
    if not pairs: return pd.DataFrame()
    df = pd.DataFrame(pairs)
    df["date"] = pd.to_datetime(df["timestamp_new"], errors='coerce').dt.strftime('%Y-%m-%d')
    return df.groupby("date").size().reset_index(name="count")

def process_company_activity():
    pairs = get_pairs()
    if not pairs: return pd.DataFrame()
    df = pd.DataFrame(pairs)
    df["company"] = df["url"].apply(lambda x: "samsung" if "samsung" in x else "oppo" if "oppo" in x else "other")
    return df.groupby("company").size().reset_index(name="count")

def process_dataset_balance():
    df = get_labeled_changes()
    if df.empty: return pd.DataFrame()
    label_map = {0: "no_change", 1: "pricing_change", 2: "feature_change", 3: "messaging_change"}
    df["category"] = df["label"].map(label_map)
    return df.groupby("category").size().reset_index(name="count")

def process_semantic_similarity():
    pairs = get_eda_pairs()
    if not pairs: return pd.DataFrame()
    df = pd.DataFrame(pairs)
    if "similarity" not in df.columns: return pd.DataFrame()
    return pd.DataFrame({"similarity": df["similarity"]})

def process_chunk_size():
    chunks = get_chunks()
    if not chunks: return pd.DataFrame()
    lengths = [len(c.get("chunk", "").split()) for c in chunks]
    return pd.DataFrame({"token_length": lengths})
