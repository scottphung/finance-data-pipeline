import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# DB connection
engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/finance_db")

# Load data
df = pd.read_sql("SELECT * FROM stock_prices", engine)

st.title("📊 Stock Market Dashboard")

# Stock selector
ticker = st.selectbox("Select Stock", df["ticker"].unique())

data = df[df["ticker"] == ticker].sort_values("date")

# Price chart
st.subheader("Closing Price")
st.line_chart(data.set_index("date")["close"])

# Moving average
data["MA20"] = data["close"].rolling(20).mean()

st.subheader("Moving Average (20-day)")
st.line_chart(data.set_index("date")[["close", "MA20"]])