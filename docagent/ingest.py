"""
Day 1 — RAG foundation.

Loads PDFs from data/docs/, splits them into chunks, embeds them,
and stores the result in a local ChromaDB collection.

Run once (or whenever you add new PDFs):
    python -m docagent.ingest
"""

from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # must happen before any Google/LangChain imports use the key

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_DIR = "chromadb"          # where ChromaDB persists its files on disk
CHUNK_SIZE = 500                  # tokens per chunk (≈ 375 words)
CHUNK_OVERLAP = 50                # overlap keeps context across chunk boundaries


def load_and_index(docs_dir: str = "data/docs", collection_name: str = "docagent") -> Chroma:
    """Load all PDFs in docs_dir, chunk, embed, and store in ChromaDB."""

    # ── 1. Load every PDF in the folder ──────────────────────────────────────
    pdf_paths = list(Path(docs_dir).glob("*.pdf"))
    if not pdf_paths:
        raise FileNotFoundError(f"No PDFs found in {docs_dir}/")

    all_pages = []
    for path in pdf_paths:
        print(f"  Loading {path.name} …")
        loader = PyPDFLoader(str(path))
        all_pages.extend(loader.load())   # each page = one Document object

    print(f"  Loaded {len(all_pages)} pages from {len(pdf_paths)} PDF(s).")

    # ── 2. Split pages into smaller chunks ───────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(all_pages)
    print(f"  Split into {len(chunks)} chunks.")

    # ── 3. Embed and store in ChromaDB ───────────────────────────────────────
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DIR,
    )
    print(f"  Stored in ChromaDB at ./{CHROMA_DIR}/")
    return vectorstore


if __name__ == "__main__":
    load_and_index()
    print("Indexing complete.")
