import ccxt
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Configurazione dell'exchange (Binance in questo caso)
exchange = ccxt.binance()

# Simbolo della criptovaluta (ad esempio, 'BTC/USDT')
symbol = 'BTC/USDT'
timeframe = '8h'  # Intervallo di tempo (15 minuti)


# Funzione per ottenere i dati OHLCV dal mercato
def fetch_ohlcv_data():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    return data


# Funzione di aggiornamento per il grafico
def update_graph(i):
    data = fetch_ohlcv_data()

    ax.clear()
    mpf.plot(data, type='candle', ax=ax, axtitle=f'{symbol} Candlestick Chart')


# Creare la figura del grafico
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_graph, interval=60000)  # Aggiorna ogni minuto

# Mostrare il grafico
plt.show()
