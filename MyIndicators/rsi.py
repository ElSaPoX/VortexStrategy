import yfinance as yf
import matplotlib.pyplot as plt

class RSI:

    def __init__(self, period):
        self.period = period