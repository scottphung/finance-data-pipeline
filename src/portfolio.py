import numpy as np

def optimize_portfolio(returns):

    cov = returns.cov().values

    inv = np.linalg.pinv(cov)
    ones = np.ones(len(inv))

    weights = inv @ ones
    weights = weights / weights.sum()

    return weights