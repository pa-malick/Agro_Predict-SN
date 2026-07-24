"""Integrite du jeu de donnees produit par le pipeline."""

import hashlib

import pytest

from utils.data_loader import CHEMIN_DONNEES, empreinte_donnees, load_data
from utils.referentiel import CULTURES, IRRIGATIONS, REGIONS, SOLS

COLONNES_ATTENDUES = [
    "year", "region", "crop", "variety", "irrigation_type", "soil_type",
    "rainfall_mm", "temp_avg_c", "fertilizer_kg_ha", "pest_pressure",
    "yield_ton_ha",
]


@pytest.fixture(scope="module")
def df():
    return load_data()


def test_colonnes_presentes(df):
    manquantes = [c for c in COLONNES_ATTENDUES if c not in df.columns]
    assert not manquantes, f"Colonnes manquantes : {manquantes}"


def test_aucune_valeur_manquante(df):
    assert df.isnull().sum().sum() == 0


def test_rendements_strictement_positifs(df):
    assert (df["yield_ton_ha"] > 0).all()


def test_categories_conformes_au_referentiel(df):
    """Le pipeline ne doit produire que des valeurs declarees au referentiel."""
    for colonne, referentiel in [
        ("region", REGIONS), ("crop", CULTURES),
        ("soil_type", SOLS), ("irrigation_type", IRRIGATIONS),
    ]:
        inconnues = set(df[colonne].unique()) - set(referentiel)
        assert not inconnues, f"{colonne} contient des valeurs hors referentiel : {inconnues}"


def test_toutes_les_regions_et_cultures_sont_couvertes(df):
    assert set(df["region"].unique()) == set(REGIONS)
    assert set(df["crop"].unique()) == set(CULTURES)


def test_annees_dans_la_plage_faostat(df):
    assert df["year"].min() >= 2000
    assert df["year"].max() <= 2022


def test_empreinte_correspond_au_fichier():
    """L'empreinte publiee doit correspondre au CSV reellement present."""
    attendue = empreinte_donnees()
    assert attendue, "Empreinte absente : relancez le pipeline"
    with open(CHEMIN_DONNEES, "rb") as f:
        reelle = hashlib.sha256(f.read()).hexdigest()
    assert reelle == attendue, "Le CSV ne correspond plus a son empreinte"
