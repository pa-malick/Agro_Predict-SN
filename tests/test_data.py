import pytest
import pandas as pd
import os


DATA_PATH = "data/raw/senegal_yield_data.csv"


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


def test_data_file_exists():
    assert os.path.exists(DATA_PATH), f"Dataset introuvable: {DATA_PATH}"


def test_required_columns(df):
    required = ["year", "region", "crop", "rainfall_mm", "temp_avg_c", "ndvi_avg", "yield_ton_ha"]
    for col in required:
        assert col in df.columns, f"Colonne manquante: {col}"


def test_no_nulls(df):
    assert df.isnull().sum().sum() == 0, "Des valeurs nulles trouvees dans le dataset"


def test_yield_positive(df):
    assert (df["yield_ton_ha"] > 0).all(), "Des rendements negatifs ou nuls detectes"


def test_year_range(df):
    assert df["year"].min() >= 2000
    assert df["year"].max() <= 2024


def test_all_crops_present(df):
    expected = {"Arachide", "Mil", "Riz", "Sorgho"}
    crops = set(df["crop"].unique())
    assert expected.issubset(crops), f"Cultures manquantes: {expected - crops}"
    assert any("a" in c.lower() for c in crops if c.startswith("Ma")), "Mais absent"


def test_all_regions_present(df):
    expected = {"Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda"}
    regions = set(df["region"].unique())
    assert expected.issubset(regions), f"Regions manquantes: {expected - regions}"
    assert len(regions) == 7, f"7 regions attendues, obtenu: {len(regions)}"


def test_minimum_rows(df):
    assert len(df) >= 400, f"Dataset trop petit: {len(df)} lignes"


def test_ndvi_range(df):
    assert df["ndvi_avg"].between(0.1, 1.0).all(), "NDVI hors plage [0.1, 1.0]"


def test_rainfall_plausible(df):
    assert df["rainfall_mm"].between(50, 3000).all(), "Pluviometrie hors plage plausible"
