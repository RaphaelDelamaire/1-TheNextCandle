import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn

from src.get_inputs import get_financial_asset
from src.get_data import get_dataframe

THRESHOLD = 0.001


def main() :

    # 1 - déterminer les choix d'entrée (valeur et temps de la bougie)
    ticker = get_financial_asset()

    # 2 - récupérer les données correspondantes dans un dataframe avec les indicateurs
    df = get_dataframe(ticker, THRESHOLD)
    
    print(df[len(df)-10:len(df)])
    print(df.columns)

    # 3

    pass

if __name__ == "__main__":
    main()