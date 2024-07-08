import yfinance as yf
import matplotlib.pyplot as plt
from MyIndicators import get_indicator
import ccxt

# Funzione per scaricare i dati storici
def download_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# Scarica i dati storici per BTC
data = download_data('BTC-USD', '2022-01-01', '2023-01-01')
high = data['High']
low = data['Low']
close = data['Close']
open_ = data['Open']
volume = data['Volume']

# VORTEX
vi = get_indicator('vortex', length=14)
vi_plus, vi_minus = vi.calculate(high, low, close, open_)

print("VI+:", vi_plus)
print("VI-:", vi_minus)

# RSI
rsi = get_indicator('RSI', rsi_period=14)
rsi_values = rsi.calculate(close)

print('RSI:', rsi_values)

# MACD
macd = get_indicator('MACD', fast_length=12, slow_length=26, signal_smoothing=9)
macd_histogram, signal_line, macd_line = macd.calculate(close)

print('MACD Histogram:', macd_histogram)
print('Signal Line:', signal_line)
print('MACD Line:', macd_line)

# Volume SMA
sma_length = 150
volume_sma = volume.rolling(window=sma_length).mean()
data['Volume_SMA'] = volume_sma

# CandleConditions
candle_conditions = get_indicator('candleconditions')
is_bullish, is_bearish = candle_conditions.calculate(high, low, close, open_)

data['BullishC'] = is_bullish
data['BearishC'] = is_bearish

print('BullishC:', is_bullish)
print('BearishC:', is_bearish)

# Generazione segnali long e short
long_signals = (data['BullishC'] & (data['Volume'] < data['Volume_SMA']) & (signal_line < 0) &
                (vi_plus < 1) & (vi_minus > 1) & (rsi_values < 47))

short_signals = (data['BearishC'] & (data['Volume'] > data['Volume_SMA']) & (signal_line > 0) &
                 (vi_plus > 1) & (vi_minus < 1) & (rsi_values > 60))

# Stampare segnali long e short
print('Long Signals:', long_signals[long_signals].index)
print('Short Signals:', short_signals[short_signals].index)

# Plotting
plt.figure(figsize=(14, 10))

# Plot candlestick data
ax1 = plt.subplot(5, 1, 1)
ax1.plot(data.index, close, label='Close')
ax1.set_title('BTC-USD Price Data')
ax1.set_ylabel('Price')
ax1.legend()

# Plot Bullish and Bearish signals
ax2 = plt.subplot(5, 1, 2)
ax2.plot(data.index, is_bullish, label='Bullish', marker='o', linestyle='None')
ax2.plot(data.index, is_bearish, label='Bearish', marker='x', linestyle='None')
ax2.set_title('Candle Conditions')
ax2.set_ylabel('Signals')
ax2.legend()

# Plot MACD
ax3 = plt.subplot(5, 1, 3)
ax3.plot(data.index, macd_line, label='MACD Line')
ax3.plot(data.index, signal_line, label='Signal Line')
ax3.bar(data.index, macd_histogram, label='Histogram', color='grey')
ax3.set_title('MACD')
ax3.legend()

# Plot RSI
ax4 = plt.subplot(5, 1, 4)
ax4.plot(data.index, rsi_values, label='RSI')
ax4.axhline(47, color='green', linestyle='--')
ax4.axhline(60, color='red', linestyle='--')
ax4.set_title('RSI')
ax4.legend()

# Plot Vortex Indicator
ax5 = plt.subplot(5, 1, 5)
ax5.plot(data.index, vi_plus, label='VI+')
ax5.plot(data.index, vi_minus, label='VI-')
ax5.axhline(1, color='black', linestyle='--')
ax5.set_title('Vortex Indicator')
ax5.legend()

plt.tight_layout()
plt.show()
