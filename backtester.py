import pandas as pd
import numpy as np
from strategies.base_strategy import BaseStrategy


def run_backtest(strategy: BaseStrategy, df: pd.DataFrame, initial_cash: float = 10000.0) -> dict:
    """
    Runs a backtest of a strategy against a historical dataset.

    Execution rules:
        - Signal generated on day i is executed at the open price of day i+1.
        - Long only: SELL signals close an open position, they do not open a short.
        - Full position sizing: the entire cash balance is used on a BUY signal.
        - No transaction costs or slippage.

    Args:
        strategy:     A BaseStrategy instance.
        df:           The full historical DataFrame from load_dataset().
        initial_cash: Starting cash balance.

    Returns:
        A dict containing:
            name          - strategy name
            trades        - list of closed trade dicts (entry_date, exit_date, entry_price, exit_price, pnl, pnl_pct)
            final_value   - final portfolio value
            total_return  - total return as a percentage
            win_rate      - proportion of profitable trades
            profit_factor - gross profit / gross loss (inf if no losses)
            max_drawdown  - largest peak-to-trough portfolio value drop as a percentage
            sharpe_ratio  - annualised Sharpe ratio (risk-free rate = 0)
            expectancy    - average pnl per trade
    """
    strategy.on_start(df)

    cash = initial_cash
    position = 0.0
    entry_price = 0.0
    entry_date = None
    trades = []

    portfolio_values = [initial_cash]

    for i in range(len(df) - 1):
        row = df.iloc[i]
        signal = strategy.generate_signal(row)
        next_open = float(df.iloc[i + 1]["Open"])
        next_date = df.iloc[i + 1]["Date"]

        if signal == "BUY" and position == 0.0:
            position = cash / next_open
            entry_price = next_open
            entry_date = next_date
            cash = 0.0

        elif signal == "SELL" and position > 0.0:
            proceeds = position * next_open
            pnl = proceeds - (position * entry_price)
            pnl_pct = (next_open - entry_price) / entry_price * 100
            trades.append({
                "entry_date":  entry_date,
                "exit_date":   next_date,
                "entry_price": entry_price,
                "exit_price":  next_open,
                "pnl":         pnl,
                "pnl_pct":     pnl_pct,
            })
            cash = proceeds
            position = 0.0
            entry_price = 0.0
            entry_date = None

        current_value = cash + position * float(df.iloc[i + 1]["Close"])
        portfolio_values.append(current_value)

    # Close any open position at the last close price
    if position > 0.0:
        last_close = float(df.iloc[-1]["Close"])
        pnl = position * (last_close - entry_price)
        pnl_pct = (last_close - entry_price) / entry_price * 100
        trades.append({
            "entry_date":  entry_date,
            "exit_date":   df.iloc[-1]["Date"],
            "entry_price": entry_price,
            "exit_price":  last_close,
            "pnl":         pnl,
            "pnl_pct":     pnl_pct,
        })
        cash = position * last_close
        position = 0.0

    final_value = cash
    total_return = (final_value - initial_cash) / initial_cash * 100

    # Metrics
    wins  = [t["pnl"] for t in trades if t["pnl"] > 0]
    losses = [t["pnl"] for t in trades if t["pnl"] <= 0]

    win_rate = len(wins) / len(trades) if trades else 0.0

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    expectancy = sum(t["pnl"] for t in trades) / len(trades) if trades else 0.0

    # Max drawdown
    values = np.array(portfolio_values)
    peak = np.maximum.accumulate(values)
    drawdowns = (values - peak) / peak * 100
    max_drawdown = float(np.min(drawdowns))

    # Annualised Sharpe ratio
    daily_returns = np.diff(values) / values[:-1]
    if len(daily_returns) > 1 and np.std(daily_returns) > 0:
        sharpe_ratio = float(np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252))
    else:
        sharpe_ratio = 0.0

    return {
        "name":          strategy.name(),
        "trades":        trades,
        "final_value":   round(final_value, 2),
        "total_return":  round(total_return, 4),
        "win_rate":      round(win_rate, 4),
        "profit_factor": round(profit_factor, 4),
        "max_drawdown":  round(max_drawdown, 4),
        "sharpe_ratio":  round(sharpe_ratio, 4),
        "expectancy":    round(expectancy, 4),
    }
