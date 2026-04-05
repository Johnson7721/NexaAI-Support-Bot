"""
Step 4: Streamlit Web App - Enhanced Version
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.load_documents import load_and_split_documents
from src.create_vectorstore import create_vectorstore, load_vectorstore, VECTORSTORE_DIR
from src.rag_chain import create_rag_chain

load_dotenv()

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="NexaAI Support Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Custom CSS
# ============================================
st.markdown(
    """
    <style>
    .main-header { text-align: center; padding: 1rem 0; }
    .main-header h1 { color: #1a73e8; }
    .status-box {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .status-success {
        background-color: #e6f4ea;
        border: 1px solid #34a853;
        color: #137333;
    }
    .status-error {
        background-color: #fce8e6;
        border: 1px solid #ea4335;
        color: #c5221f;
    }
    .source-tag {
        background-color: #e8f0fe;
        color: #1a73e8;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        margin-right: 4px;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================
# Header
# ============================================
st.markdown(
    """
    <div class="main-header">
        <h1>🤖 NexaAI Support Bot</h1>
        <p>Ask me anything about NexaAI's products, billing, and support!</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================
# Initialize RAG system
# ============================================
@st.cache_resource(show_spinner="Setting up AI knowledge base...")
def initialize_rag():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        return None, None, None, "Please add your OpenAI API key to the .env file"
    try:
        if os.path.exists(VECTORSTORE_DIR):
            vectorstore = load_vectorstore()
        else:
            faq_path = os.path.join(os.path.dirname(__file__), "..", "data", "company_faq.txt")
            chunks = load_and_split_documents(faq_path)
            vectorstore = create_vectorstore(chunks)
        chain, retriever, llm = create_rag_chain(vectorstore)
        return chain, retriever, llm, None
    except Exception as e:
        return None, None, None, f"Error: {str(e)}"


chain, retriever, llm, error = initialize_rag()

if error:
    st.markdown(
        f'<div class="status-box status-error">{error}</div>',
        unsafe_allow_html=True,
    )
    st.stop()
else:
    st.markdown(
        '<div class="status-box status-success">Knowledge base loaded and ready!</div>',
        unsafe_allow_html=True,
    )


# ============================================
# Helper Functions
# ============================================
def extract_sources(docs):
    """Extract section headings from retrieved document chunks."""
    sources = []
    for doc in docs:
        for line in doc.page_content.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                source = line.lstrip("#").strip()
                if source and source not in sources:
                    sources.append(source)
                break
    return sources if sources else ["Knowledge Base"]


def generate_followups(question, answer):
    """Use LLM to suggest 2 follow-up questions based on the current Q&A."""
    try:
        from langchain_core.messages import HumanMessage
        msg = (
            f"Suggest 2 short follow-up questions a customer might ask after this exchange.\n"
            f"Return only the questions, one per line, no numbering, no extra text.\n\n"
            f"Question: {question}\nAnswer: {answer}"
        )
        response = llm.invoke([HumanMessage(content=msg)])
        questions = [q.strip() for q in response.content.strip().split("\n") if q.strip()]
        return questions[:2]
    except Exception:
        return []


def export_chat():
    """Format chat history as plain text for download."""
    lines = []
    for m in st.session_state.messages:
        role = "You" if m["role"] == "user" else "Bot"
        lines.append(f"{role}: {m['content']}")
        if m.get("sources"):
            lines.append(f"  [Source: {', '.join(m['sources'])}]")
        lines.append("")
    return "\n".join(lines)


# ============================================
# Session State Initialization
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! 👋 I'm the NexaAI support bot. I can help you with questions about our products (NexaCRM, NexaChat, NexaAnalytics), billing, technical support, and more. What would you like to know?",
            "sources": [],
            "followups": [],
        }
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = {}
if "question_count" not in st.session_state:
    st.session_state.question_count = 0


# ============================================
# Sidebar
# ============================================
with st.sidebar:

    # Stats
    st.markdown("### 📊 Stats")
    st.metric("Questions Asked", st.session_state.question_count)
    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hi! 👋 I'm the NexaAI support bot. How can I help you today?",
                    "sources": [],
                    "followups": [],
                }
            ]
            st.session_state.feedback = {}
            st.session_state.question_count = 0
            st.rerun()
    with col2:
        st.download_button(
            "💾 Export",
            data=export_chat(),
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")

    # Sample questions by category
    st.markdown("### 💡 Sample Questions")
    st.caption("Click any question to get an answer.")

    categories = {
        "🛍️ Products": [
            "What is NexaCRM?",
            "What is NexaChat?",
            "What is NexaAnalytics?",
            "What languages does NexaChat support?",
        ],
        "💳 Billing & Pricing": [
            "How much does NexaCRM cost?",
            "How much does NexaChat cost?",
            "What payment methods do you accept?",
            "Do you offer refunds?",
            "How do I cancel my subscription?",
        ],
        "🔧 Technical Support": [
            "How do I reset my password?",
            "How is my data secured?",
            "What browsers does NexaCRM support?",
            "How do I access the API?",
        ],
        "🏢 Company": [
            "Where is NexaAI located?",
            "Are you hiring?",
            "How do I contact support?",
        ],
    }

    for category, questions in categories.items():
        with st.expander(category):
            for q in questions:
                if st.button(q, use_container_width=True, key=q):
                    st.session_state.pending_question = q
                    st.rerun()


# ============================================
# Chat History Display
# ============================================
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Source tags (assistant only)
        if message["role"] == "assistant" and message.get("sources"):
            source_html = " ".join(
                f'<span class="source-tag">{s}</span>' for s in message["sources"]
            )
            st.markdown(f"**Source:** {source_html}", unsafe_allow_html=True)

        # Follow-up suggestions (last assistant message only)
        if (
            message["role"] == "assistant"
            and i == len(st.session_state.messages) - 1
            and message.get("followups")
        ):
            st.markdown("**You might also ask:**")
            for fq in message["followups"]:
                if st.button(fq, key=f"fq_{i}_{fq}", use_container_width=False):
                    st.session_state.pending_question = fq
                    st.rerun()

        # Feedback buttons (all assistant messages except welcome)
        if message["role"] == "assistant" and i > 0:
            fb1, fb2, _ = st.columns([1, 1, 10])
            with fb1:
                if st.button("👍", key=f"up_{i}", help="Helpful"):
                    st.session_state.feedback[i] = "up"
            with fb2:
                if st.button("👎", key=f"down_{i}", help="Not helpful"):
                    st.session_state.feedback[i] = "down"

            if st.session_state.feedback.get(i) == "up":
                st.caption("Thanks for the feedback! 😊")
            elif st.session_state.feedback.get(i) == "down":
                st.caption("Thanks! We'll work on improving.")


# ============================================
# Handle Input: Chat box or Sidebar button
# ============================================
prompt = st.chat_input("Ask a question about NexaAI...")

if not prompt and "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")

if prompt:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "sources": [], "followups": []}
    )
    st.session_state.question_count += 1

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and stream assistant response
    with st.chat_message("assistant"):

        # Retrieve source docs first
        with st.spinner("Searching knowledge base..."):
            source_docs = retriever.invoke(prompt)
            sources = extract_sources(source_docs)

        # Stream the response
        response = st.write_stream(chain.stream(prompt))

        # Show sources
        source_html = " ".join(
            f'<span class="source-tag">{s}</span>' for s in sources
        )
        st.markdown(f"**Source:** {source_html}", unsafe_allow_html=True)

        # Generate follow-up suggestions
        with st.spinner("Generating suggestions..."):
            followups = generate_followups(prompt, response)

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "sources": sources,
            "followups": followups,
        }
    )

    st.rerun()
