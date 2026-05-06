import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# -----------------------
# DATABASE CONNECTION
# -----------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/finance_db"
)

# -----------------------
# STOCK LIST
# -----------------------
tickers = ["AAPL", "TSLA", "MSFT"]

all_data = []

for ticker in tickers:
    df = yf.download(ticker, start="2024-01-01", end="2025-01-01")

    # IMPORTANT FIX 1: flatten columns completely
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    df = df.reset_index()

    # IMPORTANT FIX 2: force clean column names
    df.columns = [str(col).lower().strip() for col in df.columns]

    # rename properly
    df = df.rename(columns={
        "date": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume"
    })

    df["ticker"] = ticker

    df = df[["date", "ticker", "open", "high", "low", "close", "volume"]]

    # IMPORTANT FIX 3: remove NaN issues
    df = df.dropna()

    all_data.append(df)

# combine everything
final_df = pd.concat(all_data, ignore_index=True)

# FINAL CHECK (VERY IMPORTANT DEBUG STEP)
print(final_df.head())

# load to postgres
final_df.to_sql(
    "stock_prices",
    engine,
    if_exists="append",
    index=False
)

print("Data inserted successfully!")