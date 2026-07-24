"""CA-2, CA-3 et CA-5 : le modele et ce qu'il produit.

CA-2 : chaque entree exposee a l'utilisateur a un effet mesurable et dans le
       bon sens sur le resultat.
CA-3 : le modele expose sa version et l'empreinte de ses donnees.
CA-5 : les rendements simules restent dans les plages agronomiques connues.
"""

import pytest

from models.predict import get_model_info, get_model_metrics, load_model, predict_yield, simulate
from utils.referentiel import CULTURES, REGIONS

# Plages de rendement observees au Senegal, en t/ha, toutes pratiques confondues.
# Bornes larges : le test detecte l'aberration, pas la nuance.
PLAGES = {
    "Arachide": (0.3, 3.0),
    "Mil":      (0.2, 2.5),
    "Mais":     (0.5, 6.0),
    "Riz":      (1.0, 9.0),
    "Sorgho":   (0.2, 3.5),
}


@pytest.fixture(scope="module", autouse=True)
def modele_present():
    if load_model() is None:
        pytest.skip("Modele absent : lancez python -m models.train_model")


# --- CA-2 -------------------------------------------------------------------

def test_engrais_augmente_le_rendement():
    """Plus d'engrais doit donner plus de rendement, sur toutes les cultures."""
    for culture in CULTURES:
        sans = predict_yield("Kaolack", culture, fertilizer_kg_ha=0)
        avec = predict_yield("Kaolack", culture, fertilizer_kg_ha=100)
        assert avec > sans, f"{culture} : {avec} devrait depasser {sans}"


def test_effet_engrais_est_perceptible():
    """L'effet doit etre visible par l'utilisateur, pas noye dans l'arrondi."""
    sans = predict_yield("Kaolack", "Arachide", fertilizer_kg_ha=0)
    avec = predict_yield("Kaolack", "Arachide", fertilizer_kg_ha=100)
    assert (avec - sans) >= 0.05, f"Effet trop faible : +{avec - sans:.3f} t/ha"


def test_irrigation_augmente_le_rendement_du_riz():
    pluvial = predict_yield("Saint-Louis", "Riz", irrigation_type="Pluviale")
    submerge = predict_yield("Saint-Louis", "Riz", irrigation_type="Submersion")
    assert submerge > pluvial


def test_la_region_change_le_resultat():
    """Les sept regions ne doivent pas donner le meme chiffre."""
    valeurs = {r: predict_yield(r, "Arachide") for r in REGIONS}
    assert len(set(valeurs.values())) >= 4, f"Regions trop proches : {valeurs}"


def test_la_culture_change_le_resultat():
    valeurs = {c: predict_yield("Kaolack", c) for c in CULTURES}
    assert len(set(valeurs.values())) == len(CULTURES), f"Cultures confondues : {valeurs}"


def test_la_surface_multiplie_la_recolte():
    """La surface n'agit pas sur le rendement mais bien sur la recolte totale."""
    un = simulate("Kaolack", "Arachide", surface_ha=1.0)
    quatre = simulate("Kaolack", "Arachide", surface_ha=4.0)
    assert quatre["rendement_t_ha"] == un["rendement_t_ha"]
    assert quatre["recolte_t"] == pytest.approx(un["recolte_t"] * 4, rel=0.01)


# --- CA-3 -------------------------------------------------------------------

def test_le_modele_expose_sa_version_et_ses_donnees():
    infos = get_model_info()
    assert infos.get("version"), "Version du modele absente"
    assert infos.get("commit"), "Commit d'origine absent"
    empreinte = infos.get("empreinte_donnees")
    assert empreinte and len(empreinte) == 64, "Empreinte SHA256 des donnees absente"


def test_les_metriques_sont_completes():
    metriques = get_model_metrics()
    for cle in ("rmse", "mae", "r2", "n_samples", "n_train", "n_test"):
        assert cle in metriques, f"Metrique manquante : {cle}"


def test_le_jeu_de_test_est_separe():
    """Le test doit representer une part reelle des donnees."""
    m = get_model_metrics()
    assert m["n_test"] >= 0.10 * m["n_samples"], "Jeu de test trop petit"


# --- CA-5 -------------------------------------------------------------------

@pytest.mark.parametrize("culture", list(CULTURES))
def test_rendements_dans_les_plages_connues(culture):
    """Aucune combinaison region/pratique ne doit sortir des plages agronomiques."""
    bas, haut = PLAGES[culture]
    for region in REGIONS:
        for engrais in (0, 100):
            valeur = predict_yield(region, culture, fertilizer_kg_ha=engrais)
            assert bas <= valeur <= haut, (
                f"{culture} en {region} avec {engrais} kg/ha : {valeur} t/ha "
                f"hors de la plage {bas}-{haut}"
            )


def test_la_simulation_renvoie_tout_ce_qu_affiche_l_interface():
    resultat = simulate("Fatick", "Mil", surface_ha=2.0, fertilizer_kg_ha=50)
    for cle in ("rendement_t_ha", "fourchette_t_ha", "recolte_t", "recolte_sacs",
                "rendement_sans_engrais", "surface_ha"):
        assert cle in resultat
    bas, haut = resultat["fourchette_t_ha"]
    assert bas <= resultat["rendement_t_ha"] <= haut
