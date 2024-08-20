from ..utils import calculate_macd
import pandas as pd

class MACDStrategy:
    def __init__(self, short_window=12, long_window=26, signal_window=9):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        macd, signal = calculate_macd(data['close'], self.short_window, self.long_window, self.signal_window)
        signals['macd'] = macd
        signals['signal_line'] = signal
        signals['signal'] = 0.0
        signals['signal'][macd > signal] = 1.0
        signals['signal'][macd < signal] = -1.0
        return signals

        
