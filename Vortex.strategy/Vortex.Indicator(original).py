import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Scarica i dati storici
ticker = 'AAPL'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
high = data['High']
low = data['Low']
close = data['Close']

# lunghezza in giorni
length = 14

# Calcolo dei Movimenti Positivi e Negativi (VM+ e VM-)
vm_plus = abs(high - low.shift(1))
vm_minus = abs(low - high.shift(1))

# Calcolo del True Range (TR)
tr1 = high - low
tr2 = abs(high - close.shift(1))
tr3 = abs(low - close.shift(1))
tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

# Somma dei Movimenti e del True Range
sum_vm_plus = vm_plus.rolling(window=length).sum()
sum_vm_minus = vm_minus.rolling(window=length).sum()
sum_tr = tr.rolling(window=length).sum()

# Calcolo delle Linee VI
vi_plus = sum_vm_plus / sum_tr
vi_minus = sum_vm_minus / sum_tr

# Traccia i risultati
plt.figure(figsize=(10, 6))
plt.axhline(y=1, color='black', linestyle='dashed')
plt.plot(vi_plus, label='VI+', color='green')
plt.plot(vi_minus, label='VI-', color='red')
plt.title(f'Vortex Indicator (VI) di {ticker}')
plt.xlabel('Data')
plt.ylabel('Valore VI')
plt.legend()
plt.show()

