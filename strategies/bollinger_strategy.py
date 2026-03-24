import pandas as pd
from strategies.base_strategy import BaseStrategy


class BollingerStrategy(BaseStrategy):
    """
    Bollinger Bands trading strategy.

    Generates signals based on price relative to the bands:
        - BUY  when Close price touches or breaks below the lower band
        - SELL when Close price touches or breaks above the upper band
        - HOLD otherwise
    """

    def generate_signal(self, row: pd.Series) -> str:
        close = row["Close"]
        if close <= row["bb_lower"]:
            return "BUY"
        elif close >= row["bb_upper"]:
            return "SELL"
        return "HOLD"

    def name(self) -> str:
        return "Bollinger Bands"
