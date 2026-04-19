import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
from utils.preprocessing import preprocess_data


def train_yield_model(data_path="data/raw/senegal_yield_data.csv"):
    """Entraine le modele XGBoost et sauvegarde le fichier .pkl."""
    df = pd.read_csv(data_path)
    print(f"Dataset charge : {len(df)} lignes x {len(df.columns)} colonnes")

    # Encodage des variables et separation features / cible
    X, y, encoder = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparametres du modele XGBoost (gradient boosting sur arbres de decision)
    model = xgb.XGBRegressor(
        n_estimators=600,        # nombre d'arbres
        learning_rate=0.04,      # taux d'apprentissage
        max_depth=7,             # profondeur max de chaque arbre
        subsample=0.85,          # fraction des lignes utilisees par arbre
        colsample_bytree=0.80,   # fraction des colonnes utilisees par arbre
        min_child_weight=3,      # regularisation sur les feuilles
        reg_alpha=0.1,           # regularisation L1
        reg_lambda=1.5,          # regularisation L2
        random_state=42,
        eval_metric="rmse",
        early_stopping_rounds=40,  # arret si pas d'amelioration apres 40 iterations
    )

    # Entrainement avec evaluation sur le jeu de test
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )

    # Calcul des metriques de performance
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae  = mean_absolute_error(y_test, y_pred)
    r2   = r2_score(y_test, y_pred)

    # Variables les plus importantes selon le gain moyen
    feat_names = X.columns.tolist()
    importances = dict(zip(feat_names, model.feature_importances_))
    top5 = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:5]

    metrics = {
        "rmse":           round(rmse, 4),
        "mae":            round(mae, 4),
        "r2":             round(r2, 4),
        "n_samples":      len(df),
        "n_features":     X.shape[1],
        "top_features":   [{"name": k, "importance": round(v, 4)} for k, v in top5],
        "best_iteration": model.best_iteration,
    }

    # Sauvegarde du modele, de l'encodeur et des metriques dans un seul fichier
    bundle = {"model": model, "encoder": encoder, "metrics": metrics,
              "feature_names": feat_names}

    with open("models/yield_model.pkl", "wb") as f:
        pickle.dump(bundle, f)

    print(f"Modele entraine | R2={r2:.4f} | RMSE={rmse:.4f} t/ha | MAE={mae:.4f} | N={len(df)} | Features={X.shape[1]}")
    print(f"Top features : {[t[0] for t in top5]}")
    return model, encoder, metrics


if __name__ == "__main__":
    train_yield_model()
