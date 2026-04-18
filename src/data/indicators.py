def add_return(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "return")
    """
    
    df["return"] = df["Close"].pct_change()
    return df

def add_return_lag1(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "return_lag1")
    """
    
    df["return_lag1"] = df["return"].shift(1)
    return df

def add_ma_ratio_5_10(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "ma_ratio_5_10")
    """
    
    df["ma_ratio_5_10"] = df["Close"].rolling(5).mean() / df["Close"].rolling(10).mean()
    return df

def add_volatility(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "volatility")
    """
    
    df["volatility"] = df["return"].rolling(10).std()
    return df

def add_momentum_3(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "momentum_3")
    """
    
    df["momentum_3"] = df["Close"].pct_change(3)
    return df

def add_rsi(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "rsi")
    """
    
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def add_volume_norm(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "volume_norm")
    """
    
    df["volume_norm"] = df["Volume"] / (df["Volume"].rolling(20).mean() + 1e-10)
    return df

def add_hl_range(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "hl_range")
    """
    
    df["hl_range"] = (df["High"] - df["Low"]) / df["Close"]
    return df

def add_oc_change(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "oc_change")
    """
    
    df["oc_change"] = (df["Close"] - df["Open"]) / df["Open"]
    return df