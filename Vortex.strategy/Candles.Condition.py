import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Scarica i dati storici
ticker = 'AAPL'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
high = data['High']
low = data['Low']
close = data['Close']
open_ = data['Open']

# Spostare le serie temporali per ottenere i valori delle candele precedenti
#lows
prev_low = low.shift(1)
prev2_low = low.shift(2)
third_last_low = low.shift(3)
#highs
prev_high = high.shift(1)
prev2_high = high.shift(2)
third_last_high = high.shift(3)
#close
prev_close = close.shift(1)
prev2_close = close.shift(2)
third_last_close = close.shift(3)
#open
prev_open = open_.shift(1)
prev2_open = open_.shift(2)
third_last_open = open_.shift(3)



# Definire i pattern candlestick
def is_bullish(high, low, close, open_, shift_period=3):
    return (prev2_low < prev_low) & (prev_low < low) & (prev2_close > close) & (prev_close < close) & (prev_high < close) & (prev2_open < prev_open)

def is_bearish(high, low, close, open_, shift_period=3):
    return (prev2_low > prev_low) & (prev_low > low) & (prev2_close < close) & (prev_close > close) & (prev_high > close)

# Applicare i pattern ai dati
data['Bullish'] = is_bullish(high, low, close, open_)
data['Bearish'] = is_bearish(high, low, close, open_)