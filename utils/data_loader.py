import pandas as pd
import os


def load_data():
    """Charge le dataset principal depuis data/raw/ et retourne un DataFrame."""
    path = "data/raw/senegal_yield_data.csv"
    if not os.path.exists(path):
        path = "data/raw/sample_yield_data.csv"
    if not os.path.exists(path):
        raise FileNotFoundError("Dataset introuvable. Lancez : python data/pipelines/generate_dataset.py")
    return pd.read_csv(path, encoding="utf-8")