import yfinance as yf
import pandas as pd
from datetime import date
from data.indicators import compute_indicators

# Module-level cache: keyed by (start, end) to avoid re-downloading
_cache: dict[tuple, pd.DataFrame] = {}


def load_dataset(start: str = "2025-01-01", end: str | None = None) -> pd.DataFrame:
    """
    Downloads the full historical GC=F (gold futures) dataset, computes technical
    indicators, drops NaN warm-up rows, and returns the augmented DataFrame.

    Results are cached in memory, repeated calls with the same (start, end)
    return the cached copy instantly without hitting Yahoo Finance again.

    Columns returned:
        OHLCV:      Open, High, Low, Close, Volume
        Indicators: rsi_14, macd_line, macd_signal, macd_hist,
                    bb_upper, bb_middle, bb_lower
    Index: DatetimeIndex (daily trading days)

    Args:
        start: Start date string, e.g. "2025-01-01"
        end:   End date string, e.g. "2026-03-23". Defaults to today if None.
    """
    if end is None:
        end = date.today().isoformat()

    cache_key = (start, end)
    if cache_key in _cache:
        return _cache[cache_key]

    df = yf.download(tickers="GC=F", start=start, end=end, auto_adjust=True)

    if df is None or len(df) < 30:
        raise ValueError(
            f"Insufficient data returned for GC=F ({start} to {end}). "
            "Need at least 30 rows to compute indicators."
        )

    # Flatten MultiIndex columns that yfinance sometimes produces
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = compute_indicators(df)

    # Drop warm-up rows where any indicator is NaN (first ~26 rows)
    indicator_cols = ["rsi_14", "macd_line", "macd_signal", "bb_upper", "bb_lower"]
    df = df.dropna(subset=indicator_cols)

    df = df.reset_index()  # Move Date from index to a regular column

    _cache[cache_key] = df
    return df


def get_market_summary(date) -> str | None:
    """
    Returns a natural-language summary of the most recent trading day's data.
    Kept for backward compatibility with main.py and research_agent.py.
    """
    try:
        df = load_dataset(end=str(date))
    except ValueError:
        return None

    if df is None or len(df) < 2:
        return None

    row = df.iloc[-1]
    prev = df.iloc[-2]

    close = float(row["Close"])
    prev_close = float(prev["Close"])
    change = (close - prev_close) / prev_close * 100

    return (
        f"Gold price: ${close:.2f}/oz. "
        f"Previous close: ${prev_close:.2f}. "
        f"Day change: {change:.2f}%. "
        f"Recent high: ${float(row['High']):.2f}. "
        f"Recent low: ${float(row['Low']):.2f}."
    )
