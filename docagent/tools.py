"""
Day 2 — All five agent tools.

Each function is wrapped with @tool so LangChain can register it with
the AgentExecutor and generate the JSON schema for function-calling.
"""

from langchain.tools import tool

# TODO Day 2: implement all five tools


@tool
def retrieve_docs(query: str) -> str:
    """Search the indexed documents and return the top relevant passages."""
    raise NotImplementedError


@tool
def calculator(expression: str) -> str:
    """Evaluate a safe mathematical expression and return the result."""
    raise NotImplementedError


@tool
def web_search(query: str) -> str:
    """Search the web and return a short summary of results."""
    raise NotImplementedError


@tool
def extract_themes(text: str) -> str:
    """Identify the top recurring themes in the provided customer text."""
    raise NotImplementedError


@tool
def analyze_sentiment(text: str) -> str:
    """Classify the overall sentiment (positive / negative / neutral) of the text."""
    raise NotImplementedError


ALL_TOOLS = [retrieve_docs, calculator, web_search, extract_themes, analyze_sentiment]
