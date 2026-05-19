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
import docagent.tools as tools

from docagent.prompts import SYSTEM_PROMPT

# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="DocAgent", page_icon="📄", layout="wide")
st.title("📄 DocAgent")
st.caption("LLM-powered Document Q&A — Day 1: RAG baseline")

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()


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
            answer = tools.get_answer(question)  # pass the loaded vectorstore and llm to get_answer
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
