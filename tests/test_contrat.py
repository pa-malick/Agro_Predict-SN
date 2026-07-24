"""CA-1 et CA-4 : le contrat entre l'interface, le modele et la documentation.

CA-1 : toute valeur proposee par l'interface est connue du modele. Une valeur
       inconnue leve une erreur explicite, jamais une prediction silencieuse.
CA-4 : aucune metrique de performance n'est ecrite en dur dans le code ou la
       documentation.
"""

import re
from pathlib import Path

import pytest

from models.predict import load_model, predict_yield
from utils.referentiel import CULTURES, IRRIGATIONS, REGIONS, SOLS, libelles, valider

RACINE = Path(__file__).resolve().parent.parent

CHAMPS = [
    ("region", REGIONS),
    ("crop", CULTURES),
    ("soil_type", SOLS),
    ("irrigation_type", IRRIGATIONS),
]


@pytest.fixture(scope="module")
def bundle():
    b = load_model()
    if b is None:
        pytest.skip("Modele absent : lancez python -m models.train_model")
    return b


# --- CA-1 -------------------------------------------------------------------

@pytest.mark.parametrize("champ, referentiel", CHAMPS)
def test_referentiel_correspond_au_modele(bundle, champ, referentiel):
    """Chaque valeur du referentiel est connue de l'encodeur, et inversement."""
    ordre = ["region", "crop", "soil_type", "irrigation_type", "variety"]
    apprises = set(bundle["encoder"].categories_[ordre.index(champ)])
    declarees = set(referentiel)
    assert declarees == apprises, (
        f"Desaccord sur '{champ}'. "
        f"Declarees mais inconnues du modele : {declarees - apprises}. "
        f"Connues du modele mais absentes du referentiel : {apprises - declarees}."
    )


@pytest.mark.parametrize("champ, referentiel", CHAMPS)
def test_libelles_affiches_sont_convertibles(champ, referentiel):
    """Tout libelle affiche a l'utilisateur se convertit en valeur canonique."""
    for libelle in libelles(referentiel):
        assert valider(champ, libelle) in referentiel


def test_libelles_accentues_donnent_le_meme_resultat(bundle):
    """Le libelle affiche et la valeur canonique doivent predire la meme chose.

    C'est le test qui aurait attrape le bug d'origine : l'interface envoyait
    'Thies' et 'Mais' accentues, que l'encodeur transformait en vecteur nul.
    """
    for canonique, affiche in [("Thies", "Thiès"), ("Sedhiou", "Sédhiou")]:
        for culture in ("Mais", "Maïs"):
            attendu = predict_yield(canonique, "Mais")
            obtenu = predict_yield(affiche, culture)
            assert obtenu == attendu, f"{affiche}/{culture} devrait valoir {canonique}/Mais"


@pytest.mark.parametrize("champ, valeur", [
    ("region", "Dakar"),
    ("crop", "Manioc"),
    ("soil_type", "Volcanique"),
    ("irrigation_type", "Goutte a goutte"),
])
def test_valeur_inconnue_leve_une_erreur(champ, valeur):
    """Une valeur hors referentiel doit echouer bruyamment."""
    with pytest.raises(ValueError):
        valider(champ, valeur)


def test_prediction_avec_region_inconnue_echoue(bundle):
    with pytest.raises(ValueError):
        predict_yield("Dakar", "Arachide")


# --- CA-4 -------------------------------------------------------------------

FICHIERS_SURVEILLES = [
    *(RACINE / "pages").glob("*.py"),
    RACINE / "streamlit_app.py",
    RACINE / "README.md",
]

# Une metrique ecrite en dur ressemble a "R2 = 0.98" ou "RMSE : 0.13".
MOTIF_METRIQUE = re.compile(r"(R²|R2|RMSE|MAE)\s*[:=]\s*\d", re.IGNORECASE)


@pytest.mark.parametrize("chemin", FICHIERS_SURVEILLES, ids=lambda p: p.name)
def test_aucune_metrique_ecrite_en_dur(chemin):
    """Les metriques affichees doivent venir de l'artefact, pas du code source."""
    if not chemin.exists():
        pytest.skip(f"{chemin.name} absent")
    trouvees = MOTIF_METRIQUE.findall(chemin.read_text(encoding="utf-8"))
    assert not trouvees, (
        f"{chemin.name} contient une metrique ecrite en dur : {trouvees}. "
        "Utilisez get_model_metrics()."
    )
