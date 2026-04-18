from config import THRESHOLD
from src.get_inputs import get_financial_asset
from src.data.loader import get_dataframe
from src.model.train import tune_model
from src.model.evaluate import evaluate, show_feature_importance
from src.model.predict import predict_next_candle


def main():
    ticker = get_financial_asset()
    df = get_dataframe(ticker, THRESHOLD)

    model, X_test, y_test = tune_model(df)
    evaluate(model, X_test, y_test)
    
    # show_feature_importance(model, df.drop(columns=["target"]).columns)

    predict_next_candle(model, ticker)


if __name__ == "__main__":
    main()