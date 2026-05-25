"""
Day 2 — All five agent tools.

Each function is wrapped with @tool so LangChain can register it with
the AgentExecutor and generate the JSON schema for function-calling.
"""

from langchain.tools import tool
from langchain.schema import HumanMessage, SystemMessage
import numexpr
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
import docagent.prompts as prompts

CHROMA_DIR = "chromadb"
COLLECTION_NAME = "docagent"



TOP_K = 3 # number of chunks to retrieve per question

"""Load the ChromaDB vectorstore once and reuse across all queries."""
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
_vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
"""Load the Gemini chat model once."""
_llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def get_context(query: str) -> str:
    """Helper function to retrieve relevant chunks from ChromaDB for a given query."""
    # 1. Embed the question and find the closest chunks in ChromaDB
    docs = _vectorstore.similarity_search(query, k=TOP_K)
    # 2. Concatenate chunk texts into a single context block
    context = "\n\n---\n\n".join(doc.page_content for doc in docs)
    return context



def get_answer(question: str,prompt: str) -> str:
    if prompt == prompts.RAG_PROMPT:
        context = get_context(question)  # only retrieve context for RAG prompt, not for tools that analyze customer text
    else:
        context = ""  # for non-RAG prompts, we don't have a context to pass in, but get_answer still expects a string, so passing empty string 
    # 3. Build the messages: system prompt + context + user question
    human_content = f"Context from documents:\n{context}\n\nQuestion: {question}" if context else question
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=human_content),
    ]
    response = _llm.invoke(messages)
    return response.content


@tool
def retrieve_docs(query: str) -> str:
    """Search the indexed documents and return the top relevant passages."""
    return get_answer(query, prompts.RAG_PROMPT)  # use the RAG-specific prompt that instructs the agent to answer only from the retrieved context

@tool
def calculator(expression: str) -> str:
    """Evaluate a safe mathematical expression and return the result."""
    return str(numexpr.evaluate(expression))  # numexpr safely evaluates math expressions only, no random code execution  


@tool
def web_search(query: str) -> str:
    """Search the web and return a short summary of results."""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
        # results is a list of dicts: [{"title": ..., "href": ..., "body": ...}, ...]
        # agent expects a single string back, so formatting each result as readable text
        return "\n\n".join(
            f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}"
            for r in results
        )
    except DuckDuckGoSearchException:
        return "Web search is temporarily rate-limited. Try again in a few seconds."


@tool
def extract_themes(text: str) -> str:
    """Identify the top recurring themes in the provided customer text."""
    return get_answer(text, prompts.EXTRACT_THEMES_PROMPT)


@tool
def analyze_sentiment(text: str) -> str:
    """Classify the overall sentiment (positive / negative / neutral) of the text."""
    return get_answer(text, prompts.ANALYZE_SENTIMENT_PROMPT)


ALL_TOOLS = [retrieve_docs, calculator, web_search, extract_themes, analyze_sentiment]
