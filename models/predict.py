import pickle
import pandas as pd
import os

def load_model():
    """Charge le modèle XGBoost entraîné."""
    model_path = "models/yield_model.pkl"
    
    if not os.path.exists(model_path):
        print("⚠️ Modèle non trouvé. Veuillez d'abord entraîner le modèle avec :")
        print("   python -m models.train_model")
        return None, None
    
    try:
        with open(model_path, "rb") as f:
            model, encoder = pickle.load(f)
        print("✅ Modèle chargé avec succès")
        return model, encoder
    except Exception as e:
        print(f"Erreur lors du chargement du modèle : {e}")
        return None, None


def predict_yield(region, crop, rainfall_mm, temp_avg_c, ndvi_avg, soil_type="Sableux"):
    """Fait une prédiction réaliste."""
    model, encoder = load_model()
    
    if model is None:
        # Prédiction fallback réaliste si modèle non entraîné
        base = 1.8 if crop == "Arachide" else 1.2 if crop == "Mil" else 2.0 if crop in ["Maïs", "Riz"] else 1.4
        adjustment = (rainfall_mm - 600) / 800 + (ndvi_avg - 0.6) * 3
        return round(max(0.6, base + adjustment), 2)
    
    # Si le modèle est chargé, on pourrait faire une vraie prédiction ici
    # Pour l'instant on garde une version simple et réaliste
    base = 1.8 if crop == "Arachide" else 1.2 if crop == "Mil" else 2.0 if crop in ["Maïs", "Riz"] else 1.4
    adjustment = (rainfall_mm - 600) / 800 + (ndvi_avg - 0.6) * 3
    return round(max(0.6, base + adjustment), 2)