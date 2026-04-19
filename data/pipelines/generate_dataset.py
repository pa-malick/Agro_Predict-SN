"""
Generation du dataset AgroPredict SN.
Sources calibrees : FAOSTAT, DAPSA, ANSD, NASA POWER, CHIRPS et litterature agronomique senegalaise.
Variables : climatiques, pedologiques, agronomiques, socio-economiques.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

# Caracteristiques climatiques et pedologiques de chaque region
REGIONS = {
    "Thies": {
        "lat": 14.79, "lon": -16.93,
        "rain_base": 540, "rain_std": 110,
        "temp_base": 27.5, "temp_std": 0.8,
        "humidity_base": 62, "wind_base": 3.2,
        "sunshine_base": 7.8,
        "soils": {"Sableux": 0.55, "Sablo-argileux": 0.30, "Argileux": 0.15},
        "ph_range": (5.8, 6.8),
        "elev_m": 70,
    },
    "Fatick": {
        "lat": 14.34, "lon": -16.41,
        "rain_base": 620, "rain_std": 120,
        "temp_base": 27.8, "temp_std": 0.9,
        "humidity_base": 65, "wind_base": 2.8,
        "sunshine_base": 7.6,
        "soils": {"Argileux": 0.40, "Sablo-argileux": 0.35, "Sableux": 0.25},
        "ph_range": (5.5, 6.5),
        "elev_m": 20,
    },
    "Kaolack": {
        "lat": 14.15, "lon": -16.07,
        "rain_base": 660, "rain_std": 130,
        "temp_base": 28.2, "temp_std": 1.0,
        "humidity_base": 60, "wind_base": 3.0,
        "sunshine_base": 8.1,
        "soils": {"Sableux": 0.50, "Sablo-argileux": 0.35, "Dior": 0.15},
        "ph_range": (6.0, 7.0),
        "elev_m": 15,
    },
    "Saint-Louis": {
        "lat": 16.02, "lon": -16.49,
        "rain_base": 310, "rain_std": 80,
        "temp_base": 26.8, "temp_std": 1.2,
        "humidity_base": 55, "wind_base": 4.1,
        "sunshine_base": 8.5,
        "soils": {"Argileux": 0.60, "Limoneux": 0.25, "Sableux": 0.15},
        "ph_range": (6.5, 7.5),
        "elev_m": 5,
    },
    "Kaffrine": {
        "lat": 14.10, "lon": -15.55,
        "rain_base": 700, "rain_std": 140,
        "temp_base": 28.5, "temp_std": 1.1,
        "humidity_base": 58, "wind_base": 2.9,
        "sunshine_base": 8.3,
        "soils": {"Sableux": 0.45, "Dior": 0.30, "Sablo-argileux": 0.25},
        "ph_range": (5.8, 6.8),
        "elev_m": 40,
    },
    "Tambacounda": {
        "lat": 13.77, "lon": -13.67,
        "rain_base": 840, "rain_std": 160,
        "temp_base": 29.0, "temp_std": 1.3,
        "humidity_base": 55, "wind_base": 2.5,
        "sunshine_base": 8.6,
        "soils": {"Laterite": 0.40, "Sablo-argileux": 0.35, "Argileux": 0.25},
        "ph_range": (5.2, 6.5),
        "elev_m": 130,
    },
    "Sedhiou": {
        "lat": 12.71, "lon": -15.56,
        "rain_base": 980, "rain_std": 180,
        "temp_base": 27.2, "temp_std": 0.8,
        "humidity_base": 75, "wind_base": 2.2,
        "sunshine_base": 7.2,
        "soils": {"Argileux": 0.50, "Laterite": 0.30, "Sablo-argileux": 0.20},
        "ph_range": (4.8, 6.2),
        "elev_m": 25,
    },
}

# Caracteristiques agronomiques de chaque culture (rendements, besoins en eau, etc.)
CROPS = {
    "Arachide": {
        "base_yield": 1.35, "max_yield": 3.8,
        "rain_opt": (400, 700), "temp_opt": (25, 30),
        "ndvi_coef": 2.0, "fert_coef": 0.004,
        "cycle_days": (90, 120),
        "varieties": ["55-437", "Fleur 11", "GH 119-20", "TS 32-1", "ICGV 86015"],
        "irrig_types": {"Pluviale": 0.85, "Aspersion": 0.15},
        "ph_opt": (5.8, 6.5),
        "weight_regions": {
            "Thies": 0.22, "Fatick": 0.20, "Kaolack": 0.22,
            "Saint-Louis": 0.05, "Kaffrine": 0.18, "Tambacounda": 0.08, "Sedhiou": 0.05
        },
    },
    "Mil": {
        "base_yield": 0.98, "max_yield": 2.5,
        "rain_opt": (300, 600), "temp_opt": (26, 32),
        "ndvi_coef": 1.5, "fert_coef": 0.003,
        "cycle_days": (75, 105),
        "varieties": ["Souna III", "IBV 8004", "IKMP5", "Thiokho", "Sanio"],
        "irrig_types": {"Pluviale": 0.92, "Aspersion": 0.08},
        "ph_opt": (5.5, 7.0),
        "weight_regions": {
            "Thies": 0.18, "Fatick": 0.16, "Kaolack": 0.18,
            "Saint-Louis": 0.12, "Kaffrine": 0.18, "Tambacounda": 0.12, "Sedhiou": 0.06
        },
    },
    "Mais": {
        "base_yield": 2.40, "max_yield": 6.0,
        "rain_opt": (500, 900), "temp_opt": (22, 28),
        "ndvi_coef": 2.8, "fert_coef": 0.007,
        "cycle_days": (90, 130),
        "varieties": ["DK 8031", "Bastan", "SAMAZ", "EVDT", "Pool 16 DT"],
        "irrig_types": {"Pluviale": 0.70, "Aspersion": 0.20, "Goutte-a-goutte": 0.10},
        "ph_opt": (5.8, 7.0),
        "weight_regions": {
            "Thies": 0.14, "Fatick": 0.13, "Kaolack": 0.13,
            "Saint-Louis": 0.10, "Kaffrine": 0.14, "Tambacounda": 0.18, "Sedhiou": 0.18
        },
    },
    "Riz": {
        "base_yield": 4.20, "max_yield": 8.0,
        "rain_opt": (700, 1200), "temp_opt": (22, 27),
        "ndvi_coef": 2.6, "fert_coef": 0.009,
        "cycle_days": (110, 150),
        "varieties": ["Sahel 108", "CK 4", "Nerica 4", "IR 64", "Wassa"],
        "irrig_types": {"Submersion": 0.45, "Pluviale": 0.35, "Goutte-a-goutte": 0.20},
        "ph_opt": (6.0, 7.0),
        "weight_regions": {
            "Thies": 0.04, "Fatick": 0.10, "Kaolack": 0.07,
            "Saint-Louis": 0.40, "Kaffrine": 0.04, "Tambacounda": 0.12, "Sedhiou": 0.23
        },
    },
    "Sorgho": {
        "base_yield": 1.20, "max_yield": 3.5,
        "rain_opt": (350, 650), "temp_opt": (25, 32),
        "ndvi_coef": 1.7, "fert_coef": 0.003,
        "cycle_days": (100, 140),
        "varieties": ["CE 145-66", "S 35", "IRAT 204", "Framida", "Sariaso 14"],
        "irrig_types": {"Pluviale": 0.90, "Aspersion": 0.10},
        "ph_opt": (5.5, 7.0),
        "weight_regions": {
            "Thies": 0.10, "Fatick": 0.10, "Kaolack": 0.10,
            "Saint-Louis": 0.10, "Kaffrine": 0.18, "Tambacounda": 0.22, "Sedhiou": 0.20
        },
    },
}

YEARS = list(range(2000, 2024))

# Anomalies climatiques historiques : El Nino (secheresse) et La Nina (exces pluie)
EL_NINO_YEARS = {2002: -0.15, 2004: -0.10, 2006: -0.08, 2009: -0.18,
                 2012: -0.12, 2015: -0.20, 2018: -0.10, 2019: -0.15, 2023: -0.12}
LA_NINA_YEARS = {2000: 0.08, 2007: 0.12, 2010: 0.15, 2011: 0.10,
                 2016: 0.12, 2020: 0.14, 2021: 0.10, 2022: 0.08}


def pick_soil(soils):
    names = list(soils.keys())
    probs = list(soils.values())
    return np.random.choice(names, p=probs)


def pick_variety(varieties):
    return np.random.choice(varieties)


def pick_irrigation(irrig_types):
    names = list(irrig_types.keys())
    probs = list(irrig_types.values())
    return np.random.choice(names, p=probs)


def compute_yield(crop_info, region_info, rainfall, temp, ndvi, soil_type, fertilizer,
                  irrigation, ph, pest_pressure, year):
    """Calcule le rendement (t/ha) en appliquant des facteurs multiplicatifs sur le rendement de base."""
    c = crop_info
    r_opt_lo, r_opt_hi = c["rain_opt"]
    t_opt_lo, t_opt_hi = c["temp_opt"]
    ph_lo, ph_hi = c["ph_opt"]

    # L'irrigation compense le deficit pluviometrique
    if irrigation == "Submersion":
        effective_rain = max(rainfall, r_opt_hi * 0.90)
    elif irrigation == "Goutte-a-goutte":
        effective_rain = max(rainfall, r_opt_lo + (r_opt_hi - r_opt_lo) * 0.75)
    elif irrigation == "Aspersion":
        effective_rain = rainfall * 1.25
    else:
        effective_rain = rainfall

    # Facteurs de stress (gaussienne centree sur la valeur optimale)
    rain_center = (r_opt_lo + r_opt_hi) / 2
    rain_factor = 0.45 + 0.55 * np.exp(-0.5 * ((effective_rain - rain_center) / (rain_center * 0.55)) ** 2)

    temp_center = (t_opt_lo + t_opt_hi) / 2
    temp_factor = 0.60 + 0.40 * np.exp(-0.5 * ((temp - temp_center) / 4.5) ** 2)

    ph_center = (ph_lo + ph_hi) / 2
    ph_factor = 0.70 + 0.30 * np.exp(-0.5 * ((ph - ph_center) / 0.9) ** 2)

    # NDVI : indice de verdure satellitaire (proxy de la sante vegetale)
    ndvi_factor = max(0.80, 0.80 + c["ndvi_coef"] * (ndvi - 0.45) * 0.28)

    # Effet engrais avec rendements decroissants (loi de Liebig simplifiee)
    fert_factor = 1.0 + 0.30 * (1 - np.exp(-fertilizer / 80))

    # Perte due aux ravageurs (max 25%)
    pest_penalty = pest_pressure * 0.25

    # Amelioration technologique : +1% par an depuis 2000
    tech_trend = 1 + (year - 2000) * 0.010

    yield_val = (
        c["base_yield"]
        * rain_factor * temp_factor * ph_factor
        * ndvi_factor * fert_factor * tech_trend
        * (1 - pest_penalty)
    )

    return round(np.clip(yield_val, 0.15, c["max_yield"]), 3)


rows = []

for year in YEARS:
    # Anomalie climatique annuelle
    climate_mod = EL_NINO_YEARS.get(year, LA_NINA_YEARS.get(year, 0))
    temp_trend = (year - 2000) * 0.045  # rechauffement +0.045 C/an

    for crop_name, crop_info in CROPS.items():
        w = crop_info["weight_regions"]
        total_obs = np.random.randint(45, 58)  # ~50 obs par culture/an => ~6000 total
        region_choices = np.random.choice(
            list(w.keys()), size=total_obs,
            p=[v/sum(w.values()) for v in w.values()]
        )

        for region_name in region_choices:
            ri = REGIONS[region_name]

            # Climat
            rain_anomaly = np.random.normal(0, ri["rain_std"] * 0.6)
            rainfall = max(100, ri["rain_base"] * (1 + climate_mod * 0.8) + rain_anomaly)
            temp = ri["temp_base"] + temp_trend + np.random.normal(0, ri["temp_std"])
            temp_min = temp - np.random.uniform(4, 8)
            temp_max = temp + np.random.uniform(4, 9)
            humidity = np.clip(ri["humidity_base"] + (rainfall - ri["rain_base"]) * 0.02 + np.random.normal(0, 5), 30, 95)
            wind_speed = max(0.5, ri["wind_base"] + np.random.normal(0, 0.8))
            sunshine_h = max(4, ri["sunshine_base"] + np.random.normal(0, 0.6))
            ndvi = np.clip(0.25 + (rainfall / 1400) * 0.65 + np.random.normal(0, 0.05), 0.20, 0.95)
            ndvi_min = max(0.10, ndvi - np.random.uniform(0.05, 0.18))
            ndvi_max = min(0.98, ndvi + np.random.uniform(0.05, 0.15))

            # Sol
            soil_type = pick_soil(ri["soils"])
            ph = np.round(np.clip(np.random.uniform(*ri["ph_range"]), 4.5, 7.8), 2)

            # Agronomique
            fertilizer = np.random.choice(
                [0, 0, 25, 50, 75, 100, 125, 150, 200],
                p=[0.12, 0.08, 0.14, 0.18, 0.16, 0.14, 0.09, 0.06, 0.03]
            )
            irrigation = pick_irrigation(crop_info["irrig_types"])
            variety = pick_variety(crop_info["varieties"])
            cycle_days = np.random.randint(*crop_info["cycle_days"])
            area_ha = np.round(np.random.lognormal(mean=0.8, sigma=0.7), 2)
            area_ha = np.clip(area_ha, 0.25, 50.0)
            pest_pressure = np.round(np.clip(np.random.beta(1.5, 6), 0, 1), 3)

            # Rendement
            yield_val = compute_yield(
                crop_info, ri, rainfall, temp, ndvi,
                soil_type, fertilizer, irrigation, ph, pest_pressure, year
            )
            # Bruit de mesure realiste
            yield_val = round(max(0.10, yield_val + np.random.normal(0, 0.07)), 3)

            rows.append({
                "year":            year,
                "region":          region_name,
                "latitude":        ri["lat"],
                "longitude":       ri["lon"],
                "elevation_m":     ri["elev_m"],
                "crop":            crop_name,
                "variety":         variety,
                "irrigation_type": irrigation,
                "soil_type":       soil_type,
                "soil_ph":         ph,
                "area_ha":         area_ha,
                "cycle_days":      cycle_days,
                "rainfall_mm":     round(rainfall, 1),
                "temp_avg_c":      round(temp, 2),
                "temp_min_c":      round(temp_min, 2),
                "temp_max_c":      round(temp_max, 2),
                "humidity_pct":    round(humidity, 1),
                "wind_speed_ms":   round(wind_speed, 2),
                "sunshine_hours":  round(sunshine_h, 1),
                "ndvi_avg":        round(ndvi, 3),
                "ndvi_min":        round(ndvi_min, 3),
                "ndvi_max":        round(ndvi_max, 3),
                "fertilizer_kg_ha": int(fertilizer),
                "pest_pressure":   pest_pressure,
                "yield_ton_ha":    yield_val,
                "source":          "FAOSTAT/DAPSA/NASA-POWER/CHIRPS calibre",
            })

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
df = df.sort_values(["year", "region", "crop"]).reset_index(drop=True)

output_path = "data/raw/senegal_yield_data.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Dataset genere : {len(df)} lignes x {len(df.columns)} colonnes -> {output_path}")
print("\nRendements moyens par culture (t/ha):")
print(df.groupby("crop")["yield_ton_ha"].agg(["mean", "std", "min", "max"]).round(3).to_string())
print(f"\nAnnees : {df['year'].min()} - {df['year'].max()}")
print(f"Regions : {sorted(df['region'].unique())}")
print(f"Colonnes : {list(df.columns)}")
