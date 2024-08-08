
import yfinance as yf
import matplotlib.pyplot as plt
from MyIndicators import get_indicator
import ccxt
import pandas as pd
import numpy as np
import time
import mplfinance as mpf
#Funzione per scaricare i dati storici

# Configura il tuo exchange (esempio: Binance)
exchange = ccxt.binance()

# Scegli il mercato e l'intervallo temporale
symbol = 'BTC/USDT'
timeframe = '1h'

# Calcola il timestamp per 30 giorni fa
since = exchange.parse8601('2022-06-15T00:00:00Z')  # esempio di data di inizio (modifica in base alle tue esigenze)


# Recupera i dati storici (candlestick)
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

# Crea un dfFrame dai dati
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# Scarica i dati storici per BTC
high = df['high']
low = df['low']
close = df['close']
open_ = df['open']
volume = df['volume']


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
df['Volume_SMA'] = volume_sma

# CandleConditions
candle_conditions = get_indicator('candleconditions')
is_bullish, is_bearish = candle_conditions.calculate(high, low, close, open_)

df['BullishC'] = is_bullish
df['BearishC'] = is_bearish

print('BullishC:', is_bullish)
print('BearishC:', is_bearish)

# Generazione segnali long e short
# Definisci i segnali di trading
df['is_volume_long'] = 0
df['is_volume_long'] = np.where(df['volume'] < df['Volume_SMA'], 1, -1)
df['is_volume_short'] = 0
df['is_volume_short'] = np.where(df['volume'] > df['Volume_SMA'], 1, -1)
df['is_signal_long'] = 0
df['is_signal_long'] = np.where(signal_line < 0, 1, -1)
df['is_signal_short'] = 0
df['is_signal_short'] = np.where(signal_line > 0, 1, -1)


df['long_signals'] = np.where(df['is_volume_long'] == 1 & df['is_signal_long'] & (vi_plus < 1) & (vi_minus > 1) & (rsi_values < 47), 1, -1)
#long_signals = is_signal_long
#print(type(long_signals))

df['short_signals'] = (df['is_volume_short'] & df['is_signal_short'] & (vi_plus > 1) & (vi_minus < 1) & (rsi_values > 60))
#short_signals = (df['volume'])
#print(type(short_signals))

# Stampare segnali long e short
#print('Long Signals:', long_signals[long_signals].index)
#print('Short Signals:', short_signals[short_signals].index)

# Plotting
plt.figure(figsize=(14, 10))

# Plot candlestick df
ax1 = plt.subplot(5, 1, 1)
ax1.plot(df.index, close, label='Close')
ax1.set_title('BTC-USD Price df')
ax1.set_ylabel('Price')
ax1.legend()

# Plot Bullish and Bearish signals
ax2 = plt.subplot(5, 1, 2)
#ax2.plot(df.index, long_signals, label='Bullish', marker='o', linestyle='None')
#ax2.plot(df.index, short_signals, label='Bearish', marker='x', linestyle='None')
ax2.plot(df.index, is_bullish, label='Bullish', marker='o', linestyle='None')
ax2.plot(df.index, is_bearish, label='Bearish', marker='x', linestyle='None')
ax2.set_title('Candle Conditions')
ax2.set_ylabel('Signals')
ax2.legend()

# Plot MACD
ax3 = plt.subplot(5, 1, 3)
ax3.plot(df.index, macd_line, label='MACD Line')
ax3.plot(df.index, signal_line, label='Signal Line')
ax3.bar(df.index, macd_histogram, label='Histogram', color='grey')
ax3.set_title('MACD')
ax3.legend()

# Plot RSI
ax4 = plt.subplot(5, 1, 4)
ax4.plot(df.index, rsi_values, label='RSI')
ax4.axhline(47, color='green', linestyle='--')
ax4.axhline(60, color='red', linestyle='--')
ax4.set_title('RSI')
ax4.legend()

# Plot Vortex Indicator
ax5 = plt.subplot(5, 1, 5)
ax5.plot(df.index, vi_plus, label='VI+')
ax5.plot(df.index, vi_minus, label='VI-')
ax5.axhline(1, color='black', linestyle='--')
ax5.set_title('Vortex Indicator')
ax5.legend()

plt.tight_layout()
#plt.show()

print("Length of df.index:", len(df.index))
print("Length of close:", len(close))
print("Length of is_bullish:", len(is_bullish))
print("Length of is_bearish:", len(is_bearish))
print("Length of macd_line:", len(macd_line))
print("Length of signal_line:", len(signal_line))
print("Length of macd_histogram:", len(macd_histogram))
print("Length of rsi_values:", len(rsi_values))
print("Length of vi_plus:", len(vi_plus))
print("Length of vi_minus:", len(vi_minus))
print("Length of [close]:", len(df['long_signals']))

df, close = df.align(close, join='inner', axis=0)
df, is_bullish = df.align(is_bullish, join='inner', axis=0)
df, is_bearish = df.align(is_bearish, join='inner', axis=0)
df, macd_line = df.align(macd_line, join='inner', axis=0)
df, signal_line = df.align(signal_line, join='inner', axis=0)
df, macd_histogram = df.align(macd_histogram, join='inner', axis=0)
df, rsi_values = df.align(rsi_values, join='inner', axis=0)
df, vi_plus = df.align(vi_plus, join='inner', axis=0)
df, vi_minus = df.align(vi_minus, join='inner', axis=0)


# Crea un grafico a candele
#mc = mpf.make_marketcolors(up='g', down='r', wick='i', edge='i', volume='in')
#s = mpf.make_mpf_style(marketcolors=mc)

# Filtrare solo i dati che hanno segnali long e short
#long_signals = df[df['long_signals'] == 1]
#short_signals = df[df['short_signals'] == -1]

# Plotta il grafico a candele con segnali
#apds = [
    #mpf.make_addplot(df['SMA'], color='orange'),  # Plotta la SMA
    #mpf.make_addplot(df[df['long_signals'] == -1]['close'], type='scatter', markersize=100, marker='^', color='g'),  # Segnali long
    #mpf.make_addplot(df[df['signal'] == -1]['SMA'], type='scatter', markersize=100, marker='v', color='r')  # Segnali short
#]


#mpf.plot(df, type='candle', style=s, addplot=apds, volume=True, title=f'{symbol} Price with Trading Signals', ylabel='price')
#mpf.plot(df, type='candle', style=s, volume=True, title=f'{symbol} Price with Trading Signals', ylabel='Price')

