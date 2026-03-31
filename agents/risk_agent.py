from ollama import chat


def risk_agent(market_analysis: str, temperature: float = 0.0) -> str:
    """
    LLM agent with risk assessment role.

    Receives the gold analyst's market assessment and evaluates the level of
    risk associated with entering a trade under current market conditions.

    Args:
        market_analysis: The output from the gold analyst agent.
        temperature: LLM sampling temperature (0.0 = deterministic).

    Returns:
        A string containing the risk assessment.
    """
    response = chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional financial risk assessor specializing in commodity markets. "
                    "Your role is to evaluate the risk of entering a trade based on a provided market analysis. "
                    "Assess the risk level as low, medium, or high, and briefly explain your reasoning. "
                    "Be concise, 2-3 sentences."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Based on the following gold market analysis, assess the risk of entering a trade:\n\n"
                    f"{market_analysis}"
                )
            }
        ],
        options={"temperature": temperature}
    )

    return response.message.content or "Error: No response from risk agent."
