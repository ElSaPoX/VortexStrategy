import yfinance as yf
import matplotlib.pyplot as plt


class VOLUME:

    def __init__(self, period):
        self.period = period

    def calculate(self, volume):

        # Scarica i dati storici
        ticker = 'BTC'
        data = yf.download(ticker, start='2022-01-01', end='2023-01-01')
        volume = data['Volume']

        # Calcola la SMA a 150 giorni del volume
        sma_length = 150

        data['Volume_SMA'] = volume.rolling(window=sma_length).mean()

        return  data['Volume_SMA'], data['Volume']