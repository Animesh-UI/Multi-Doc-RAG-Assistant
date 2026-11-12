# app.py
import streamlit as st
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, LLM_MODEL, FALLBACK_MESSAGE
from ingest import load_and_split_pdfs
from vectorstore import build_vectorstore
from memory import create_memory
from rag_chain import answer_question
from guardrails import NO_SOURCES_FOUND, validate_question

# ------------------------------------------------------------------
# Page Config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Multi‑Document RAG Assistant",
    page_icon="📚",
    layout="centered",
)

st.title("📚 Multi‑Document RAG Assistant")
st.caption(
    "Upload multiple PDFs, ask questions in natural language, "
    "and get grounded answers with source citations."
)

# ------------------------------------------------------------------
# Session State Initialisation
# ------------------------------------------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "memory" not in st.session_state:
    st.session_state.memory = create_memory()
if "messages" not in st.session_state:
    st.session_state.messages = []          # list of (role, content, sources)
if "docs_ready" not in st.session_state:
    st.session_state.docs_ready = False

# ------------------------------------------------------------------
# Sidebar – Document Upload & Processing
# ------------------------------------------------------------------
with st.sidebar:
    st.header("📂 Document Library")

    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("⚙️ Process Documents", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            with st.spinner("Loading, chunking, and embedding PDFs…"):
                chunks = load_and_split_pdfs(uploaded_files)
                if not chunks:
                    st.error("Could not extract any text from the uploaded PDFs.")
                else:
                    st.session_state.vectorstore = build_vectorstore(chunks)
                    # Reset memory when a new document set is loaded
                    st.session_state.memory = create_memory()
                    st.session_state.messages = []
                    st.session_state.docs_ready = True
                    st.success(
                        f"✅ Processed {len(uploaded_files)} PDF(s) "
                        f"into {len(chunks)} chunks."
                    )

    if st.button("🗑️ Clear Knowledge Base"):
        st.session_state.vectorstore = None
        st.session_state.memory = create_memory()
        st.session_state.messages = []
        st.session_state.docs_ready = False
        st.success("Knowledge base and chat history cleared.")

    st.divider()
    st.markdown(
        "**How to use:**\n"
        "1. Upload 2–4 PDFs (annual reports, manuals, etc.).\n"
        "2. Click **Process Documents**.\n"
        "3. Ask questions in the chat.\n"
        "4. Follow‑up questions are supported."
    )

# ------------------------------------------------------------------
# Main Chat Area
# ------------------------------------------------------------------
if not st.session_state.docs_ready:
    st.info("👈 Upload and process PDF documents to get started.")
else:
    # Initialise LLM once
    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0.0,
        api_key=GROQ_API_KEY,
    )

    # Render previous chat messages
    for role, content, sources in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)
            if role == "assistant" and sources and sources != "No sources found.":
                with st.expander("📖 Sources"):
                    st.caption(sources)

    # Chat input
    user_input = st.chat_input("Ask a question about your documents…")

    if user_input:
        input_error = validate_question(user_input)
        displayed_input = (
            "[Input omitted by guardrails]" if input_error else user_input
        )

        # Display user message
        st.session_state.messages.append(("user", displayed_input, ""))
        with st.chat_message("user"):
            st.markdown(displayed_input)

        # Generate answer
        with st.chat_message("assistant"):
            if input_error:
                answer, sources = input_error, NO_SOURCES_FOUND
            else:
                with st.spinner("Thinking…"):
                    answer, sources = answer_question(
                        vectorstore=st.session_state.vectorstore,
                        llm=llm,
                        memory=st.session_state.memory,
                        question=user_input,
                    )

            st.markdown(answer)

            if sources and sources != "No sources found.":
                with st.expander("📖 Sources"):
                    st.caption(sources)

        st.session_state.messages.append(("assistant", answer, sources))