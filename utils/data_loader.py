import os

import pandas as pd

CHEMIN_DONNEES = "data/raw/senegal_yield_data.csv"


def load_data():
    """Charge le jeu de donnees principal."""
    if not os.path.exists(CHEMIN_DONNEES):
        raise FileNotFoundError(
            f"Jeu de donnees introuvable : {CHEMIN_DONNEES}. "
            "Lancez : python data/pipelines/build_final_dataset.py"
        )
    return pd.read_csv(CHEMIN_DONNEES, encoding="utf-8")


def empreinte_donnees():
    """Empreinte SHA256 du jeu de donnees, ou None si elle n'a pas ete produite."""
    chemin = CHEMIN_DONNEES.replace(".csv", ".sha256")
    if not os.path.exists(chemin):
        return None
    with open(chemin) as f:
        return f.read().strip()
