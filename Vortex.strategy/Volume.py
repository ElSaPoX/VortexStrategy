
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Scarica i dati storici
ticker = 'BTC'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
volume = data['Volume']

# Calcola la SMA a 150 giorni del volume
sma_length = 150
data['Volume_SMA'] = volume.rolling(window=sma_length).mean()

# Visualizzazione dei risultati
plt.figure(figsize=(12, 8))

# Grafico del volume
plt.bar(data.index, volume, color='yellow', alpha=0.3, label='Volume')

# Grafico della SMA del volume
plt.plot(data.index, data['Volume_SMA'], color='orange', label=f'{sma_length}-day SMA')

plt.title(f'Volume e {sma_length}-day SMA di {ticker}')
plt.xlabel('Data')
plt.ylabel('Volume')
plt.legend()
plt.show()
