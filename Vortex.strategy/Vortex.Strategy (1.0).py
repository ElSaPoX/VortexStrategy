
import yfinance as yf
import matplotlib.pyplot as plt
from MyIndicators import get_indicator



# Scarica i dati storici
ticker = 'AAPL'
data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
high = data['High']
low = data['Low']
close = data['Close']

# Creiamo una istanza dell'indicatore VI con un periodo di 14
vi = get_indicator('vortex', length=14)


vi_plus, vi_minus = vi.calculate(['High'], ['Low'], ['Close'])

print("VI+:", vi_plus)
print("VI-:", vi_minus)


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
