# TechNova RAG Chatbot - Full Documentation

---

## Table of Contents

1. [User Guide](#1-user-guide)
2. [How the System Works](#2-how-the-system-works)
3. [Technologies Used](#3-technologies-used)
4. [Skills & Concepts to Understand](#4-skills--concepts-to-understand)
5. [Project File Structure](#5-project-file-structure)

---

## 1. User Guide

### What is this chatbot?

This is the **TechNova Support Bot** — an AI-powered chatbot that answers customer questions about TechNova's products, billing, and support. It only answers based on the company FAQ document, so its answers are always accurate and grounded in real company information.

---

### How to Start the App

**Step 1 — Open a terminal** (in VS Code: press `Ctrl + backtick`)

**Step 2 — Activate the virtual environment:**
```
source venv/Scripts/activate
```

**Step 3 — Run the app:**
```
streamlit run src/app.py
```

**Step 4 — Open your browser** and go to:
```
http://localhost:8501
```

---

### Using the Chatbot

Once the app is open in your browser:

| Action | How |
|---|---|
| Ask a question | Type in the chat box at the bottom and press Enter |
| Use example questions | Click any button in the left sidebar |
| Ask follow-up questions | Just keep typing — the chat history stays visible |
| Restart the chat | Refresh the browser page |

**Example questions you can ask:**
- What is NovaCRM?
- How much does NovaChat cost?
- How do I reset my password?
- What payment methods do you accept?
- Do you offer refunds?
- What languages does NovaChat support?
- How is my data secured?
- Are you hiring?

---

### What the Chatbot Can and Cannot Answer

| It CAN answer | It CANNOT answer |
|---|---|
| Questions about TechNova products | General knowledge (e.g., "What is AI?") |
| Pricing and billing questions | Questions not in the FAQ file |
| Password reset and technical support | Real-time data (e.g., live order status) |
| Contact information | Personal account lookups |

If a question is not in the FAQ, the bot will say: *"I'm sorry, I don't have information about that. Please contact support@technova.com"*

---

### How to Update the Knowledge Base

1. Open `data/company_faq.txt`
2. Add or edit the content (use `##` for section headings)
3. Delete the `db/chroma` folder (this is the old knowledge base)
4. Restart the app — it will rebuild automatically

---

## 2. How the System Works

This chatbot uses a technique called **RAG (Retrieval-Augmented Generation)**. Here is the step-by-step flow of what happens when a user asks a question:

```
User types question
        |
        v
[Step 1] Convert question into an embedding (a list of numbers)
        |
        v
[Step 2] Search ChromaDB for the most similar text chunks from the FAQ
        |
        v
[Step 3] Take the top 4 matching chunks as "context"
        |
        v
[Step 4] Send context + question to GPT-4o-mini
        |
        v
[Step 5] GPT generates an answer based ONLY on the context
        |
        v
Answer displayed in the chat
```

### Why RAG instead of just asking ChatGPT directly?

| Direct ChatGPT | RAG Chatbot |
|---|---|
| Uses general internet knowledge | Uses only YOUR company data |
| May hallucinate (make things up) | Grounded answers, less hallucination |
| Cannot know your company's details | Knows your products, pricing, policies |
| Same for everyone | Customized per company |

---

### The 4 Source Files Explained

#### `src/load_documents.py` — Step 1: Load & Chunk
Reads `data/company_faq.txt` and splits it into small overlapping pieces called **chunks**.
- Each chunk is ~500 characters
- Chunks overlap by 100 characters so context is not lost at boundaries

#### `src/create_vectorstore.py` — Step 2: Create Embeddings & Save
Converts each chunk into a **vector (embedding)** using OpenAI's `text-embedding-3-small` model and saves everything into **ChromaDB** (a local database stored in the `db/chroma` folder).

#### `src/rag_chain.py` — Step 3: Query Engine
When a user asks a question:
1. Converts the question into an embedding
2. Searches ChromaDB for the 4 most similar chunks
3. Sends those chunks + question to **GPT-4o-mini**
4. Returns the answer

#### `src/app.py` — Step 4: Web Interface
Builds the chat UI using **Streamlit**. Handles the chat history, sidebar buttons, and connects everything together.

---

## 3. Technologies Used

### Python
The programming language the entire project is built in.
- Version: 3.11 or 3.12
- Why: Most popular language for AI/ML projects

---

### LangChain (`langchain`, `langchain-openai`, `langchain-community`)
A framework that connects AI models with data and tools.
- Used for: building the RAG pipeline, connecting to OpenAI, splitting text
- Think of it as: the "glue" that connects all the pieces together
- Website: langchain.com

---

### OpenAI API (`langchain-openai`)
The AI brain of the chatbot. Two models are used:

| Model | Purpose |
|---|---|
| `text-embedding-3-small` | Converts text into vectors (numbers) for search |
| `gpt-4o-mini` | Reads the context and generates the answer |

- Requires: `OPENAI_API_KEY` in the `.env` file
- Cost: Pay-per-use (very cheap for small projects)

---

### ChromaDB (`chromadb`, `langchain-chroma`)
A local vector database that stores the embeddings.
- Used for: saving and searching text vectors
- Stored in: `db/chroma/` folder on your computer
- Why ChromaDB: No server needed, runs fully local, free

---

### Streamlit (`streamlit`)
A Python library that turns Python scripts into web apps.
- Used for: the chat UI in the browser
- Why: Very fast to build, no HTML/CSS/JavaScript needed
- Run with: `streamlit run src/app.py`

---

### python-dotenv (`python-dotenv`)
Loads environment variables from the `.env` file.
- Used for: keeping the API key secret (not hardcoded in code)
- The `.env` file contains: `OPENAI_API_KEY=your-key-here`

---

### LangChain Text Splitters (`langchain-text-splitters`)
Splits long documents into smaller chunks.
- Used for: breaking `company_faq.txt` into 500-character pieces
- Uses: `RecursiveCharacterTextSplitter`

---

## 4. Skills & Concepts to Understand

### RAG (Retrieval-Augmented Generation)
The core concept of this project.
- **Retrieval**: Find the most relevant information from your data
- **Augmented**: Add that information to the prompt
- **Generation**: LLM generates an answer using that information
- Used by: Google, Microsoft, Amazon in their AI products

---

### Embeddings & Vector Search
- An **embedding** is a list of numbers that represents the meaning of text
- Similar sentences have similar numbers (vectors)
- **Vector search** finds the most similar vectors to a query
- Example: "password reset" and "forgot my password" are similar even though the words differ

---

### LLM (Large Language Model)
- The AI model that reads text and generates human-like responses
- This project uses **GPT-4o-mini** from OpenAI
- The LLM does NOT search the database — it only reads what you give it

---

### Prompt Engineering
- The chatbot uses a carefully written **system prompt** to control behavior
- The prompt tells GPT: "Only answer from the context below. If not found, say you don't know."
- This prevents the bot from making up answers

---

### Vector Database
- A special database designed to store and search embeddings
- Normal databases search by exact match (SQL)
- Vector databases search by **similarity** (semantic search)
- This project uses **ChromaDB** as the vector database

---

### Virtual Environment (venv)
- An isolated Python environment for this project
- Keeps project dependencies separate from other Python projects
- Activated with: `source venv/Scripts/activate`

---

### Environment Variables (.env)
- A file that stores secret keys outside of the code
- The `.env` file is in `.gitignore` so it is never uploaded to GitHub
- Always keep your API keys in `.env`, never hardcode them

---

## 5. Project File Structure

```
rag-chatbot/
|
|-- data/
|   `-- company_faq.txt          # The knowledge base (edit this to change what the bot knows)
|
|-- src/
|   |-- load_documents.py        # Step 1: Read and chunk the FAQ file
|   |-- create_vectorstore.py    # Step 2: Create embeddings and save to ChromaDB
|   |-- rag_chain.py             # Step 3: Connect vector search to GPT
|   `-- app.py                   # Step 4: Streamlit web interface
|
|-- db/
|   `-- chroma/                  # Auto-generated: stores the vector database locally
|
|-- docs/
|   `-- documentation.md         # This file
|
|-- venv/                        # Auto-generated: Python virtual environment
|-- .env                         # Your secret API key (never share this)
|-- .env.example                 # Template showing what .env should look like
|-- requirements.txt             # List of Python packages needed
|-- setup.bat                    # One-click Windows setup script
`-- README.md                    # Quick start guide
```

---

*Documentation written for TechNova RAG Chatbot project.*
