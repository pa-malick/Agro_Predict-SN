"""
Récupère les données météo réelles via NASA POWER API (gratuit, sans clé).
Paramètres : PRECTOTCORR (pluie mm/mois), T2M (température 2m °C)
Source : https://power.larc.nasa.gov/
"""
import requests
import pandas as pd
import time

REGIONS = {
    "Thiès":        {"lat": 14.79, "lon": -16.93},
    "Fatick":       {"lat": 14.34, "lon": -16.41},
    "Kaolack":      {"lat": 14.15, "lon": -16.07},
    "Saint-Louis":  {"lat": 16.02, "lon": -16.49},
    "Kaffrine":     {"lat": 14.10, "lon": -15.55},
    "Tambacounda":  {"lat": 13.77, "lon": -13.67},
    "Sédhiou":      {"lat": 12.71, "lon": -15.56},
}

BASE_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"


def fetch_region(region, lat, lon, start=2005, end=2023):
    params = {
        "parameters": "PRECTOTCORR,T2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON",
        "start": start,
        "end": end,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()["properties"]["parameter"]

    records = []
    for key in data["PRECTOTCORR"]:
        year = int(key[:4])
        month = int(key[4:])
        if month == 13:
            continue
        records.append({
            "region": region,
            "year": year,
            "month": month,
            "rainfall_mm": data["PRECTOTCORR"][key],
            "temp_avg_c": data["T2M"][key],
        })
    return records


def fetch_all(output_path="data/raw/nasa_power_weather.csv"):
    all_records = []
    for region, coords in REGIONS.items():
        print(f"  Fetching {region}...")
        try:
            records = fetch_region(region, coords["lat"], coords["lon"])
            all_records.extend(records)
            time.sleep(1)
        except Exception as e:
            print(f"  Erreur {region}: {e}")

    df = pd.DataFrame(all_records)
    # Agréger par année : pluie totale juin-oct (saison des pluies), temp moyenne annuelle
    saison = df[df["month"].between(6, 10)].groupby(["region", "year"])["rainfall_mm"].sum().reset_index()
    saison.columns = ["region", "year", "rainfall_saison_mm"]
    temp_ann = df.groupby(["region", "year"])["temp_avg_c"].mean().reset_index()
    temp_ann.columns = ["region", "year", "temp_avg_annuel_c"]

    result = saison.merge(temp_ann, on=["region", "year"])
    result.to_csv(output_path, index=False)
    print(f"\nDonnées NASA POWER sauvegardées : {len(result)} lignes → {output_path}")
    return result


if __name__ == "__main__":
    fetch_all()
