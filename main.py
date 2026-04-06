import time
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
NUM_LLM_RUNS = 5     # Number of runs to average for LLM strategies (reduces variance from non-determinism)

AVERAGED_METRICS = ["total_return", "win_rate", "profit_factor", "max_drawdown", "sharpe_ratio", "expectancy", "final_value"]


def run_strategy(strategy, df: pd.DataFrame) -> dict:
    """Run a strategy and return results. LLM strategies are run NUM_LLM_RUNS times and averaged."""
    if not isinstance(strategy, LLMStrategy):
        return run_backtest(strategy, df)

    if strategy.temperature == 0.0:
        return run_backtest(strategy, df)

    runs = []
    for i in range(1, NUM_LLM_RUNS + 1):
        print(f"  Run {i}/{NUM_LLM_RUNS}...")
        runs.append(run_backtest(strategy, df))

    averaged = runs[-1].copy()
    for metric in AVERAGED_METRICS:
        averaged[metric] = round(sum(r[metric] for r in runs) / NUM_LLM_RUNS, 4)
    return averaged


def main(dev: bool = False):
    start_time = time.time()
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
        result = run_strategy(strategy, df)
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
    running_time = time.time() - start_time
    print(f"\nResults saved to results.csv")
    print(f"Total runtime: {int(running_time // 60)}m {int(running_time % 60)}s")


if __name__ == "__main__":
    import sys
    main(dev="--dev" in sys.argv)
