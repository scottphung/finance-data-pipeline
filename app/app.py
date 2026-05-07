import streamlit as st
import requests

st.set_page_config(page_title="Quant Hedge Fund", layout="wide")
st.title("📊 Quant Hedge Fund System vFinal")

tickers = st.multiselect(
    "Select Assets",
    ["AAPL", "MSFT", "TSLA", "GOOG", "AMZN"],
    default=["AAPL", "MSFT"]
)

if st.button("Run Analysis"):

    res = requests.get(
        "http://localhost:8000/portfolio",
        params={"tickers": ",".join(tickers)}
    )

    # --------------------------
    # API ERROR HANDLING
    # --------------------------
    if res.status_code != 200:
        st.error(res.text)
        st.stop()

    result = res.json()

    if result.get("status") == "error":
        st.error(result["message"])
        st.stop()

    # --------------------------
    # WEIGHTS
    # --------------------------
    st.subheader("📌 Portfolio Weights")

    st.json(result["data"]["weights"])

    # --------------------------
    # RISK METRICS
    # --------------------------
    st.subheader("📊 Risk Metrics")
    st.write("Sharpe:", result["data"]["sharpe"])
    st.write("VaR:", result["data"]["var"])

    # --------------------------
    # EQUITY CURVE
    # --------------------------
    st.subheader("📈 Equity Curve")

    st.line_chart(result["equity_curve"])