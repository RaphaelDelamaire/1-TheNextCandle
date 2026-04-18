from config import THRESHOLD, DEFAULT_PERIOD, DEFAULT_INTERVAL

from src.get_inputs import get_financial_asset
from src.data.loader import get_dataframe


def main() :

    # 1 - déterminer les choix d'entrée (valeur et temps de la bougie)
    ticker = get_financial_asset()

    # 2 - récupérer les données correspondantes dans un dataframe avec les indicateurs
    df = get_dataframe(ticker, THRESHOLD, DEFAULT_PERIOD, DEFAULT_INTERVAL)
    
    print(df[len(df)-10:len(df)])
    print(df.columns)

    # 3

    pass

if __name__ == "__main__":
    main()