from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Abstract base class that all trading strategies must implement.

    Both technical indicator strategies and the LLM-assisted strategy implement
    this interface, allowing the backtesting engine to be completely strategy-agnostic.
    """

    @abstractmethod
    def generate_signal(self, row: pd.Series) -> str:
        """
        Given a single row of OHLCV + indicator data for one trading day,
        return a trading signal.

        Args:
            row: A pandas Series with columns including Close, Open, High, Low,
                 rsi_14, macd_line, macd_signal, macd_hist, bb_upper, bb_middle, bb_lower.

        Returns:
            One of: "BUY", "SELL", "HOLD"
        """

    def on_start(self, df: pd.DataFrame) -> None:
        """
        Called once before the backtesting loop with the full DataFrame.

        Optional hook — default is no-op. Used by stateful strategies (e.g. MACD)
        to reset internal state between runs, and by the LLM strategy to store
        a reference to the full DataFrame for lookback windowing.

        Args:
            df: The full historical DataFrame that will be iterated.
        """

    @abstractmethod
    def name(self) -> str:
        """
        Human-readable strategy name used in results tables and CSV output.
        """
