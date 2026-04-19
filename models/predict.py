import pickle
import os
from utils.preprocessing import preprocess_single

# Cache en memoire pour eviter de recharger le fichier .pkl a chaque prediction
_cache = {}


def load_model():
    """Charge le modele depuis le fichier .pkl (avec cache en memoire)."""
    if "bundle" in _cache:
        return _cache["bundle"]
    path = "models/yield_model.pkl"
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        bundle = pickle.load(f)
    # Compatibilite avec l'ancien format (tuple) si modele regenere manuellement
    if isinstance(bundle, tuple):
        model, encoder = bundle
        bundle = {"model": model, "encoder": encoder, "metrics": {}, "feature_names": []}
    _cache["bundle"] = bundle
    return bundle


def _fallback(crop, rainfall_mm, ndvi_avg):
    """Estimation heuristique si le modele n'est pas disponible."""
    base = {"Arachide": 1.20, "Mil": 0.90, "Mais": 2.00, "Riz": 3.50, "Sorgho": 1.10}
    c = base.get(crop, 1.2)
    adj = 0.0006 * (rainfall_mm - 600) + 0.8 * (ndvi_avg - 0.55)
    return round(max(0.2, c + adj), 2)


def predict_yield(region, crop, rainfall_mm, temp_avg_c, ndvi_avg,
                  soil_type="Sableux", fertilizer_kg_ha=50,
                  irrigation_type="Pluviale", variety=None,
                  humidity_pct=62, wind_speed_ms=3.0, sunshine_hours=8.0,
                  soil_ph=6.2, pest_pressure=0.10, area_ha=1.0,
                  cycle_days=100, year=2024):
    """Predit le rendement (t/ha) pour une region, une culture et des conditions donnees."""
    bundle = load_model()
    if bundle is None:
        return _fallback(crop, rainfall_mm, ndvi_avg)

    model   = bundle["model"]
    encoder = bundle["encoder"]

    # Variete locale par defaut si non specifiee
    default_variety = {
        "Arachide": "55-437", "Mil": "Souna III", "Mais": "DK 8031",
        "Riz": "Sahel 108", "Sorgho": "CE 145-66"
    }
    variety = variety or default_variety.get(crop, "Local")

    # Coordonnees GPS et altitude de chaque region (utilisees comme features geographiques)
    coords = {
        "Thies": (14.79, -16.93, 70), "Fatick": (14.34, -16.41, 20),
        "Kaolack": (14.15, -16.07, 15), "Saint-Louis": (16.02, -16.49, 5),
        "Kaffrine": (14.10, -15.55, 40), "Tambacounda": (13.77, -13.67, 130),
        "Sedhiou": (12.71, -15.56, 25),
    }
    lat, lon, elev = coords.get(region, (14.5, -15.0, 50))

    row = {
        "year": year, "latitude": lat, "longitude": lon, "elevation_m": elev,
        "rainfall_mm": rainfall_mm, "temp_avg_c": temp_avg_c,
        "temp_min_c": temp_avg_c - 5.5, "temp_max_c": temp_avg_c + 6.5,
        "humidity_pct": humidity_pct, "wind_speed_ms": wind_speed_ms,
        "sunshine_hours": sunshine_hours, "ndvi_avg": ndvi_avg,
        "ndvi_min": ndvi_avg - 0.10, "ndvi_max": ndvi_avg + 0.08,
        "fertilizer_kg_ha": fertilizer_kg_ha, "pest_pressure": pest_pressure,
        "soil_ph": soil_ph, "area_ha": area_ha, "cycle_days": cycle_days,
        "region": region, "crop": crop, "soil_type": soil_type,
        "irrigation_type": irrigation_type, "variety": variety,
    }

    X = preprocess_single(row, encoder)
    return round(float(model.predict(X)[0]), 2)


def get_model_metrics():
    bundle = load_model()
    return bundle.get("metrics", {}) if bundle else {}


def predict_interval(region, crop, rainfall_mm, temp_avg_c, ndvi_avg,
                     soil_type="Sableux", fertilizer_kg_ha=50,
                     irrigation_type="Pluviale", **kwargs):
    """Retourne la prediction et l'intervalle de confiance a 95% (pred +/- 1.96 * RMSE)."""
    pred = predict_yield(region, crop, rainfall_mm, temp_avg_c, ndvi_avg,
                         soil_type, fertilizer_kg_ha, irrigation_type, **kwargs)
    metrics = get_model_metrics()
    rmse = metrics.get("rmse", 0.18)
    return pred, round(max(0, pred - 1.96 * rmse), 2), round(pred + 1.96 * rmse, 2)


def get_feature_importances(top_n=10):
    bundle = load_model()
    if not bundle:
        return []
    model = bundle["model"]
    names = bundle.get("feature_names", [])
    if not names:
        return []
    pairs = sorted(zip(names, model.feature_importances_), key=lambda x: x[1], reverse=True)
    return [(n, round(float(v), 4)) for n, v in pairs[:top_n]]
