import yfinance as yf
import matplotlib.pyplot as plt

class MACD:

    def __init__(self, period):
        self.period = period