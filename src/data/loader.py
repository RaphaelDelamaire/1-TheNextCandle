import yfinance as yf
import pandas as pd

from config import DEFAULT_PERIOD, DEFAULT_INTERVAL

from src.data.indicators import add_indicators

def add_target(df, threshold):
    """
    Entrée : df et seuil 
    Sortie : Dataframe avec une nouvelle colonne : 0 si la prochaine bougie sera quasi nulle (en dessous du seuil en abs), 1 si elle sera au dessus du seuil, -1 si elle sera en dessous de -seuil
    """

    df = df.copy()

    future_return = (df["Close"].shift(-1)/df["Close"]) - 1
    df["target"] = 0
    df.loc[future_return > threshold, "target"] = 1
    df.loc[future_return < -threshold, "target"] = -1

    return df

def get_dataframe(ticker, threshold, period=DEFAULT_PERIOD, interval=DEFAULT_INTERVAL):
    """
    Entrée : ticker 
    Sortie : Dataframe 2 ans avec : return / return_lag1 / ma_ratio_5_10 / volatility / momentum_3 / rsi / volume_norm / hl_range / oc_change
    """

    df = yf.download(ticker, period=period, interval=interval)

    # réordonne les colonnes si elles sont désordonnées
    df = df.sort_index()

    # évite les multiindexs (les noms de colonnes sur 2 lignes)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

    df = add_indicators(df)
    df = add_target(df, threshold)
    df = df.drop(columns=["Open", "High", "Low", "Close", "Volume"])

    df = df.dropna()

    return df

def get_dataframe_for_predict(ticker, period=DEFAULT_PERIOD, interval=DEFAULT_INTERVAL):
    """
    Similaire à get_dataframe mais sans la colonne target pour la prédiction de la dernière bougie
    """
    df = yf.download(ticker, period=period, interval=interval)
    df = df.sort_index()
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

    df = add_indicators(df)
    df = df.drop(columns=["Open", "High", "Low", "Close", "Volume"])
    df = df.dropna()

    return df