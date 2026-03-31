from data.gold_market_data import load_dataset
from agents.gold_analyst_agent import gold_analyst_agent
from agents.risk_agent import risk_agent
from agents.trade_decision_agent import trade_decision_agent

df = load_dataset()
row = df.iloc[-1]  # Most recent trading day

print("=== Market Data ===")
print(f"Date: {row['Date'].date()} | Close: ${float(row['Close']):.2f}\n")

print("=== Gold Analyst Agent ===")
analysis = gold_analyst_agent(row, temperature=0.0)
print(analysis)

print("\n=== Risk Agent ===")
risk = risk_agent(analysis, temperature=0.0)
print(risk)

print("\n=== Trade Decision Agent ===")
signal = trade_decision_agent(analysis, risk, temperature=0.0)
print(signal)
