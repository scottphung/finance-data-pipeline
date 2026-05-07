import yfinance as yf
import pandas as pd

def load_data(ticker: str):

    df = yf.download(ticker, period="1y", interval="1d")

    # -----------------------------
    # HARD VALIDATION (CRITICAL)
    # -----------------------------
    if df is None or df.empty:
        raise ValueError(f"No data returned for ticker: {ticker}")

    # -----------------------------
    # FLATTEN MULTIINDEX (YF BUG FIX)
    # -----------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).lower() for col in df.columns]
    else:
        df.columns = [c.lower() for c in df.columns]

    return df