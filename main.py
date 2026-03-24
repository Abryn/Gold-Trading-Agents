from datetime import date
from data.gold_market_data import get_market_summary
from agents.research_agent import research_agent

if __name__ == "__main__":
    summary = get_market_summary(date.today())
    print(summary)
    
    if summary:
        reply = research_agent(summary)
        print(reply)