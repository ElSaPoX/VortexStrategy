import yfinance as yf

from mplchart.chart import Chart
from mplchart.primitives import Candlesticks, Volume
from mplchart.indicators import ROC, SMA, EMA, RSI, MACD

ticker = 'BTC'
prices = yf.Ticker(ticker).history('2y')

max_bars = 250

indicators = [
    Candlesticks(), SMA(50), SMA(200), Volume(),
    RSI(),
    MACD(),
]

chart = Chart(title=ticker, max_bars=max_bars)
chart.plot(prices, indicators)
chart.show()