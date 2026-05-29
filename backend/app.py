from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "TrendPulse AI Backend Running"}

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):

    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")

    if hist.empty:
        return {"error": "Invalid ticker"}

    current_price = round(float(hist["Close"].iloc[-1]), 2)

    ma50 = round(float(hist["Close"].rolling(window=20).mean().iloc[-1]), 2)

    trend = "Bullish" if current_price > ma50 else "Bearish"

    confidence = 75 if trend == "Bullish" else 45

    return {
        "ticker": ticker.upper(),
        "trend": trend,
        "confidence": confidence,
        "current_price": current_price,
        "moving_average": ma50
    }
