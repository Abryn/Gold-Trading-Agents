import pandas as pd
from ollama import chat


def gold_analyst_agent(row: pd.Series, temperature: float = 0.0) -> str:
    """
    LLM agent with gold market analysis role.

    Receives raw OHLCV data for a single trading day and returns a natural-language
    market analysis for use by downstream agents (risk and trade decision).

    Only raw price and volume data is provided, no pre-computed technical
    indicators so that the LLM reasons independently from the indicator-based strategies.

    Args:
        row: A pandas Series containing OHLCV columns.
        temperature: LLM sampling temperature (0.0 = deterministic).

    Returns:
        A string containing the analyst's market assessment.
    """
    open_price = float(row["Open"])
    high_price = float(row["High"])
    low_price = float(row["Low"])
    close_price = float(row["Close"])
    volume = int(row["Volume"])
    day_change = ((close_price - open_price) / open_price) * 100
    candle_range = high_price - low_price

    market_context = (
        f"Date: {row['Date'].date()}\n"
        f"Open: ${open_price:.2f} | High: ${high_price:.2f} | Low: ${low_price:.2f} | Close: ${close_price:.2f}\n"
        f"Day change: {day_change:+.2f}%\n"
        f"Candle range: ${candle_range:.2f}\n"
        f"Volume: {volume:,}"
    )

    response = chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert gold market analyst. "
                    "Your role is to analyze raw gold futures price data and provide a concise market assessment. "
                    "Analyze ONLY the data provided. Do not invent or assume any information not present in the data. "
                    "Focus on price action and market conditions based solely on the OHLCV values given. "
                    "Be concise, 2-3 sentences."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following gold market data and provide a brief market assessment:\n\n"
                    f"{market_context}"
                )
            }
        ],
        options={"temperature": temperature}
    )

    return response.message.content or "Error: No response from gold analyst agent."
