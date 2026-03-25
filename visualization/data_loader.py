import pandas as pd
import json
import os
import streamlit as st

@st.cache_data
def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@st.cache_data
def load_csv(filepath):
    if not os.path.exists(filepath):
        return pd.DataFrame()
    return pd.read_csv(filepath)

def get_ml_results():
    return load_json("data/processed/ml_results.json")

def get_pairs():
    return load_json("data/processed/pairs.json")

def get_eda_pairs():
    return load_json("data/processed/eda_pairs.json")

def get_labeled_changes():
    return load_csv("data/labeled_changes.csv")

def get_chunks():
    return load_json("data/processed/chunks.json")
