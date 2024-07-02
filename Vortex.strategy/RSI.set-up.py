import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Scarica i dati storici
ticker = 'AAPL'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
close = data['Close']

# Calcola l'RSI manualmente
rsi_period = 14

# Calcola i guadagni e le perdite
delta = close.diff()
gain = (delta.where(delta > 0, 0)).fillna(0)
loss = (-delta.where(delta < 0, 0)).fillna(0)

# Calcola le medie mobili esponenziali dei guadagni e delle perdite
avg_gain = gain.rolling(window=rsi_period, min_periods=1).mean()
avg_loss = loss.rolling(window=rsi_period, min_periods=1).mean()

# Calcola l'RSI
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))
data['RSI'] = rsi

# Visualizzazione dei risultati
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(data.index, close, label='Close Price')
plt.title(f'{ticker} Close Price')

plt.subplot(2, 1, 2)
plt.plot(data.index, data['RSI'], label='RSI', color='purple')
plt.axhline(70, color='red', linestyle='--', label='Overbought')
plt.axhline(30, color='green', linestyle='--', label='Oversold')
plt.title(f'{ticker} RSI')
plt.legend()

plt.tight_layout()
plt.show()
