"""
Step 3: RAG Query Chain
This is the brain of the chatbot — it connects the vector store to the LLM
to generate grounded, accurate answers.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def format_docs(docs: list) -> str:
    """Format retrieved documents into a single string for the prompt."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(vectorstore):
    """
    Create a RAG chain that:
    1. Takes a user question
    2. Retrieves relevant chunks from the vector store
    3. Sends the chunks + question to GPT-4o-mini
    4. Returns a grounded answer

    Returns: (chain, retriever, llm)
    """

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3,
    )

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful customer support assistant for NexaAI.
Answer the customer's question based ONLY on the following context.
If the answer is not in the context, say "I'm sorry, I don't have information about that. Please contact support@nexaai.com for further assistance."

Be friendly, professional, and concise.

Context:
{context}

Customer Question: {question}

Answer:"""
    )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever, llm


# Run this file directly to test: python src/rag_chain.py
if __name__ == "__main__":
    from load_documents import load_and_split_documents
    from create_vectorstore import create_vectorstore, load_vectorstore

    if os.path.exists("db/chroma"):
        vectorstore = load_vectorstore()
    else:
        chunks = load_and_split_documents("data/company_faq.txt")
        vectorstore = create_vectorstore(chunks)

    chain, retriever, llm = create_rag_chain(vectorstore)

    test_questions = [
        "What is the pricing for NovaCRM?",
        "How do I reset my password?",
    ]

    for question in test_questions:
        print(f"\n? {question}")
        answer = chain.invoke(question)
        print(f"  {answer}")
        print("-" * 60)
