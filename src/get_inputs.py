import yfinance as yf

def get_financial_asset():
    """
    Entrée : /
    Sortie : Renvoie le nom le ticker de la valeur souhaitée
    """

    fa_found = False
    while not fa_found :
        print("===============================================")
        ticker_input  = str(input("Enter the ticker of the financial asset : ")).strip().upper()
        ticker = yf.Ticker(ticker_input )
        info = ticker.info
        name = info.get("longName") or info.get("shortName")
        
        if name: fa_found = True
        else:  print("Financial value not found. Please try again.")

    print(f'You choose "{name}" !')
    return ticker_input 