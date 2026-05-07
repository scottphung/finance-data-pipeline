import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "TSLA"]

data = []

for t in tickers:
    df = yf.download(t, period="1y")
    df["ticker"] = t
    df = df.reset_index()
    data.append(df)

final = pd.concat(data)
final.to_csv("data/stocks.csv", index=False)