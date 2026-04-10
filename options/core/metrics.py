def fmt_market_cap(v):
    if v is None:
        return "N/A"
    if v >= 1e12:
        return f"${v/1e12:.2f}T"
    if v >= 1e9:
        return f"${v/1e9:.2f}B"
    return f"${v/1e6:.2f}M"


def compute_hysa(principal, rate, dte):
    apy = rate / 100
    daily = (1 + apy) ** (1/365) - 1

    value = principal * ((1 + daily) ** dte)
    profit = value - principal

    return value, profit