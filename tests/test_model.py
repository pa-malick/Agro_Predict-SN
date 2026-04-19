import pytest
from models.predict import predict_yield, predict_interval, get_model_metrics


REGIONS = ["Thies", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sedhiou"]
CROPS = ["Arachide", "Mil", "Mais", "Riz", "Sorgho"]


def test_prediction_positive():
    pred = predict_yield("Thies", "Arachide", 650, 27.5, 0.65)
    assert pred > 0, "Le rendement doit etre positif"


def test_prediction_range():
    pred = predict_yield("Kaolack", "Mil", 600, 28.0, 0.60)
    assert 0.3 <= pred <= 6.0, f"Rendement hors plage realiste: {pred}"


def test_riz_saint_louis():
    """Saint-Louis avec irrigation doit avoir un rendement riz eleve."""
    pred = predict_yield("Saint-Louis", "Riz", 320, 26.8, 0.78)
    assert pred > 2.0, f"Riz irrique Saint-Louis devrait depasser 2 t/ha, obtenu: {pred}"


def test_all_regions_all_crops():
    for region in REGIONS:
        for crop in CROPS:
            pred = predict_yield(region, crop, 650, 27.5, 0.65)
            assert isinstance(pred, float), f"Prediction non numerique pour {region}/{crop}"
            assert pred > 0, f"Prediction negative pour {region}/{crop}"


def test_rainfall_effect():
    """Avec plus de pluie ET meilleur NDVI -> meilleur rendement."""
    pred_low  = predict_yield("Kaffrine", "Arachide", 300, 30.0, 0.35, fertilizer_kg_ha=0)
    pred_high = predict_yield("Kaffrine", "Arachide", 850, 27.5, 0.78, fertilizer_kg_ha=100)
    assert pred_high > pred_low, f"Meilleures conditions ({pred_high}) doivent surpasser mauvaises ({pred_low})"


def test_predict_interval():
    pred, low, high = predict_interval("Fatick", "Mais", 700, 27.0, 0.70)
    assert low <= pred <= high, "La prediction doit etre dans l'intervalle"
    assert high - low > 0, "L'intervalle doit etre non nul"


def test_model_metrics_present():
    metrics = get_model_metrics()
    if metrics:
        assert "r2" in metrics
        assert "rmse" in metrics
        assert metrics["r2"] > 0.8, f"R2 trop faible: {metrics['r2']}"
        assert metrics["rmse"] < 0.5, f"RMSE trop eleve: {metrics['rmse']}"
