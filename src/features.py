import pandas as pd

def add_features(df: pd.DataFrame):

    # ---------------------------
    # 1. Normalize column names
    # ---------------------------
    df.columns = [str(c).lower() for c in df.columns]

    # ---------------------------
    # 2. Handle MultiIndex case
    # ---------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).lower() for col in df.columns]

    # ---------------------------
    # 3. Find correct close column
    # ---------------------------
    close_col = None

    for c in df.columns:
        if "close" in c:
            close_col = c
            break

    if close_col is None:
        raise ValueError(f"No close column found. Columns: {df.columns}")

    # ---------------------------
    # 4. Compute features safely
    # ---------------------------
    df["returns"] = df[close_col].pct_change().fillna(0)

    df["volatility"] = df["returns"].rolling(20).std().fillna(0)

    df["momentum"] = df[close_col] / df[close_col].shift(10) - 1
    df["momentum"] = df["momentum"].fillna(0)

    return df