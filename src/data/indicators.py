def add_indicators(df) :
    """
    Entrée : Dataframe 
    Sortie : Dataframe avec les indicateurs ajoutés
    """

    df = df.copy()

    df = add_return(df)
    df = add_return_lag(df, lag=1)
    df = add_return_lag(df, lag=2)
    df = add_return_lag(df, lag=3)
    df = add_momentum(df, momentum=3)
    df = add_momentum(df, momentum=5)
    df = add_ma_ratio(df, ma_1=5, ma_2=10)
    df = add_ma_ratio(df, ma_1=20, ma_2=50)
    df = add_volatility(df, volatility=10)
    df = add_volatility(df, volatility=20)
    df = add_volume_norm(df)
    df = add_hl_range(df)
    df = add_oc_change(df)
    df = add_rsi(df, period=7)
    df = add_rsi(df, period=14)
    df = add_rsi(df, period=21)
    df = add_macd(df)
    df = add_bb(df, period=20)

    return df

def add_return(df):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "return")
    """
    
    df["return"] = df["Close"].pct_change()
    return df

def add_return_lag(df, lag=1):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "return_lag1")
    """
    if "return" not in df.columns:
        df = add_return(df)
    df[f"return_lag{lag}"] = df["return"].shift(lag)
    return df

def add_ma_ratio(df, ma_1=5, ma_2=10):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "ma_ratio_1_2")
    """
    
    df[f"ma_ratio_{ma_1}_{ma_2}"] = df["Close"].rolling(ma_1).mean() / df["Close"].rolling(ma_2).mean()
    return df

def add_volatility(df, volatility=10):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "volatility_{volatility}")
    """
    
    df[f"volatility_{volatility}"] = df["return"].rolling(volatility).std()
    return df

def add_momentum(df, momentum=3):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "momentum_{momentum}")
    """
    
    df[f"momentum_{momentum}"] = df["Close"].pct_change(momentum)
    return df

def add_rsi(df, period=14):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "rsi_{period}")
    """
    
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df[f"rsi_{period}"] = 100 - (100 / (1 + rs))
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

def add_macd(df, span_1=12, span_2=26, span_3=9) :
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec les colonnes "macd", "macd_signal", "macd_hist")
    """
    ema12 = df["Close"].ewm(span=span_1).mean()
    ema26 = df["Close"].ewm(span=span_2).mean()
    df["macd"] = (ema12-ema26)/df["Close"]
    df["macd_signal"] = df["macd"].ewm(span=span_3).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    return df

def add_bb(df, period=20):
    """
    Entrée : df (dataframe)
    Sortie : df (dataframe avec une colonne "bb_position")
    """
    
    ma_20 = df["Close"].rolling(period).mean()
    std_20 = df["Close"].rolling(period).std()
    df[f"bb_position_{period}"] = (df["Close"] - ma_20)/(2*std_20+1e-10)
    return df