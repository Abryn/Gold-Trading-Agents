# Gold-Trading-Agents
Multi-agent LLM application for gold market trading. Built for experimenting
and comparing LLM-assisted strategies against technical indicator baselines
using historical gold market data.

## Tools Used
- Python, pandas, yfinance, Ollama
- LLM: llama3.1:8b (local via Ollama)
- AI-assisted coding: Claude Code
  
## Requirements
- [Python 3.14.3](https://www.python.org/downloads/release/python-3143/)
- Ollama (see installation step 3)
  
## Installation
1. Clone the repository
   git clone https://github.com/Abryn/Gold-Trading-Agents.git
   cd Gold-Trading-Agents

2. Install dependencies
   pip3 install -r requirements.txt

3. Install and start Ollama
   https://ollama.com/download
   ollama pull llama3.1:8b

4. Run the backtest (see usage segment)

## Usage
python main.py (~3h runtime)
python main.py --dev (~8 min runtime)

Note: This project was developed on Python 3.14.3. 
Compatibility with earlier versions is not guaranteed.
