"""
Step 1: Load and chunk documents
This module reads your company FAQ file and splits it into smaller chunks
that can be searched efficiently.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_documents(file_path: str) -> list:
    """
    Load a text file and split it into overlapping chunks.
    
    Why chunk? LLMs have token limits, and smaller chunks allow us to
    find the most relevant piece of information for a question.
    
    Why overlap? So we don't cut important context at chunk boundaries.
    """

    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Create a text splitter
    # - chunk_size: max characters per chunk (500 is good for FAQ-style content)
    # - chunk_overlap: characters shared between consecutive chunks
    # - separators: try to split on these characters first (preserves structure)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )

    # Split text into chunks
    chunks = text_splitter.create_documents([text])

    print(f"[OK] Loaded '{file_path}'")
    print(f"   -> Split into {len(chunks)} chunks")
    print(f"   -> Average chunk size: {sum(len(c.page_content) for c in chunks) // len(chunks)} characters")

    return chunks


# Run this file directly to test: python src/load_documents.py
if __name__ == "__main__":
    chunks = load_and_split_documents("data/company_faq.txt")
    print("\n--- Sample Chunk ---")
    print(chunks[0].page_content)
