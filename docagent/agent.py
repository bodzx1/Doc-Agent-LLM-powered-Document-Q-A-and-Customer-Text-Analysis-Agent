"""
Wires together the LLM, tools, memory, and system prompt into a
single runnable agent.
"""

from langchain.agents import AgentExecutor

def build_agent() -> AgentExecutor:
    """Construct and return the configured AgentExecutor."""
    raise NotImplementedError
