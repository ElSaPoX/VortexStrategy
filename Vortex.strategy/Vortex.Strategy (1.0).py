
import yfinance as yf
import matplotlib.pyplot as plt
from MyIndicators import get_indicator




#VORTEX

# Scarica i dati storici
ticker = 'BTC'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
high = data['High']
low = data['Low']
close = data['Close']

# Creiamo una istanza dell'indicatore VI con un periodo di 14
vi = get_indicator('vortex', length=14)

vi_plus, vi_minus = vi.calculate(['High'], ['Low'], ['Close'], ['open'])

print("VI+:", vi_plus)
print("VI-:", vi_minus)





#RSI

# Scarica i dati storici
ticker = 'BTC'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
close = data['Close']

# Calcola l'RSI manualmente
rsi_period = 14

#creiamo istanza indicatore rsi con periodo 14
rsi = get_indicator('rsi', rsi_period=14)

print('rsi', rsi)





#MaCD

# Scarica i dati storici
ticker = 'BTC-USD'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
close = data['Close']

# Crea l'istanza dell'indicatore MACD
MD = get_indicator('macd', fast_length=12, slow_length=26, signal_smoothing=9)

# Calcola il MACD
macd_histogram, signal_line, macd_line = MD.calculate(close)

print('MACD Histogram:', macd_histogram)
print('Signal Line:', signal_line)
print('MACD Line:', macd_line)





#Volume

# Scarica i dati storici
ticker = 'BTC'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
volume = data['Volume']

# Calcola la SMA a 150 giorni del volume
sma_length = 150
data['Volume_SMA'] = volume.rolling(window=sma_length).mean()
volume_sma = volume.rolling(window=sma_length).mean()



#CandleConditions

# Scarica i dati storici
ticker = 'BTC-USD'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
high = data['High']
low = data['Low']
close = data['Close']
open_ = data['Open']

# Crea l'istanza dell'indicatore CandleConditions
candle_conditions = get_indicator('candleconditions')

# Calcola le condizioni delle candele
is_bullish, is_bearish = candle_conditions.calculate(high, low, close, open_)

print('Bullish:', is_bullish)
print('Bearish:', is_bearish)

# Generazione segnali long e short
long_signals = (is_bullish & (volume < volume_sma) & (signal_line < 0) &
                (vi_plus < 1) & (vi_minus > 1) & (rsi<47))

short_signals = (is_bearish & (volume > volume_sma) & (signal_line > 0) &
                 (vi_plus > 1) & (vi_minus < 1) & (rsi>60))

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
ax4.plot(data.index, rsi, label='RSI')
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