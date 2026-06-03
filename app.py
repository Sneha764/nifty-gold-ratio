import streamlit as st
import yfinance as yf
import pandas as pd

st.title("NIFTYBEES vs GOLDBEES Strategy")

if st.button("Run Signal"):

    nbes = yf.download("NIFTYBEES.NS", period="5y", auto_adjust=True)
    gbes = yf.download("GOLDBEES.NS", period="5y", auto_adjust=True)

    df = pd.DataFrame()
    df["NBES"] = nbes["Close"]
    df["GBES"] = gbes["Close"]

    df["Ratio"] = df["NBES"] / df["GBES"]
    df["MA50"] = df["Ratio"].rolling(50).mean()
    df["MA200"] = df["Ratio"].rolling(200).mean()

    latest = df.iloc[-1]

    signal = (
        "BUY NIFTYBEES"
        if latest["MA50"] > latest["MA200"]
        else "BUY GOLDBEES"
    )

    st.subheader("Current Signal")

    st.write("Date:", df.index[-1].date())
    st.write("Ratio:", round(float(latest["Ratio"]), 3))
    st.write("MA50:", round(float(latest["MA50"]), 3))
    st.write("MA200:", round(float(latest["MA200"]), 3))

    st.success(signal)