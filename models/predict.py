"""Simulation de rendement a partir des informations que l'agriculteur connait.

L'utilisateur ne renseigne que cinq choses : sa region, sa culture, sa surface,
son engrais et son mode d'irrigation. Toutes les autres variables du modele
(meteo, sol, cycle, pression ravageurs) sont completees avec les valeurs
typiques de sa region, calculees lors de l'entrainement.
"""

import os
import pickle

from utils.preprocessing import preprocess_single
from utils.referentiel import COORDONNEES, VARIETES_DEFAUT, valider

CHEMIN_MODELE = "models/yield_model.pkl"

# Un sac standard de recolte pese 50 kg, soit 20 sacs par tonne.
SACS_PAR_TONNE = 20

_cache = {}


def load_model():
    """Charge le modele entraine, ou None si l'artefact est absent."""
    if "bundle" in _cache:
        return _cache["bundle"]
    if not os.path.exists(CHEMIN_MODELE):
        return None
    with open(CHEMIN_MODELE, "rb") as f:
        bundle = pickle.load(f)
    _cache["bundle"] = bundle
    return bundle


def _bundle_requis():
    bundle = load_model()
    if bundle is None:
        raise FileNotFoundError(
            f"Modele introuvable : {CHEMIN_MODELE}. Lancez : python -m models.train_model"
        )
    return bundle


def get_model_info():
    """Version, commit et empreinte des donnees du modele charge."""
    bundle = load_model()
    if bundle is None:
        return {}
    return {
        "version": bundle.get("version", "inconnue"),
        "commit": bundle.get("commit", "inconnu"),
        "empreinte_donnees": bundle.get("empreinte_donnees"),
    }


def get_model_metrics():
    """Metriques mesurees sur le jeu de test lors de l'entrainement."""
    bundle = load_model()
    return bundle.get("metrics", {}) if bundle else {}


def predict_yield(region, crop, fertilizer_kg_ha=0, irrigation_type="Pluviale", **remplacements):
    """Rendement predit en t/ha.

    Les valeurs categorielles sont validees avant tout calcul : une region ou une
    culture inconnue leve ValueError au lieu de produire un chiffre faux.
    Les variables non renseignees prennent la valeur typique de la region.
    """
    region = valider("region", region)
    crop = valider("crop", crop)
    irrigation_type = valider("irrigation_type", irrigation_type)

    bundle = _bundle_requis()
    defauts = bundle["defauts"]
    typiques = defauts["par_region"][region]
    lat, lon, elev = COORDONNEES[region]

    temp = typiques["temp_avg_c"]
    ndvi = typiques["ndvi_avg"]

    ligne = {
        "year": 2022,
        "latitude": lat, "longitude": lon, "elevation_m": elev,
        "rainfall_mm": typiques["rainfall_mm"],
        "temp_avg_c": temp, "temp_min_c": temp - 5.5, "temp_max_c": temp + 6.5,
        "humidity_pct": typiques["humidity_pct"],
        "wind_speed_ms": typiques["wind_speed_ms"],
        "sunshine_hours": typiques["sunshine_hours"],
        "ndvi_avg": ndvi, "ndvi_min": ndvi - 0.10, "ndvi_max": ndvi + 0.08,
        "soil_ph": typiques["soil_ph"],
        "soil_type": typiques["soil_type"],
        "cycle_days": defauts["cycle_par_culture"][crop],
        "pest_pressure": defauts["pest_pressure"],
        "area_ha": 1.0,
        "fertilizer_kg_ha": fertilizer_kg_ha,
        "region": region, "crop": crop,
        "irrigation_type": irrigation_type,
        "variety": VARIETES_DEFAUT[crop],
    }
    ligne.update(remplacements)

    if "soil_type" in remplacements:
        ligne["soil_type"] = valider("soil_type", remplacements["soil_type"])

    X = preprocess_single(ligne, bundle["encoder"])
    return round(float(bundle["model"].predict(X)[0]), 2)


def simulate(region, crop, surface_ha=1.0, fertilizer_kg_ha=0, irrigation_type="Pluviale"):
    """Simulation complete, telle qu'elle est presentee a l'agriculteur.

    Renvoie le rendement, sa fourchette, la recolte totale attendue sur la
    surface declaree, et le rendement qu'il obtiendrait sans engrais.
    """
    rendement = predict_yield(region, crop, fertilizer_kg_ha, irrigation_type)
    marge = 1.96 * get_model_metrics().get("rmse", 0.18)
    recolte = rendement * surface_ha

    return {
        "rendement_t_ha": rendement,
        "fourchette_t_ha": (round(max(0, rendement - marge), 2), round(rendement + marge, 2)),
        "recolte_t": round(recolte, 2),
        "recolte_sacs": int(round(recolte * SACS_PAR_TONNE)),
        "rendement_sans_engrais": predict_yield(region, crop, 0, irrigation_type),
        "surface_ha": surface_ha,
    }


def get_feature_importances(top_n=10):
    """Variables les plus influentes du modele, par gain decroissant."""
    bundle = load_model()
    if not bundle:
        return []
    noms = bundle.get("feature_names", [])
    if not noms:
        return []
    paires = sorted(zip(noms, bundle["model"].feature_importances_),
                    key=lambda kv: kv[1], reverse=True)
    return [(nom, round(float(v), 4)) for nom, v in paires[:top_n]]
