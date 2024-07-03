import ccxt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

# Imposta l'exchange (ad esempio Binance)
exchange = ccxt.binance()

# Lista per memorizzare i dati
timestamps = []
prices = []

# Funzione per ottenere il prezzo corrente di BTC/USD
def get_current_price():
    ticker = exchange.fetch_ticker('BTC/USDT')
    return ticker['last']

# Funzione per aggiornare i dati e il grafico
def update_data(i):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_price = get_current_price()

    timestamps.append(current_time)
    prices.append(current_price)

    # Mantieni solo gli ultimi 20 valori
    if len(timestamps) > 20:
        timestamps.pop(0)
        prices.pop(0)

    ax.clear()
    ax.plot(timestamps, prices, label='BTC/USD')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Bitcoin (BTC) to USD - Real Time Chart')
    plt.ylabel('Price (USD)')
    plt.xlabel('Time')
    plt.legend()
    plt.grid(True)

# Configura il grafico
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_data, interval=2000)  # Aggiorna ogni 2000 ms (2 secondi)

plt.show()
