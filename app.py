"""
Streamlit entry point.

Day 1: simple RAG — retrieve chunks from ChromaDB, pass to Gemini, return answer.
Day 2: swap get_answer() for the full AgentExecutor.
Day 3: add ConversationBufferMemory.

Run with:  streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

from docagent.prompts import SYSTEM_PROMPT

CHROMA_DIR = "chromadb"
COLLECTION_NAME = "docagent"
TOP_K = 3  # number of chunks to retrieve per question


@st.cache_resource
def load_vectorstore() -> Chroma:
    """Load the ChromaDB vectorstore once and reuse across all queries."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


@st.cache_resource
def load_llm() -> ChatGoogleGenerativeAI:
    """Load the Gemini chat model once."""
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def get_answer(question: str, vectorstore: Chroma, llm: ChatGoogleGenerativeAI) -> str:
    """Retrieve relevant chunks then ask the LLM to answer using them."""
    # 1. Embed the question and find the closest chunks in ChromaDB
    docs = vectorstore.similarity_search(question, k=TOP_K)

    # 2. Concatenate chunk texts into a single context block
    context = "\n\n---\n\n".join(doc.page_content for doc in docs)

    # 3. Build the messages: system prompt + context + user question
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context from documents:\n{context}\n\nQuestion: {question}"),
    ]

    # 4. Call Gemini and return the text response
    response = llm.invoke(messages)
    return response.content


# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="DocAgent", page_icon="📄", layout="wide")
st.title("📄 DocAgent")
st.caption("LLM-powered Document Q&A — Day 1: RAG baseline")

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

vectorstore = load_vectorstore()
llm = load_llm()

# Keep conversation history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if question := st.chat_input("Ask something about the documents…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get and show answer
    with st.chat_message("assistant"):
        with st.spinner("Retrieving and reasoning…"):
            answer = get_answer(question, vectorstore, llm)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
