import pandas as pd
import numpy as np

def build_options_df(ticker, expirations, strategy, max_dte):

    # 🔥 LIMIT EXPIRATIONS (CRITICAL)
    expirations = expirations[:8]

    all_data = []

    for exp in expirations:
        dte = (pd.to_datetime(exp) - pd.Timestamp.today()).days

        if dte <= 0 or dte > max_dte:
            continue

        # 🔥 USE CACHED FUNCTION
        opt = get_option_chain(ticker.ticker, exp)

        df_opt = opt.calls if strategy == "Covered Call" else opt.puts

        df_opt = df_opt.copy()
        df_opt["expiration"] = exp
        df_opt["dte"] = dte

        all_data.append(df_opt)

    if not all_data:
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)


def apply_filters(df, strategy, current_price):
    if strategy == "Covered Call":
        df = df[df["strike"] > current_price]
    else:
        df = df[df["strike"] < current_price]

    df = df[df["volume"].fillna(0) > 0]
    df["premium"] = df["bid"].fillna(0)
    df = df[df["premium"] > 0]

    df["yield_pct"] = (df["premium"] / current_price) * 100

    if strategy == "Covered Call":
        df["distance_pct"] = ((df["strike"] - current_price) / current_price) * 100
    else:
        df["distance_pct"] = ((current_price - df["strike"]) / current_price) * 100

    return df.replace([np.inf, -np.inf], np.nan).dropna()