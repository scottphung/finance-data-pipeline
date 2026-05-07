import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import minimize
from prophet import Prophet
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Hedge Fund Dashboard v1", layout="wide")
st.title("📊 Hedge Fund Interview Project v1")

st_autorefresh(interval=10000, key="refresh")

# -----------------------------
# DATA LOADER
# -----------------------------
@st.cache_data
def load_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d")

    # -------------------------
    # STEP 1: HANDLE MULTIINDEX
    # -------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join([str(i) for i in col if i]) for col in df.columns]

    # -------------------------
    # STEP 2: FLATTEN + NORMALIZE
    # -------------------------
    df = df.reset_index()
    df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]

    # -------------------------
    # STEP 3: STANDARDIZE COLUMN NAMES
    # -------------------------
    rename_map = {}

    for col in df.columns:
        if "date" in col or "time" in col:
            rename_map[col] = "date"
        elif "open" in col:
            rename_map[col] = "open"
        elif "high" in col:
            rename_map[col] = "high"
        elif "low" in col:
            rename_map[col] = "low"
        elif "close" in col and "adj" not in col:
            rename_map[col] = "close"
        elif "volume" in col:
            rename_map[col] = "volume"

    df = df.rename(columns=rename_map)

    # -------------------------
    # STEP 4: FORCE REQUIRED COLUMNS
    # -------------------------
    required = ["date", "open", "high", "low", "close", "volume"]

    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error("❌ Missing columns after cleanup")
        st.write("Available columns:", df.columns)
        st.stop()

    df["date"] = pd.to_datetime(df["date"])

    return df

# -----------------------------
# SIDEBAR
# -----------------------------
tickers = st.sidebar.multiselect(
    "Select Stocks",
    ["AAPL", "MSFT", "TSLA", "GOOG", "AMZN"],
    default=["AAPL", "MSFT"]
)

window = st.sidebar.slider("Moving Average Window", 5, 50, 20)

# -----------------------------
# LOAD DATA
# -----------------------------
data = {t: load_data(t) for t in tickers}

prices = pd.DataFrame({
    t: data[t].set_index("date")["close"]
    for t in tickers
}).dropna()

returns = prices.pct_change().dropna()

# -----------------------------
# STRATEGY ENGINE (NEW)
# -----------------------------
def generate_signal(df):
    df["ma_short"] = df["close"].rolling(10).mean()
    df["ma_long"] = df["close"].rolling(30).mean()

    df["signal"] = np.where(df["ma_short"] > df["ma_long"], "BUY", "SELL")
    return df

# -----------------------------
# SELECT STOCK
# -----------------------------
selected = tickers[0]
df = generate_signal(data[selected])

# -----------------------------
# PRICE CHART
# -----------------------------
st.subheader("📈 Price + Strategy Signal")

fig = go.Figure()

fig.add_trace(go.Scatter(x=df["date"], y=df["close"], name="Price"))
fig.add_trace(go.Scatter(x=df["date"], y=df["ma_short"], name="MA 10"))
fig.add_trace(go.Scatter(x=df["date"], y=df["ma_long"], name="MA 30"))

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df[["date", "close", "signal"]].tail(10))

# -----------------------------
# PORTFOLIO OPTIMIZATION
# -----------------------------
st.subheader("💼 Portfolio Optimization")

cov = returns.cov()
n = len(tickers)

def portfolio_vol(w):
    return np.sqrt(w.T @ cov.values @ w)

constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
bounds = [(0, 1)] * n
init = np.ones(n) / n

res = minimize(portfolio_vol, init, bounds=bounds, constraints=constraints)

st.dataframe(pd.DataFrame({
    "Ticker": tickers,
    "Weight": res.x
}))

# -----------------------------
# RISK METRICS
# -----------------------------
st.subheader("⚠️ Risk Metrics")

portfolio_returns = returns @ res.x

sharpe = portfolio_returns.mean() / portfolio_returns.std()
var_95 = np.percentile(portfolio_returns, 5)

st.metric("Sharpe Ratio", f"{sharpe:.2f}")
st.metric("1-Day VaR", f"{var_95:.4f}")

# -----------------------------
# DRAWDOWN (IMPORTANT)
# -----------------------------
st.subheader("📉 Drawdown")

cum = (1 + portfolio_returns).cumprod()
drawdown = cum / cum.cummax() - 1

st.line_chart(drawdown)

# -----------------------------
# CORRELATION
# -----------------------------
st.subheader("🔗 Correlation Matrix")
st.dataframe(returns.corr())

# -----------------------------
# INSIGHTS ENGINE
# -----------------------------
st.subheader("🧠 Hedge Fund Insights")

avg_ret = portfolio_returns.mean()

st.markdown(f"""
- Expected Return: **{avg_ret:.4f}**
- Sharpe: **{sharpe:.2f}**
- Strategy: **Mean Reversion + Momentum Hybrid**
""")