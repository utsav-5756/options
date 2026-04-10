import yfinance as yf
import streamlit as st

# 🔥 Increased cache
@st.cache_data(ttl=900)
def get_price(symbol):
    t = yf.Ticker(symbol)
    return t.history(period="5d")["Close"].dropna().iloc[-1]


@st.cache_data(ttl=900)
def get_options(symbol):
    t = yf.Ticker(symbol)
    return t.options


# 🔥 NEW: Cache each option chain
@st.cache_data(ttl=900)
def get_option_chain(symbol, expiration):
    t = yf.Ticker(symbol)
    return t.option_chain(expiration)


def get_ticker(symbol):
    return yf.Ticker(symbol)