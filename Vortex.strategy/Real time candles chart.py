import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf


# Impostazione del client per l'exchange (usiamo Binance come esempio)
exchange = ccxt.binance()


# Funzione per ottenere i dati di Bitcoin/USD (BTC/USDT in Binance)
def fetch_ohlcv():
    # Otteniamo i dati OHLCV (Open, High, Low, Close, Volume)
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='4h')
    # Convertiamo i dati in un DataFrame Pandas
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # Convertiamo i timestamp in un formato leggibile
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


# Inizializzazione del grafico
plt.ion()  # Permette l'aggiornamento interattivo del grafico
fig, ax = plt.subplots()

while True:

    # Otteniamo i dati aggiornati
    df = fetch_ohlcv()

    # Puliamo l'asse per evitare sovrapposizioni
    ax.clear()

    # Tracciamo il grafico candlestick
    mpf.plot(df, type='candle', style='charles', ax=ax)

    # Aggiorniamo il grafico
    plt.pause(60)  # Pausa di 60 secondi per aggiornamenti in tempo reale
