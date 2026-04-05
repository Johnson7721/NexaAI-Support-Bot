"""
Step 2: Create embeddings and store in vector database
This module converts text chunks into numerical vectors (embeddings)
and stores them in ChromaDB for fast similarity search.
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load API key from .env file
load_dotenv()

# Directory to persist the vector database
VECTORSTORE_DIR = "db/chroma_nexa"


def create_vectorstore(chunks: list) -> Chroma:
    """
    Convert text chunks into embeddings and store in ChromaDB.

    What are embeddings?
    - Text converted into a list of numbers (a vector)
    - Similar texts have similar vectors
    - This lets us find relevant chunks by "semantic search"

    What is ChromaDB?
    - A lightweight vector database that runs locally
    - No server setup needed — it saves to a folder on your computer
    - Perfect for learning and prototyping
    """

    # Initialize OpenAI embeddings model
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Create vector store from chunks
    # This will: embed each chunk → store vectors + text in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR,
    )

    print(f"[OK] Vector store created with {len(chunks)} documents")
    print(f"   -> Saved to '{VECTORSTORE_DIR}'")

    return vectorstore


def load_vectorstore() -> Chroma:
    """Load an existing vector store from disk."""

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings,
    )

    print(f"[OK] Loaded vector store from '{VECTORSTORE_DIR}'")
    return vectorstore


# Run this file directly to test: python src/create_vectorstore.py
if __name__ == "__main__":
    from load_documents import load_and_split_documents

    chunks = load_and_split_documents("data/company_faq.txt")
    vectorstore = create_vectorstore(chunks)

    # Test a similarity search
    query = "What is the pricing for NovaCRM?"
    results = vectorstore.similarity_search(query, k=3)
    print(f"\n--- Top 3 results for: '{query}' ---")
    for i, doc in enumerate(results):
        print(f"\n[Result {i+1}]")
        print(doc.page_content[:200] + "...")
