import yfinance as yf

def get_financial_asset():
    """
    Entrée : /
    Sortie : Renvoie le nom le ticker de la valeur souhaitée
    """

    fa_found = False
    while not fa_found :
        print("=============================================")
        answ = str(input("Enter the ticker of the financial asset : "))
        ticker = yf.Ticker(answ)
        info = ticker.info
        name = info.get("longName") or info.get("shortName")
        
        if name: fa_found = True
        else:  print("Financial value not found. Please try again.")

    print(f'You choose "{name}" !')
    return answ

def get_candle_time():
    """
    Entrée : /
    Sortie : Renvoie la durée de la prochaine bougie choisie
    """
    
    candle_found = False
    while not candle_found :
        print("=============================================")
        print("Choose the next candle you want to predict :\n[1] 1 minute\t[4] 30 minutes\n[2] 5 minutes\t[5] 1 hour\n[3] 15 minutes\t[6] 1 day\n")
        answ = input("Enter the number : ")
        
        try : answ = int(answ)
        except ValueError :
            print("Candle not found. Please try again.")
            continue
        try :
            assert(1<=answ and answ<=6)
            candle_found = True
        except AssertionError : print("Wrong number. Please try again.")
    
    interval_list = ['1m', '5m', '15m', '30m', '1h', '1d']

    return interval_list[answ-1]
