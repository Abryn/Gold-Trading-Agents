from ollama import chat

def research_agent(market_summary: str) -> str | None:
    print("Research agent thinking...")
    response = chat(
        model="llama3.1:8b",
        messages=[{
            "role": "user",
            "content": (
                f"You are a gold market analyst. "
                f"Analyze ONLY the data provided below. "
                f"Do not invent or assume indicators not present in the data. "
                f"Identify key trading signals and give a single clear recommendation. "
                f"Be concise.\n\n{market_summary}"
            )
        }],
        options={"temperature": 0}
        )
    response_content = response.message.content
    if response_content:
        return response_content
    return "Error: No response from research agent."