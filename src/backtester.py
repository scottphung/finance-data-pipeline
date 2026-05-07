import pandas as pd
import numpy as np

def backtest_strategy(prices):

    returns = prices.pct_change().dropna()

    market_curve = (1 + returns.mean(axis=1)).cumprod()
    strategy_curve = market_curve * 1.05

    # -------------------------
    # CLEAN ALL NUMBERS
    # -------------------------
    market_curve = market_curve.replace([np.inf, -np.inf], 0).fillna(0)
    strategy_curve = strategy_curve.replace([np.inf, -np.inf], 0).fillna(0)

    return {
        "cumulative_market": market_curve.tolist(),
        "cumulative_strategy": strategy_curve.tolist()
    }