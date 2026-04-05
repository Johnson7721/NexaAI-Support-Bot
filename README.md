# 🤖 RAG Customer Support Chatbot

An AI-powered chatbot that answers questions about your company using Retrieval-Augmented Generation (RAG) with Google Gemini API.

## 📁 Project Structure

```
rag-chatbot/
├── data/
│   └── company_faq.txt          # Your company knowledge base
├── src/
│   ├── load_documents.py        # Step 1: Load & chunk documents
│   ├── create_vectorstore.py    # Step 2: Create embeddings & vector store
│   ├── rag_chain.py             # Step 3: RAG query engine
│   └── app.py                   # Step 4: Streamlit web UI
├── requirements.txt
├── .env.example
├── setup.bat                    # One-click Windows setup
└── README.md
```

## 🚀 Setup Guide (Windows)

### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12
3. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
4. Verify: Open Command Prompt and type:
   ```
   python --version
   ```

### Step 2: Install VS Code

1. Go to https://code.visualstudio.com/
2. Download and install
3. Install the "Python" extension from the Extensions tab (Ctrl+Shift+X)

### Step 3: Open Project in VS Code

1. Open VS Code
2. File → Open Folder → Select the `rag-chatbot` folder
3. Open Terminal in VS Code: Terminal → New Terminal (or Ctrl+`)

### Step 4: Setup Environment

Option A — Run the setup script:
```
setup.bat
```

Option B — Manual setup:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 5: Add Your API Key

1. Copy `.env.example` to `.env`:
   ```
   copy .env.example .env
   ```
2. Open `.env` in VS Code and paste your Gemini API key:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

### Step 6: Run the Chatbot

```
venv\Scripts\activate
streamlit run src/app.py
```

Your browser will open at http://localhost:8501 with your chatbot! 🎉

## 🔧 How It Works

1. **Load Documents** → Reads your company FAQ text file and splits it into chunks
2. **Create Embeddings** → Converts text chunks into numerical vectors using Gemini
3. **Store in Vector DB** → Saves vectors in ChromaDB (local, no server needed)
4. **Query with RAG** → When user asks a question:
   - Finds the most relevant chunks via similarity search
   - Sends those chunks + question to Gemini LLM
   - Returns a grounded, accurate answer

## 📝 Customization

To use your own company data, edit `data/company_faq.txt` with your own Q&A pairs or documentation. Then restart the app.

## 🧠 Skills You'll Learn

- LangChain framework
- Google Gemini API integration
- Text embeddings & vector search
- ChromaDB vector database
- Streamlit web app development
- RAG architecture pattern
