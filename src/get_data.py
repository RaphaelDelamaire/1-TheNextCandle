import yfinance as yf

def add_indicators(df) :
    """
    Entrée : Dataframe 
    Sortie : Dataframe avec ajouté : return / return_lag1 / ma_ratio_5_10 / volatility / momentum_3 / rsi / volume_norm / hl_range / oc_change
    """

    df = df.copy()

    # return
    df["return"] = df["Close"].pct_change()
    # return lag 1
    df["return_lag1"] = df["return"].shift(1)
    # Moving average (5/10)
    df["ma_ratio_5_10"] = df["Close"].rolling(5).mean() / df["Close"].rolling(10).mean()
    # Volatility
    df["volatility"] = df["return"].rolling(10).std()
    # Momentum 3
    df["momentum_3"] = df["Close"].pct_change(3)

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df["rsi"] = 100 - (100 / (1 + rs))

    # Volume normalised
    df["volume_norm"] = df["Volume"] / (df["Volume"].rolling(20).mean() + 1e-10)

    # High vs Low range
    df["hl_range"] = (df["High"] - df["Low"]) / df["Close"]
    # Open vs Close change
    df["oc_change"] = (df["Close"] - df["Open"]) / df["Open"]

    return df

def add_target(df, threshold):
    """
    Entrée : df et seuil 
    Sortie : Dataframe avec une nouvelle colonne : 0 si la prochaine bougie sera quasi nulle (en dessous du seuil en abs), 1 si elle serat au dessus du seuil, -1 si elle sera en dessous de -seuil
    """

    df = df.copy()

    future_return = (df["Close"].shift(-1)/df["Close"]) - 1
    df["target"] = 0
    df.loc[future_return > threshold, "target"] = 1
    df.loc[future_return < -threshold, "target"] = -1

    return df

def get_dataframe(ticker, threshold):
    """
    Entrée : ticker 
    Sortie : Dataframe 2 ans avec : return / return_lag1 / ma_ratio_5_10 / volatility / momentum_3 / rsi / volume_norm / hl_range / oc_change
    """

    df = yf.download(ticker, period="2y", interval="1h")

    # réordonne les colonnes si elles sont désordonnées
    df = df.sort_index()

    # évite les multiindexs (grossièrement : les noms de colonnes sur 2 lignes)
    if isinstance(df.columns, tuple) or hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    df = add_indicators(df)
    df = add_target(df, threshold)
    df = df.drop(columns=["Open", "High", "Low", "Close"])
    df = df.dropna()

    return df