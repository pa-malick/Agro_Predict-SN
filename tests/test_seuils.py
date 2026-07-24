"""CA-6 : seuils de performance en dessous desquels le modele n'est pas deployable.

Volontairement prudents : ils detectent une regression franche, pas une variation
de quelques centiemes entre deux entrainements.
"""

import pytest

from models.predict import get_model_info, get_model_metrics, load_model

R2_MINIMUM = 0.85
RMSE_MAXIMUM = 0.50
MAE_MAXIMUM = 0.35


@pytest.fixture(scope="module", autouse=True)
def modele_present():
    if load_model() is None:
        pytest.fail("Aucun modele entraine : lancez python -m models.train_model")


def test_r2_au_dessus_du_seuil():
    r2 = get_model_metrics()["r2"]
    assert r2 >= R2_MINIMUM, f"R2 {r2} sous le seuil {R2_MINIMUM}"


def test_rmse_sous_le_seuil():
    rmse = get_model_metrics()["rmse"]
    assert rmse <= RMSE_MAXIMUM, f"RMSE {rmse} au-dessus du seuil {RMSE_MAXIMUM}"


def test_mae_sous_le_seuil():
    mae = get_model_metrics()["mae"]
    assert mae <= MAE_MAXIMUM, f"MAE {mae} au-dessus du seuil {MAE_MAXIMUM}"


def test_artefact_tracable():
    """Un modele sans version ni empreinte ne doit jamais partir en production."""
    infos = get_model_info()
    assert infos.get("version"), "Version absente de l'artefact"
    assert infos.get("commit"), "Commit absent de l'artefact"
    assert infos.get("empreinte_donnees"), "Empreinte des donnees absente de l'artefact"
