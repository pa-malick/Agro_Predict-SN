import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


# Variables numeriques utilisees comme features par le modele
NUMERIC_COLS = [
    "year", "latitude", "longitude", "elevation_m",
    "rainfall_mm", "temp_avg_c", "temp_min_c", "temp_max_c",
    "humidity_pct", "wind_speed_ms", "sunshine_hours",
    "ndvi_avg", "ndvi_min", "ndvi_max",
    "fertilizer_kg_ha", "pest_pressure", "soil_ph",
    "area_ha", "cycle_days",
]

# Variables categorielles a encoder en One-Hot
CAT_COLS = ["region", "crop", "soil_type", "irrigation_type", "variety"]


def _safe_numeric(df):
    """Ajoute les colonnes numeriques manquantes avec la valeur 0."""
    missing = [c for c in NUMERIC_COLS if c not in df.columns]
    for c in missing:
        df[c] = 0.0
    return df, NUMERIC_COLS


def preprocess_data(df):
    """Prepare le dataset complet : encodage One-Hot + separation X / y."""
    df = df.copy()
    df, num_cols = _safe_numeric(df)

    available_cats = [c for c in CAT_COLS if c in df.columns]

    # One-Hot Encoding : transforme les categories en colonnes binaires
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded_cat = encoder.fit_transform(df[available_cats])
    encoded_df = pd.DataFrame(
        encoded_cat,
        columns=encoder.get_feature_names_out(available_cats),
        index=df.index,
    )

    X = pd.concat([df[num_cols].reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    y = df["yield_ton_ha"]

    return X, y, encoder


def preprocess_single(row_dict, encoder):
    """Transforme un dictionnaire de parametres en vecteur de features pour la prediction."""
    row = pd.DataFrame([row_dict])

    # Remplir les colonnes numeriques absentes avec 0
    for c in NUMERIC_COLS:
        if c not in row.columns:
            row[c] = 0.0

    available_cats = [c for c in CAT_COLS if c in row.columns]
    encoded = encoder.transform(row[available_cats])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(available_cats))

    X = pd.concat([row[NUMERIC_COLS].reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    return X
