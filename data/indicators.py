import pandas as pd
from typing import cast


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a raw OHLCV DataFrame and returns it with technical indicator columns appended.

    Added columns:
        rsi_14       - Relative Strength Index (14-period, Wilder's smoothing)
        macd_line    - MACD line (12-period EMA minus 26-period EMA)
        macd_signal  - MACD signal line (9-period EMA of MACD line)
        macd_hist    - MACD histogram (macd_line - macd_signal)
        bb_upper     - Bollinger Band upper (20-period SMA + 2 std dev)
        bb_middle    - Bollinger Band middle (20-period SMA)
        bb_lower     - Bollinger Band lower (20-period SMA - 2 std dev)
    """
    df = df.copy()
    close = cast(pd.Series, df["Close"].squeeze())

    # --- RSI (14-period, Wilder's smoothing) ---
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    # --- MACD (12/26/9) ---
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["macd_line"]   = ema12 - ema26
    df["macd_signal"] = df["macd_line"].ewm(span=9, adjust=False).mean()
    df["macd_hist"]   = df["macd_line"] - df["macd_signal"]

    # --- Bollinger Bands (20-period SMA, 2 standard deviations) ---
    sma20 = close.rolling(window=20).mean()
    std20 = close.rolling(window=20).std()
    df["bb_middle"] = sma20
    df["bb_upper"]  = sma20 + 2 * std20
    df["bb_lower"]  = sma20 - 2 * std20

    return df
