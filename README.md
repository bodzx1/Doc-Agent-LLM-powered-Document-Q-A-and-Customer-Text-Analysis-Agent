# DocAgent

> LLM-powered Document Q&A and Customer-Text Analysis Agent

_Demo GIF, architecture diagram, eval results, and design decisions will be added on Day 3._

## Stack
Python · LangChain · OpenAI API · ChromaDB · Streamlit

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
python -m docagent.ingest
streamlit run app.py
```

## Project structure

```
docagent/          # core package
  ingest.py        # PDF → chunks → ChromaDB
  tools.py         # 5 agent tools
  agent.py         # AgentExecutor
  memory.py        # ConversationBufferMemory
  prompts.py       # system prompt
data/              # sample PDFs and reviews CSV
eval/              # eval harness + results
app.py             # Streamlit UI
```
