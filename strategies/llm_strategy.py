import pandas as pd
from strategies.base_strategy import BaseStrategy
from agents.gold_analyst_agent import gold_analyst_agent
from agents.risk_agent import risk_agent
from agents.trade_decision_agent import trade_decision_agent


class LLMStrategy(BaseStrategy):
    """
    LLM-assisted trading strategy using the multi-agent pipeline.

    Routes each trading day through three sequential agents:
        1. gold_analyst_agent   — analyses raw OHLCV data and produces a market assessment
        2. risk_agent           — evaluates trade risk based on the market assessment
        3. trade_decision_agent — combines both outputs and returns BUY, SELL, or HOLD

    The temperature parameter is passed to all three agents and acts as the
    independent variable in the experiment.
    """

    def __init__(self, temperature: float = 0.0):
        self.temperature = temperature

    def generate_signal(self, row: pd.Series) -> str:
        analysis = gold_analyst_agent(row, temperature=self.temperature)
        risk = risk_agent(analysis, temperature=self.temperature)
        signal = trade_decision_agent(analysis, risk, temperature=self.temperature)
        return signal

    def name(self) -> str:
        return f"LLM (temperature={self.temperature})"
