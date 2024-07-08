import yfinance as yf
import matplotlib.pyplot as plt

class RSI:
    def __init__(self, rsi_period):
        self.rsi_period = rsi_period

    def calculate(self, close):

        # Scarica i dati storici
        ticker = 'BTC'
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

        return data['RSI']