from ollama import chat


def trade_decision_agent(market_analysis: str, risk_assessment: str, temperature: float = 0.0) -> str:
    """
    LLM agent with trade decision role.

    Receives the market assessment and the risk assessment, 
    and returns a trade signal of BUY, SELL, or HOLD.

    If the response cannot be parsed as one of the three valid signals,
    HOLD is returned as a safe fallback.

    Args:
        market_analysis: The output from the gold analyst agent.
        risk_assessment: The output from the risk agent.
        temperature: LLM sampling temperature (0.0 = deterministic).

    Returns:
        One of the strings: "BUY", "SELL", or "HOLD"
    """
    response = chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a gold futures trader. "
                    "You will be given a market analysis and a risk assessment. "
                    "Based on this information, decide whether to BUY, SELL, or HOLD. "
                    "You must respond with exactly one word: BUY, SELL, or HOLD. "
                    "Do not include any explanation or additional text."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Market analysis:\n{market_analysis}\n\n"
                    f"Risk assessment:\n{risk_assessment}\n\n"
                    f"What is your trading decision? Respond with BUY, SELL, or HOLD only."
                )
            }
        ],
        options={"temperature": temperature}
    )

    content = response.message.content or ""
    signal = content.strip().upper()
    
    if signal in ("BUY", "SELL", "HOLD"):
        return signal
    return "HOLD"
