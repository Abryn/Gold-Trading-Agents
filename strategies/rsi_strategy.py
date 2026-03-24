import pandas as pd
from strategies.base_strategy import BaseStrategy


class RSIStrategy(BaseStrategy):
    """
    RSI-based trading strategy.

    Generates signals based on overbought/oversold thresholds:
        - BUY  when RSI < 30 (oversold)
        - SELL when RSI > 70 (overbought)
        - HOLD otherwise
    """

    def generate_signal(self, row: pd.Series) -> str:
        rsi = row["rsi_14"]
        if rsi < 30:
            return "BUY"
        elif rsi > 70:
            return "SELL"
        return "HOLD"

    def name(self) -> str:
        return "RSI"
        