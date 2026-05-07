"""
Day 3 — Conversation memory.

Wraps ConversationBufferMemory so the agent remembers prior turns
within a single session.
"""

from langchain.memory import ConversationBufferMemory

# TODO Day 3: instantiate and expose memory


def get_memory() -> ConversationBufferMemory:
    """Return a fresh ConversationBufferMemory tied to the agent's input/output keys."""
    raise NotImplementedError
