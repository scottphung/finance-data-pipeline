import numpy as np

def sharpe_ratio(returns):

    return np.sqrt(252) * returns.mean() / returns.std()

def value_at_risk(returns):

    return np.percentile(returns, 5)