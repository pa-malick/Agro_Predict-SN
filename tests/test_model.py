from models.predict import predict_yield

def test_prediction():
    pred = predict_yield("Thiès", "Arachide", 700, 27, 0.7)
    assert pred > 1.0, "La prédiction doit être positive"
    print("Test passé !")

if __name__ == "__main__":
    test_prediction()