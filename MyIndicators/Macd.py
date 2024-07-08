import yfinance as yf
import matplotlib.pyplot as plt


class MACD:
    def __init__(self, fast_length=12, slow_length=26, signal_smoothing=9):
        self.fast_length = fast_length
        self.slow_length = slow_length
        self.signal_smoothing = signal_smoothing

    def calculate(self, close):
        # Utilizza i parametri inizializzati
        fast_length = self.fast_length
        slow_length = self.slow_length
        signal_smoothing = self.signal_smoothing

        # Calcolo delle EMA
        fast_ema = close.ewm(span=fast_length, adjust=False).mean()
        slow_ema = close.ewm(span=slow_length, adjust=False).mean()

        # Calcolo del MACD
        macd_line = fast_ema - slow_ema

        # Calcolo della linea di segnale
        signal_line = macd_line.ewm(span=signal_smoothing, adjust=False).mean()

        # Calcolo dell'istogramma MACD
        macd_histogram = macd_line - signal_line

        return macd_histogram, signal_line, macd_line
