"""
Wires together the LLM, tools, memory, and system prompt into a
single runnable agent.
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
import docagent.prompts as prompts
import docagent.tools as tools

def build_agent() -> AgentExecutor:
    """Construct and return the configured AgentExecutor."""
    prompt=ChatPromptTemplate.from_messages([
        ("system", prompts.SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    agent=create_tool_calling_agent(llm=llm, tools=tools.ALL_TOOLS, prompt=prompt)
    agent_executor=AgentExecutor(agent=agent, tools=tools.ALL_TOOLS, verbose=True)
    return agent_executor
