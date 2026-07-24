"""EF-4 : l'application reste presentable quand le modele est absent.

Le modele n'est pas versionne : il est construit par la CI. Un deploiement
neuf doit donc afficher un message clair, jamais une trace d'erreur.
"""

from pathlib import Path

import pytest

from models import predict

RACINE = Path(__file__).resolve().parent.parent


@pytest.fixture
def sans_modele(monkeypatch):
    """Simule un environnement ou l'artefact du modele n'a pas ete construit."""
    monkeypatch.setattr(predict, "_cache", {})
    monkeypatch.setattr(predict, "CHEMIN_MODELE", "models/artefact_absent.pkl")
    yield
    predict._cache.clear()


def test_les_infos_sont_vides_sans_modele(sans_modele):
    """L'ecran d'accueil s'appuie sur ce dictionnaire vide pour se proteger."""
    assert predict.get_model_info() == {}
    assert predict.get_model_metrics() == {}


def test_la_simulation_echoue_avec_un_message_explicite(sans_modele):
    with pytest.raises(FileNotFoundError, match="Modele introuvable"):
        predict.simulate("Kaolack", "Arachide")


def test_l_accueil_verifie_la_presence_du_modele():
    """L'ecran d'accueil doit couper avant d'appeler le modele."""
    source = (RACINE / "streamlit_app.py").read_text(encoding="utf-8")
    assert "if not get_model_info():" in source, "Garde EF-4 absente de l'accueil"
    assert "st.stop()" in source, "L'accueil doit s'arreter au lieu de continuer"
