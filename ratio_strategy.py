import yfinance as yf
import pandas as pd

# ETFs
NBES = "NIFTYBEES.NS"
GBES = "GOLDBEES.NS"

# Download 5 years data
nbes = yf.download(NBES, period="5y", auto_adjust=True)
gbes = yf.download(GBES, period="5y", auto_adjust=True)

# Create ratio
df = pd.DataFrame()
df["NBES"] = nbes["Close"]
df["GBES"] = gbes["Close"]
df["Ratio"] = df["NBES"] / df["GBES"]

# Moving averages
df["MA50"] = df["Ratio"].rolling(50).mean()
df["MA200"] = df["Ratio"].rolling(200).mean()

latest = df.iloc[-1]

print("\n===== DAILY SIGNAL =====")
print(f"Date  : {df.index[-1].date()}")
print(f"Ratio : {latest['Ratio']:.3f}")
print(f"MA50  : {latest['MA50']:.3f}")
print(f"MA200 : {latest['MA200']:.3f}")

if latest["MA50"] > latest["MA200"]:
    print("\nSIGNAL: BUY NIFTYBEES")
else:
    print("\nSIGNAL: BUY GOLDBEES")