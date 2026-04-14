import yfinance as yf

def get_financial_asset():

    fa_found = False

    while not fa_found :
        answ = str(input("Enter the ticker of the financial asset : "))
        ticker = yf.Ticker(answ)
        info = ticker.info
        name = info.get("longName") or info.get("shortName")
        
        if name:
            fa_found = True
        else:
            print("Financial value not found. Please try again.")

    print(f'You choose "{name}" !')

    return answ