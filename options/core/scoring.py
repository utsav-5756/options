import numpy as np

def add_scoring(df):
    df["annualized_yield"] = df["yield_pct"] * (365 / df["dte"])

    df["liquidity_score"] = np.log1p(
        df["openInterest"].fillna(0) + df["volume"].fillna(0)
    )

    df["score"] = (
        0.70 * df["annualized_yield"] +
        0.20 * df["liquidity_score"] +
        0.10 * df["yield_pct"]
    )

    return df


def get_best(df):
    df = df.sort_values(by="score", ascending=False)
    return df.iloc[0], df