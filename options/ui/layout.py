import streamlit as st
import pandas as pd

# -----------------------------
# 🎨 GLOBAL STYLING (RESTORED)
# -----------------------------
def apply_styles():
    st.markdown("""
    <style>

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    html, body, [class*="css"] {
        font-size: 13px;
    }

    /* metric cards */
    div[data-testid="stMetric"] {
        background-color: rgba(120,120,120,0.06);
        border: 1px solid rgba(120,120,120,0.12);
        padding: 6px 8px;
        border-radius: 8px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 15px;
        font-weight: 600;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 12px;
        opacity: 0.8;
    }

    h1, h2, h3 {
        margin-bottom: 0.2rem;
    }

    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# STOCK OVERVIEW
# -----------------------------
def render_stock(price, pe, div, mcap):
    st.markdown("### 📈 Stock Overview")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Price", f"${price:.2f}")
        st.metric("P/E", pe)

    with c2:
        st.metric("Div Yield", div)
        st.metric("MCap", mcap)


# -----------------------------
# BEST OPPORTUNITY
# -----------------------------
def render_best(strategy, best, option_profit, hysa_profit, edge_pct):
    st.markdown("### 🔥 Best Opportunity")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Strategy", strategy)
        st.metric("Strike", f"${best['strike']}")

    with c2:
        st.metric("DTE", f"{best['dte']}d")
        st.metric("Option Profit", f"${option_profit:.0f}")

    with c3:
        st.metric("Yield", f"{best['yield_pct']:.2f}%")
        st.metric("Distance", f"{best['distance_pct']:.2f}%")

    with c4:
        st.metric("HYSA", f"${hysa_profit:.0f}")
        st.metric("Edge %", f"{edge_pct:.1f}%")


# -----------------------------
# BOTTOM METRICS
# -----------------------------
def render_bottom(principal, best, edge):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Capital", f"${principal:,.0f}")

    with c2:
        st.metric("Expiration", pd.to_datetime(best["expiration"]).strftime("%Y-%m-%d"))

    with c3:
        st.metric("Edge ($)", f"${edge:.0f}")


# -----------------------------
# TABLE
# -----------------------------
def render_table(df):
    st.subheader("📋 Opportunities")
    st.dataframe(df, use_container_width=True)