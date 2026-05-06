import yfinance as yf
import pandas as pd

# Step 1: define stocks
tickers = ["AAPL", "TSLA", "MSFT"]

# Step 2: empty list to store data
all_data = []

# Step 3: loop through stocks
for ticker in tickers:
    data = yf.download(ticker, start="2024-01-01", end="2025-01-01")
    data.reset_index(inplace=True)
    data["Ticker"] = ticker
    all_data.append(data)

# Step 4: combine all stocks
final_df = pd.concat(all_data)

# Step 5: save to file
final_df.to_csv("data/stock_data.csv", index=False)

print("Data saved successfully!")