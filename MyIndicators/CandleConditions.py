import pandas as pd

class CANDLECONDITIONS:
    def __init__(self, period=None):
        self.period = period

    def calculate(self, high, low, close, open_):
        # Spostare le serie temporali per ottenere i valori delle candele precedenti
        prev_low = low.shift(1)
        prev2_low = low.shift(2)
        third_last_low = low.shift(3)

        prev_high = high.shift(1)
        prev2_high = high.shift(2)
        third_last_high = high.shift(3)

        prev_close = close.shift(1)
        prev2_close = close.shift(2)
        third_last_close = close.shift(3)

        prev_open = open_.shift(1)
        prev2_open = open_.shift(2)
        third_last_open = open_.shift(3)

        # Definire i pattern candlestick
        def is_bullish():
            return (prev2_low < prev_low) & (prev_low < low) & (prev2_close > close) & (prev_close < close) & (prev_high < close) & (prev2_open < prev_open)

        def is_bearish():
            return (prev2_low > prev_low) & (prev_low > low) & (prev2_close < close) & (prev_close > close) & (prev_high > close)

        # Applicare i pattern ai dati
        data = pd.DataFrame(index=high.index)

        data['BullishC'] = is_bullish()
        data['BearishC'] = is_bearish()

        return data['BullishC'], data['BearishC']
