import pandas as pd
import yfinance as yf

class CANDLECONDITIONS:

    def __init__(self, period):
        self.period = period