import yfinance as yf

def get_market_data(date) -> str | None:
    data_frame = yf.download(tickers="GC=F", start="2025-01-01", end=date, auto_adjust=True)
    
    if data_frame is None or len(data_frame) < 2:
        return None
    
    close = data_frame["Close"].iloc[-1]
    prev = data_frame["Close"].iloc[-2]
    change = ((close - prev) / prev * 100)

    return (
        f"Gold price: ${float(close.iloc[0]):.2f}/oz. "
        f"Previous close: ${float(prev.iloc[0]):.2f}. "
        f"Day change: {float(change.iloc[0]):.2f}%. "
        f"Recent high: ${data_frame['High'].iloc[-1].item():.2f}. "
        f"Recent low: ${data_frame['Low'].iloc[-1].item():.2f}."
    )