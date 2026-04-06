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
   - Download and install Ollama from https://ollama.com/download
   - Restart your terminal after installation
   - ollama pull llama3.1:8b  
   Note llama3.1:8b requires ~5GB of disk space and a capable GPU.  
   If your hardware is limited, consider a smaller model such as ollama3.2:1b,  
   though results may differ.

3. Install dependencies
   * Add Python to PATH during installation for the pip3 command to work
   - pip3 install -r requirements.txt

4. Run the agent test & then backtest (see usage segment)

## Usage
Verify that Ollama works and then run the backtest, add --dev for a quicker runtime
- python test_agents.py (~1m runtime)
- python main.py (~3h runtime)
- python main.py --dev (~1h runtime)

Note: You can change the runtime of dev mode by updating DEV_MODE_ROWS in main.py  

Note: This project was developed on Python 3.14.3. 
Compatibility with earlier/later versions is not guaranteed.
