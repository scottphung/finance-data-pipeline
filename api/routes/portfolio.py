from fastapi import APIRouter
from src.data_loader import load_data
from src.features import add_features
from src.portfolio import optimize_portfolio
from src.risk import sharpe_ratio, value_at_risk
from src.backtester import backtest_strategy

import pandas as pd

router = APIRouter()

@router.get("/portfolio")
def portfolio(tickers: str):

    tickers = tickers.split(",")

    data = {}

    # --------------------------
    # SAFE LOADING (FIXED)
    # --------------------------
    for t in tickers:
        try:
            df = load_data(t)
            df = add_features(df)
            data[t] = df

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed on {t}: {str(e)}"
            }

    # --------------------------
    # BUILD PRICE MATRIX
    # --------------------------
    prices_dict = {}

    for t in tickers:
        df = data[t]

        # robust close detection
        close_col = None
        for c in df.columns:
            if "close" in c:
                close_col = c
                break

        if close_col is None:
            continue

        prices_dict[t] = df[close_col]

    prices = pd.DataFrame(prices_dict).dropna()

    if prices.empty:
        return {
            "status": "error",
            "message": "No price data loaded"
        }

    # --------------------------
    # RETURNS
    # --------------------------
    returns = prices.pct_change().dropna()

    if returns.empty:
        return {
            "status": "error",
            "message": "No returns computed"
        }

    # --------------------------
    # PORTFOLIO OPTIMIZATION
    # --------------------------
    weights = optimize_portfolio(returns)

    portfolio_returns = returns @ weights

    bt = backtest_strategy(prices)

    return {
        "status": "success",
        "data": {
            "weights": dict(zip(tickers, weights.tolist())),
            "sharpe": float(sharpe_ratio(portfolio_returns)),
            "var": float(value_at_risk(portfolio_returns)),
        },
        "equity_curve": bt["cumulative_strategy"]
    }   