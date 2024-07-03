import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Scarica i dati storici
ticker = 'BTC'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
close = data['Close']

# Parametri del MACD
fast_length = 12
slow_length = 26
signal_smoothing = 9

# Calcolo delle EMA
fast_ema = close.ewm(span=fast_length, adjust=False).mean()
slow_ema = close.ewm(span=slow_length, adjust=False).mean()

# Calcolo del MACD
macd = fast_ema - slow_ema

# Calcolo della linea di segnale
signal = macd.ewm(span=signal_smoothing, adjust=False).mean()

# Calcolo dell'istogramma MACD
histogram = macd - signal

# Aggiungi MACD, segnale e istogramma ai dati
data['MACD'] = macd
data['Signal'] = signal
data['Histogram'] = histogram

# Visualizzazione dei risultati
plt.figure(figsize=(12, 8))

# Grafico del prezzo di chiusura
plt.subplot(2, 1, 1)
plt.plot(data.index, close, label='Close Price')
plt.title(f'{ticker} Close Price & MACD')
plt.legend()

# Grafico del MACD
plt.subplot(2, 1, 2)
plt.plot(data.index, macd, label='MACD', color='blue')
plt.plot(data.index, signal, label='Signal Line', color='red')
plt.bar(data.index, histogram, label='Histogram', color='gray', alpha=0.3)

plt.legend()
plt.tight_layout()
plt.show()
