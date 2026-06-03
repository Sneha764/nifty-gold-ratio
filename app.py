import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from zoneinfo import ZoneInfo

st.title("NIFTY vs Gold Ratio Signal")

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

    st.markdown(f"## 🚦 {signal}")

    # =====================
    # Plotly Chart
    # =====================

    st.subheader("5-Year Ratio Trend")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Ratio"],
            mode="lines",
            name="Ratio",
            line=dict(color="#FF8C00", width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MA50"],
            mode="lines",
            name="MA50",
            line=dict(color="lightskyblue", width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["MA200"],
            mode="lines",
            name="MA200",
            line=dict(color="darkblue", width=2)
        )
    )

    fig.update_layout(
        title="NBES / GBES Ratio with MA50 and MA200",
        xaxis_title="Date",
        yaxis_title="Ratio",
        hovermode="x unified",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown(
        """
        👩‍💻 **Developed by Sneha Yadav**

        📈 NIFTYBEES vs GOLDBEES Ratio Strategy  
        📊 50-Day / 200-Day Moving Average Signal

        🔗 GitHub: [nifty-gold-ratio](https://github.com/Sneha764/nifty-gold-ratio)  
        📡 Data Source: Yahoo Finance

        ⚠️ For educational purposes only. Not financial advice.
        """
    )
    ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    st.caption(
        f"Market data date: {df.index[-1].date()} | Generated: {ist_time.strftime('%d %b %Y %I:%M:%S %p IST')}"
    )