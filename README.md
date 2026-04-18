# 🕯️ TheNextCandle

A machine learning model that predicts the direction of the next financial candlestick using a Random Forest classifier tuned with GridSearchCV.

**Prediction classes :**
- `1` → Bullish candle (price increase > threshold)
- `0` → Neutral candle (price movement within threshold)
- `-1` → Bearish candle (price decrease > threshold)

---

## How It Works

1. The user inputs any ticker symbol (e.g. `AAPL`, `BTC-USD`, `EURUSD=X`), validated against `yfinance`
2. 10 years of daily OHLCV data is fetched via `yfinance`
3. Technical indicators are computed as features and the target column is built from the next candle's return vs. the threshold
4. A Random Forest classifier is trained with `GridSearchCV` (5-fold CV, `f1_macro` scoring) to find the best hyperparameters
5. The best model is saved to `models/random_forest.pkl`, evaluated on a hold-out test set, and used to predict the direction of the next candle

---

## Features Used

| Feature | Description |
|---|---|
| `return` | Daily percentage return |
| `return_lag1` / `return_lag2` / `return_lag3` | Lagged returns (1, 2, 3 days) |
| `momentum_3` | 3-day price momentum |
| `momentum_5` | 5-day price momentum |
| `ma_ratio_5_10` | Ratio of 5-day MA over 10-day MA |
| `ma_ratio_20_50` | Ratio of 20-day MA over 50-day MA |
| `volatility_10` | 10-day rolling standard deviation of returns |
| `volatility_20` | 20-day rolling standard deviation of returns |
| `volume_norm` | Volume normalized by 20-day average volume |
| `hl_range` | (High - Low) / Close |
| `oc_change` | (Close - Open) / Open |
| `rsi_7` | RSI short-term (7 periods) |
| `rsi_14` | RSI (14 periods) |
| `rsi_21` | RSI long-term (21 periods) |
| `macd` | MACD line (normalized by Close) |
| `macd_signal` | MACD signal line |
| `macd_hist` | MACD histogram |
| `bb_position_20` | Position within 20-period Bollinger Bands |

**Target threshold :** `0.005` (0.5%) — a candle is considered neutral if its next-day return stays within ±0.5%.

---

## Project Structure

```
├── src/
│   ├── data/
│   │   ├── loader.py        # Data fetching via yfinance + target building
│   │   └── indicators.py    # Technical indicators computation
│   ├── model/
│   │   ├── train.py         # Baseline training + GridSearchCV tuning
│   │   ├── evaluate.py      # Classification report, confusion matrix, feature importance
│   │   └── predict.py       # Load model & predict next candle
│   └── get_inputs.py        # Ticker input validation via yfinance
├── models/
│   ├── random_forest.pkl    # Saved trained model
│   └── feature_importance.png
├── notebooks/               # Exploration notebooks
├── config.py                # Global constants (THRESHOLD, DEFAULT_PERIOD, DEFAULT_INTERVAL)
├── main.py                  # Entry point
├── requirements.txt
└── README.md
```

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/RaphaelDelamaire/1-TheNextCandle.git
cd 1-TheNextCandle
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run**
```bash
python main.py
```

Then enter any valid ticker when prompted :
```
===============================================
Enter the ticker of the financial asset : AAPL
You choose "Apple Inc." !
```

The script will run the GridSearch, save the best model to `models/random_forest.pkl`, print the performances, and predict the direction of the next candle.

---

## Dependencies

```
yfinance
scikit-learn
pandas
numpy
matplotlib
```

---

## Current Results

Tested on `AAPL` with daily candles over 10 years and `THRESHOLD = 0.005` :

| Class | F1-score |
|---|---|
| Bearish (-1) | 0.31 |
| Neutral (0) | 0.31 |
| Bullish (1) | 0.42 |

> Results vary depending on the asset. The model is still being improved.

---

## Roadmap

- [x] Data pipeline & technical indicators
- [x] Random Forest baseline model
- [x] Hyperparameter tuning (GridSearchCV)
- [x] Feature importance analysis
- [ ] Walk-forward validation
- [ ] Additional models (XGBoost, LSTM)

---

## Author

I'm a student aiming to become a quantitative analyst specialized in machine learning applied to finance.
This is my first project - I'm actively building my portfolio and publishing new projects regularly on GitHub.
Feel free to open an issue or reach out if you have any feedback !

[GitHub Profile](https://github.com/RaphaelDelamaire)

---

## Disclaimer

This project is for **educational purposes only**.
It is not financial advice and should not be used for real trading decisions.
