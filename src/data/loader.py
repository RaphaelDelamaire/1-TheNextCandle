import yfinance as yf
import pandas as pd

from src.data.indicators import add_return, add_return_lag1, add_ma_ratio_5_10, add_volatility, add_momentum_3, add_rsi, add_volume_norm, add_hl_range, add_oc_change

def add_indicators(df) :
    """
    Entrée : Dataframe 
    Sortie : Dataframe avec ajouté : return / return_lag1 / ma_ratio_5_10 / volatility / momentum_3 / rsi / volume_norm / hl_range / oc_change
    """

    df = df.copy()

    df = add_return(df)
    df = add_return_lag1(df)
    df = add_ma_ratio_5_10(df)
    df = add_volatility(df)
    df = add_momentum_3(df)
    df = add_rsi(df)
    df = add_volume_norm(df)
    df = add_hl_range(df)
    df = add_oc_change(df)

    return df

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

def get_dataframe(ticker, threshold, period="2y", interval="1h"):
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