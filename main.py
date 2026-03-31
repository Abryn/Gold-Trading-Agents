import pandas as pd
from data.gold_market_data import load_dataset
from backtester import run_backtest
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.bollinger_strategy import BollingerStrategy
from strategies.llm_strategy import LLMStrategy

TEMPERATURES = [0.0, 0.2, 0.5, 0.8, 1.0]

STRATEGIES = [
    RSIStrategy(),
    MACDStrategy(),
    BollingerStrategy(),
    *[LLMStrategy(temperature=t) for t in TEMPERATURES],
]

DEV_MODE_ROWS = 100  # Number of most recent trading days to use in dev mode (lower=faster)


def main(dev: bool = False):
    print("Loading dataset...")
    df = load_dataset()

    if dev:
        df = df.tail(DEV_MODE_ROWS).reset_index(drop=True)
        print(f"DEV MODE: using last {DEV_MODE_ROWS} trading days\n")
    else:
        print(f"Dataset loaded: {len(df)} trading days\n")

    results = []
    for strategy in STRATEGIES:
        print(f"Running: {strategy.name()}")
        result = run_backtest(strategy, df)
        results.append(result)
        print(f"  Return: {result['total_return']}% | Win rate: {result['win_rate']} | "
              f"Sharpe: {result['sharpe_ratio']} | Max drawdown: {result['max_drawdown']}%\n")

    # Results table
    summary = pd.DataFrame([{
        "Strategy":      r["name"],
        "Total Return %": r["total_return"],
        "Win Rate":      r["win_rate"],
        "Profit Factor": r["profit_factor"],
        "Max Drawdown %": r["max_drawdown"],
        "Sharpe Ratio":  r["sharpe_ratio"],
        "Expectancy":    r["expectancy"],
        "# Trades":      len(r["trades"]),
    } for r in results])

    print(summary.to_string(index=False))

    summary.to_csv("results.csv", index=False)
    print("\nResults saved to results.csv")


if __name__ == "__main__":
    import sys
    main(dev="--dev" in sys.argv)
