import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import pickle
from utils.preprocessing import preprocess_data

def train_yield_model():
    """Entraîne le modèle XGBoost sur les données agricoles du Sénégal."""
    print("Chargement des données...")
    df = pd.read_csv("data/raw/sample_yield_data.csv")
    
    print("Prétraitement des données...")
    X, y, encoder = preprocess_data(df)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Entraînement du modèle XGBoost...")
    model = xgb.XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Évaluation simple
    score = model.score(X_test, y_test)
    print(f"Modèle entraîné ! Score R² sur test : {score:.3f}")
    
    # Sauvegarde
    with open("models/yield_model.pkl", "wb") as f:
        pickle.dump((model, encoder), f)  # on sauvegarde aussi l'encoder
    
    print("Modèle sauvegardé dans models/yield_model.pkl")
    return model