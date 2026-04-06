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
   - git clone https://github.com/Abryn/Gold-Trading-Agents.git  
   - cd Gold-Trading-Agents
  
2. Install and start Ollama  
   https://ollama.com/download
   * After installation, restart your terminal properly for the ollama command to work
   - ollama pull llama3.1:8b

3. Install dependencies
   * Add Python to PATH during installation for the pip3 command to work (if missed add it by updating your environment variables)
   - pip3 install -r requirements.txt

4. Run the agent test & then backtest (see usage segment)

## Usage
* Verify that Ollama works and then run the backtest, add --dev for a quicker runtime
- python test_agents.py (~1m runtime)
- python main.py (~3h runtime)
- python main.py --dev (~1h runtime)

Note: This project was developed on Python 3.14.3. 
Compatibility with earlier/later versions is not guaranteed.
