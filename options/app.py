import streamlit as st
import time
import numpy as np

from services.data_service import get_price, get_options, get_ticker
from core.filters import build_options_df, apply_filters
from core.scoring import add_scoring, get_best
from core.metrics import fmt_market_cap, compute_hysa
from ui.layout import render_stock, render_best, render_bottom, render_table, apply_styles
from config import DEFAULT_REFRESH_SEC, DEFAULT_MAX_DTE, DEFAULT_HYSA

st.set_page_config(page_title="Options Income Finder", layout="wide")
apply_styles()   # 🔥 ADD THIS LINE
st.title("📊 Options Income Strategy Finder")

# -----------------------------
# UI
# -----------------------------
col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 2, 1, 2, 1])

with col1:
    ticker_input = st.text_input("Ticker", value="AAPL")

with col2:
    max_dte = st.number_input("Max DTE", min_value=1, value=DEFAULT_MAX_DTE)

with col3:
    strategy = st.radio(
        "Strategy",
        ["Covered Call", "Cash-Secured Put"],
        horizontal=True
    )

with col4:
    hysa_rate = st.number_input("HYSA %", min_value=0.0, value=DEFAULT_HYSA)

with col5:
    # refresh_sec = st.number_input("Refresh (sec)", min_value=5, value=DEFAULT_REFRESH_SEC)
    refresh_clicked = st.button("🔄 Refresh")

with col6:
    strike_container = st.container()

# -----------------------------
# MAIN
# -----------------------------
if ticker_input and refresh_clicked:

    ticker = get_ticker(ticker_input.upper())

    try:
        expirations = get_options(ticker_input.upper())

        if not expirations:
            st.error("No options data found.")
            st.stop()

        current_price = get_price(ticker_input.upper())
        info = ticker.info

        pe = info.get("trailingPE")
        mcap = fmt_market_cap(info.get("marketCap"))
        div = info.get("dividendRate")

        div = f"{(div/current_price)*100:.2f}%" if div else "N/A"
        pe = f"{pe:.2f}" if pe else "N/A"

        df = build_options_df(ticker, expirations, strategy, max_dte)
        df = apply_filters(df, strategy, current_price)

        if df.empty:
            st.warning("No options found.")
            st.stop()

        # strike filter (UNCHANGED)
        strikes = sorted(df["strike"].unique())

        c1, c2 = strike_container.columns(2)

        with c1:
            strike_min = st.number_input("Min Strike", float(min(strikes)), float(max(strikes)), float(min(strikes)))

        with c2:
            strike_max = st.number_input("Max Strike", float(min(strikes)), float(max(strikes)), float(max(strikes)))

        df = df[(df["strike"] >= strike_min) & (df["strike"] <= strike_max)]

        df = add_scoring(df)
        best, df = get_best(df)

        principal = current_price * 100 if strategy == "Covered Call" else best["strike"] * 100

        _, hysa_profit = compute_hysa(principal, hysa_rate, best["dte"])
        option_profit = best["premium"] * 100

        edge = option_profit - hysa_profit
        edge_pct = (edge / hysa_profit * 100) if hysa_profit > 0 else 0

        # ---------------- UI ----------------
        left, right = st.columns([1, 2])

        with left:
            render_stock(current_price, pe, div, mcap)

        with right:
            render_best(strategy, best, option_profit, hysa_profit, edge_pct)

        render_bottom(principal, best, edge)
        st.divider()
        render_table(df)

        # time.sleep(refresh_sec)
        # st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")