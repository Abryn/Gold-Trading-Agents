import pandas as pd
from strategies.base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    """
    MACD crossover trading strategy.

    Generates signals based on the MACD line crossing the signal line:
        - BUY  when MACD line crosses above the signal line
        - SELL when MACD line crosses below the signal line
        - HOLD otherwise
    """

    def on_start(self, df: pd.DataFrame) -> None:
        self._df = df

    def generate_signal(self, row: pd.Series) -> str:
        idx = row.name
        if idx == 0:
            return "HOLD"

        prev = self._df.iloc[idx - 1]

        macd_crossed_above = prev["macd_line"] <= prev["macd_signal"] and row["macd_line"] > row["macd_signal"]
        macd_crossed_below = prev["macd_line"] >= prev["macd_signal"] and row["macd_line"] < row["macd_signal"]

        if macd_crossed_above:
            return "BUY"
        elif macd_crossed_below:
            return "SELL"
        return "HOLD"

    def name(self) -> str:
        return "MACD"
