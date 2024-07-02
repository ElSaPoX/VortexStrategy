
from .rsi import RSI
from .Volume import VOLUME
from .Vortex import VORTEX
from .macd import MACD
from .CandleConditions import CANDLECONDITIONS

# Mappa delle parole chiave agli indicatori
INDICATORS = {
    'rsi': RSI,
    'volume': VOLUME,
    'vortex': VORTEX,
    'macd': MACD,
    'candleConditions': CANDLECONDITIONS
}

def get_indicator(name, *args, **kwargs):
    indicator_class = INDICATORS.get(name.lower())
    if indicator_class:
        return indicator_class(*args, **kwargs)
    else:
        raise ValueError(f"Indicator '{name}' not found.")
