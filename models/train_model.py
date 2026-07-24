"""Entrainement du modele de simulation de rendement.

Deux choix de protocole importants, expliques dans le cahier des charges :

1. Le decoupage est fait par groupe (annee, region, culture). Les 8 parcelles
   d'un meme groupe partagent la meme meteo et le meme rendement national de
   depart : les laisser a cheval sur l'entrainement et le test gonflerait
   artificiellement les metriques.

2. L'arret anticipe se base sur un jeu de validation distinct du jeu de test.
   Utiliser le test pour choisir le nombre d'arbres reviendrait a ne plus avoir
   de jeu de test du tout.
"""

import os
import pickle
import subprocess

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit

from utils.data_loader import empreinte_donnees
from utils.preprocessing import preprocess_data

VERSION_MODELE = "2.0.0"
CHEMIN_SORTIE = "models/yield_model.pkl"


def _commit_courant():
    """Identifiant du commit, pour pouvoir reconstruire ce modele plus tard.

    Dans une image Docker le depot git est absent : le commit est alors fourni
    par la variable d'environnement AGROPREDICT_COMMIT au moment du build.
    """
    depuis_env = os.environ.get("AGROPREDICT_COMMIT")
    if depuis_env:
        return depuis_env.strip()[:7]
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "inconnu"


def _decouper_par_groupe(X, y, groupes, part_test, graine=42):
    """Separe X et y en gardant chaque groupe entierement d'un seul cote."""
    separateur = GroupShuffleSplit(n_splits=1, test_size=part_test, random_state=graine)
    idx_a, idx_b = next(separateur.split(X, y, groups=groupes))
    return idx_a, idx_b


def train_yield_model(data_path="data/raw/senegal_yield_data.csv"):
    """Entraine le modele et enregistre un artefact complet et trecable."""
    df = pd.read_csv(data_path)
    print(f"Jeu de donnees : {len(df)} lignes x {len(df.columns)} colonnes")

    X, y, encoder = preprocess_data(df)

    # Un groupe = une combinaison annee/region/culture.
    groupes = df["year"].astype(str) + "_" + df["region"] + "_" + df["crop"]

    idx_reste, idx_test = _decouper_par_groupe(X, y, groupes, part_test=0.20)
    X_reste, y_reste = X.iloc[idx_reste], y.iloc[idx_reste]
    X_test, y_test = X.iloc[idx_test], y.iloc[idx_test]
    groupes_reste = groupes.iloc[idx_reste]

    idx_train, idx_val = _decouper_par_groupe(X_reste, y_reste, groupes_reste, part_test=0.20)
    X_train, y_train = X_reste.iloc[idx_train], y_reste.iloc[idx_train]
    X_val, y_val = X_reste.iloc[idx_val], y_reste.iloc[idx_val]

    print(f"Entrainement {len(X_train)} | Validation {len(X_val)} | Test {len(X_test)}")

    model = xgb.XGBRegressor(
        n_estimators=600,
        learning_rate=0.04,
        max_depth=7,
        subsample=0.85,
        colsample_bytree=0.80,
        min_child_weight=3,
        reg_alpha=0.1,
        reg_lambda=1.5,
        random_state=42,
        eval_metric="rmse",
        early_stopping_rounds=40,
    )
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

    # Les metriques sont mesurees sur le jeu de test, jamais vu pendant
    # l'entrainement ni pendant le choix du nombre d'arbres.
    y_pred = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae = float(mean_absolute_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))

    importances = dict(zip(X.columns, model.feature_importances_))
    top5 = sorted(importances.items(), key=lambda kv: kv[1], reverse=True)[:5]

    metrics = {
        "rmse": round(rmse, 4),
        "mae": round(mae, 4),
        "r2": round(r2, 4),
        "n_samples": len(df),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "n_features": X.shape[1],
        "top_features": [{"name": k, "importance": round(float(v), 4)} for k, v in top5],
        "best_iteration": int(model.best_iteration),
    }

    # Valeurs par defaut des variables que l'agriculteur ne renseigne pas.
    # Elles sont calculees sur les donnees plutot qu'ecrites en dur, pour rester
    # coherentes avec le jeu d'entrainement.
    defauts = _calculer_defauts(df)

    bundle = {
        "version": VERSION_MODELE,
        "commit": _commit_courant(),
        "empreinte_donnees": empreinte_donnees(),
        "model": model,
        "encoder": encoder,
        "metrics": metrics,
        "feature_names": list(X.columns),
        "defauts": defauts,
    }

    with open(CHEMIN_SORTIE, "wb") as f:
        pickle.dump(bundle, f)

    print(f"Modele v{VERSION_MODELE} | R2={r2:.4f} | RMSE={rmse:.4f} t/ha | MAE={mae:.4f}")
    print(f"Variables dominantes : {[nom for nom, _ in top5]}")
    return model, encoder, metrics


def _calculer_defauts(df):
    """Valeurs typiques par region et par culture, mediane du jeu de donnees.

    Elles servent a completer les variables que l'utilisateur ne saisit pas :
    meteo, sol, duree de cycle, pression ravageurs.
    """
    par_region = {
        "rainfall_mm": "median", "temp_avg_c": "median", "humidity_pct": "median",
        "wind_speed_ms": "median", "sunshine_hours": "median",
        "ndvi_avg": "median", "soil_ph": "median",
    }
    regions = df.groupby("region").agg(par_region).round(2).to_dict("index")
    sols = df.groupby("region")["soil_type"].agg(lambda s: s.mode().iat[0]).to_dict()
    cycles = df.groupby("crop")["cycle_days"].median().round().astype(int).to_dict()
    ravageurs = float(df["pest_pressure"].median())

    for region, valeurs in regions.items():
        valeurs["soil_type"] = sols[region]

    return {"par_region": regions, "cycle_par_culture": cycles, "pest_pressure": ravageurs}


if __name__ == "__main__":
    train_yield_model()
