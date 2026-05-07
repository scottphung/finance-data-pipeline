# 📊 Quant Hedge Fund System (Full Stack: FastAPI + Streamlit)

A small end-to-end quant finance system that:
- Pulls stock data
- Computes features
- Optimizes portfolio weights
- Backtests strategy
- Visualizes results in Streamlit UI

---

## 🚀 Features

### Backend (FastAPI)
- `/portfolio` endpoint
- Multi-asset portfolio construction
- Mean-variance optimization
- Risk metrics:
  - Sharpe Ratio
  - Value at Risk (VaR)
- Backtesting engine (equity curve simulation)

### Frontend (Streamlit)
- Multi-stock selector
- Portfolio weights visualization
- Risk metrics dashboard
- Equity curve chart

---

## 🧠 System Architecture

```
Streamlit UI
    ↓
FastAPI backend (/portfolio)
    ↓
Data Loader (prices)
    ↓
Feature Engineering
    ↓
Portfolio Optimization
    ↓
Backtesting Engine
    ↓
Risk Metrics
    ↓
JSON Response → Streamlit Charts
```

---

## 📦 Installation

### 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn pandas numpy streamlit requests yfinance scipy
```

---

## ▶️ Run the Project

### Start backend (FastAPI)

```bash
uvicorn api.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

### Start frontend (Streamlit)

```bash
streamlit run app/app.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 📊 API Usage

### Portfolio endpoint

```
GET /portfolio?tickers=AAPL,MSFT,TSLA
```

### Example response

```json
{
  "status": "success",
  "data": {
    "weights": {
      "AAPL": 0.4,
      "MSFT": 0.6
    },
    "sharpe": 1.25,
    "var": -0.03
  },
  "equity_curve": [100, 101.2, 102.5]
}
```

---

## 🧠 What the System Does

1. Fetches historical stock data (Yahoo Finance)
2. Cleans and processes price data
3. Calculates returns and features
4. Optimizes portfolio weights (mean-variance optimization)
5. Runs backtest simulation
6. Computes risk metrics
7. Sends results to Streamlit dashboard

---

## ⚠️ Known Issues (Learning Notes)

- Data dependency on Yahoo Finance (`yfinance`)
- Missing or incomplete price data can break pipeline
- NaN values must be handled before JSON serialization
- Portfolio optimization assumes valid covariance matrix

---

## 🛠 Tech Stack

- **FastAPI** — Backend API
- **Streamlit** — Frontend dashboard
- **Pandas / NumPy** — Data processing
- **SciPy** — Optimization
- **Yahoo Finance API** — Data source

---

## 📈 Future Improvements

- Add machine learning signal models
- Add factor-based investing (momentum, value, etc.)
- Add database (PostgreSQL)
- Add real-time streaming prices
- Deploy on AWS / Docker

---

## 👨‍💻 Author

Built as a learning project for:

- Quant finance
- Backend engineering
- Data pipelines
- Portfolio optimization systems