from ollama import chat
from data.gold_market_data import get_market_data

def research_agent(market_summary: str) -> str | None:
    print("Research agent thinking...")
    response = chat(
        model="llama3.1:8b",
        messages=[{
            "role": "user",
            "content": (
                f"You are a gold market analyst. "
                f"Analyze this market data and identify key trading signals. "
                f"Be concise.\n\n{market_summary}"
            )
        }]
        )
    response_content = response.message.content
    if response_content:
        return response_content
    return "Error: No response from research agent."

if __name__ == "__main__":
    from datetime import date
    
    summary = get_market_data(date.today())
    print(summary)
    
    if summary:
        reply = research_agent(summary)
        print(reply)