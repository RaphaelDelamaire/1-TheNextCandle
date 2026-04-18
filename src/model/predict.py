import pickle
from src.data.loader import get_dataframe_for_predict

def load_model(model_path="models/random_forest.pkl"):
    """
    Entrée : lien vers un modèle
    Sortie : modèle chargé
    """
    
    with open(model_path, 'rb') as f :
        model = pickle.load(f)
    return model

def predict_next_candle(model, ticker):
    """
    Entrée : modèle et ticker
    Sortie : sens de la prochaine bougie
    """
    df = get_dataframe_for_predict(ticker)
    X_last = df.tail(1)
    prediction = model.predict(X_last)[0]

    labels = {1: "High", 0: "Netral", -1: "Low"}
    print(f"Prediction of the next candle : {labels[prediction]}")
    return prediction