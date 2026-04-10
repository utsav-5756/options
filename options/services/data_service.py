import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)
def get_price(symbol):
    t = yf.Ticker(symbol)
    return t.history(period="5d")["Close"].dropna().iloc[-1]

@st.cache_data(ttl=300)
def get_options(symbol):
    t = yf.Ticker(symbol)
    return t.options

def get_ticker(symbol):
    return yf.Ticker(symbol)