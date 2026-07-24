"""Recupere la meteo reelle par region via l'API NASA POWER (gratuite, sans cle).

Produit data/raw/nasa_power_monthly.json, le fichier consomme par
build_final_dataset.py. Ce script n'a besoin d'etre relance que pour etendre la
periode couverte : le JSON est versionne dans le depot.

Source : https://power.larc.nasa.gov/
"""

import json
import time

import requests

# Noms sans accent : ce sont ceux qu'apprend le modele (voir utils/referentiel.py).
REGIONS = {
    "Thies":       (14.79, -16.93),
    "Fatick":      (14.34, -16.41),
    "Kaolack":     (14.15, -16.07),
    "Saint-Louis": (16.02, -16.49),
    "Kaffrine":    (14.10, -15.55),
    "Tambacounda": (13.77, -13.67),
    "Sedhiou":     (12.71, -15.56),
}

URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"

# Chaque parametre NASA POWER et son nom dans le fichier produit.
PARAMETRES = {
    "PRECTOTCORR":    "rainfall_mm",     # pluie, mm par jour
    "T2M":            "temp_avg_c",      # temperature moyenne a 2 m
    "T2M_MIN":        "temp_min_c",
    "T2M_MAX":        "temp_max_c",
    "RH2M":           "humidity_pct",    # humidite relative
    "WS2M":           "wind_speed_ms",   # vitesse du vent
    "ALLSKY_SFC_SW_DWN": "sunshine_mjm2",  # rayonnement solaire
}

SORTIE = "data/raw/nasa_power_monthly.json"


def recuperer_region(region, lat, lon, debut=2000, fin=2022):
    """Renvoie une ligne par mois pour une region."""
    reponse = requests.get(URL, timeout=60, params={
        "parameters": ",".join(PARAMETRES),
        "community": "AG",
        "latitude": lat,
        "longitude": lon,
        "start": debut,
        "end": fin,
        "format": "JSON",
    })
    reponse.raise_for_status()
    mesures = reponse.json()["properties"]["parameter"]

    lignes = []
    for cle in mesures["PRECTOTCORR"]:
        mois = int(cle[4:])
        if mois == 13:  # l'API ajoute un 13e "mois" qui est la moyenne annuelle
            continue
        ligne = {"region": region, "lat": lat, "lon": lon,
                 "year": int(cle[:4]), "month": mois}
        for parametre, nom in PARAMETRES.items():
            ligne[nom] = round(mesures[parametre][cle], 2)
        lignes.append(ligne)
    return lignes


def main():
    toutes = []
    for region, (lat, lon) in REGIONS.items():
        print(f"  {region}...")
        toutes.extend(recuperer_region(region, lat, lon))
        time.sleep(1)  # courtoisie envers l'API

    with open(SORTIE, "w") as f:
        json.dump(toutes, f)
    print(f"{len(toutes)} lignes mensuelles ecrites dans {SORTIE}")


if __name__ == "__main__":
    main()
