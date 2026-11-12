# 📚 Multi-Document RAG System

An intelligent **Retrieval-Augmented Generation (RAG)** assistant that lets users upload multiple PDF documents and ask questions in natural language. The system retrieves relevant information from the documents and generates accurate, **grounded answers with source citations**, while maintaining **conversational memory** for follow-up questions.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?logo=langchain)
![Groq](https://img.shields.io/badge/Groq-Llama_3.1-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

Organizations maintain large collections of documents — technical reports, business documents, policies, and operational manuals. Finding accurate information across multiple documents is time-consuming and error-prone.

This project solves that problem with an intelligent RAG assistant that:

- Ingests **multiple PDF documents** at once
- Understands **natural language questions**
- **Retrieves** relevant passages from the correct documents
- **Generates** context-grounded answers using a Large Language Model
- **Cites** the exact source file and page number
- **Remembers** the conversation for natural follow-ups
- **Refuses** to answer when the information is not in the documents (no hallucinations)

All powered by **free APIs** — no credit card required. Built as part of **Assignment 3: Generative AI — Intelligent Multi-Document RAG System**.

---

## ✨ Features

- 📂 **Multi-PDF Upload** — Upload one or many PDFs simultaneously
- 🔍 **Semantic Retrieval** — Vector embeddings find the most relevant chunks across documents
- 🎯 **Grounded Answers** — Responses generated **only** from retrieved context
- 📖 **Source Citations** — Every answer includes `[Source: filename, page X]`
- 🛡️ **"I Don't Know" Guardrail** — LLM-based relevance check prevents hallucination
- 🧠 **Conversational Memory** — Keeps last 5 turns for context-aware follow-ups
- 🔄 **Query Reformulation** — Rewrites ambiguous follow-ups into standalone queries
- ⚡ **Fast Inference** — Groq's Llama 3.1 delivers near-instant responses
- 🆓 **100% Free** — Groq, Gemini Embeddings, and ChromaDB all have free tiers
- 🎨 **Interactive UI** — Clean Streamlit chat interface with expandable sources

---

## 🏗️ Architecture

```
User (Streamlit UI)
        │
        ▼
Multi-PDF Upload ──► Ingestion & Chunking (PyPDFLoader + Splitter)
        │
        ▼
Embedding (Gemini API) ──► ChromaDB Vector Store
        │
        ▼
User asks a question
        │
        ▼
Query Reformulation (uses chat history)
        │
        ▼
Similarity Search (top-k)
        │
        ▼
Guardrail: Is context sufficient?
        │
   ┌────┴────┐
   Yes       No
   │         │
   ▼         ▼
Generate   Fallback
Answer     "Not found"
   │         │
   └────┬────┘
        ▼
Display Answer + Sources + Save to Memory
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Chat UI + file uploader |
| Orchestration | LangChain | Chains, prompts, memory |
| LLM | Groq (Llama 3.1 8B) | Fast free inference |
| Embeddings | Google Gemini (`embedding-001`) | Free embedding API |
| Vector Store | ChromaDB | In-memory similarity search |
| PDF Parsing | PyPDFLoader | Per-page text extraction |
| Memory | `ConversationBufferWindowMemory` | Conversational context |

---

## 📁 Project Structure

```
multi-doc-rag/
├── app.py                 # Streamlit UI and chat interface
├── config.py              # Central configuration
├── ingest.py              # PDF loading and chunking
├── vectorstore.py         # ChromaDB setup and retrieval
├── rag_chain.py           # Reformulation, guardrail, generation
├── memory.py              # Conversation memory wrapper
├── requirements.txt       # Python dependencies
├── .env.example           # API key template
├── .gitignore             # Files excluded from Git
└── README.md              # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- Free API keys for **Groq** and **Google Gemini**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/multi-doc-rag.git
cd multi-doc-rag

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY and GOOGLE_API_KEY

# 5. Run the app
streamlit run app.py
```

App opens at `http://localhost:8501`.

---

## 🔑 Free API Keys

| Service | Free Tier | Sign Up |
|---|---|---|
| **Groq** (LLM) | 30 req/min, 14,400 req/day | [console.groq.com](https://console.groq.com) |
| **Google Gemini** (Embeddings) | 1,500 req/day | [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) |

**Get Groq key:** Sign up → API Keys → Create API Key → copy.
**Get Gemini key:** Sign in with Google → Create API key → copy.

Paste both into `.env`:
```
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIzaSy...
```

---

## 📘 Usage Guide

1. **Upload documents** — Use the sidebar to select 2–4 PDFs (annual reports, manuals, policies).
2. **Process** — Click **⚙️ Process Documents** and wait for the success message.
3. **Ask questions** — Type your question in the chat box.
4. **Review answers** — Each answer includes expandable **📖 Sources** with file + page.
5. **Follow-ups** — Ask context-dependent questions like *"What about the previous year?"*
6. **Reset** — Click **🗑️ Clear Knowledge Base** to start fresh.

---

## 🔬 How It Works

1. **Ingestion** — PyPDFLoader extracts text page-by-page, preserving filename + page metadata.
2. **Chunking** — RecursiveCharacterTextSplitter splits text into ~800-char overlapping chunks.
3. **Embedding** — Gemini API converts chunks into vectors stored in in-memory ChromaDB.
4. **Query Reformulation** — Follow-up questions are rewritten into standalone queries using chat history.
5. **Retrieval** — Top-4 most similar chunks are fetched from ChromaDB.
6. **Guardrail** — LLM checks whether retrieved context can answer the question; if not, returns a polite fallback.
7. **Generation** — LLM produces an answer using only the context, with `[Source: file, page X]` citations.
8. **Memory** — The turn is saved for context-aware follow-ups.

---

## 🧪 Testing Scenarios

| Test | Action | Expected Result |
|---|---|---|
| Multi-document retrieval | Upload 3 PDFs, ask a cross-file question | Answer synthesizes info from multiple docs |
| Source citations | Ask any factual question | Answer includes `[Source: file, page X]` + Sources panel |
| Unanswerable query | Ask about a topic not in any PDF | Returns "I could not find this information…" |
| Conversational memory | Ask "Revenue in 2024?" then "And in 2025?" | Second answer resolves both terms from history |
| Query reformulation | Ask "Risk factors" then "Which one is the biggest?" | Correct risk factor retrieved from prior doc |
| Document isolation | Upload two unrelated PDFs, ask about one | No irrelevant chunks in answer |

---

## ✅ Assignment Requirement Mapping

| Requirement | How It's Met |
|---|---|
| Upload multiple PDFs | `st.file_uploader(accept_multiple_files=True)` |
| Natural language Q&A | Streamlit chat + Groq Llama 3.1 |
| Retrieve relevant info | ChromaDB top-k similarity search |
| Context-aware LLM responses | `ANSWER_PROMPT` with retrieved context |
| Grounded in documents | Prompt: "use ONLY the provided context" |
| Source references | `[Source: filename, page X]` + Sources panel |
| Handle unavailable info | LLM guardrail → `FALLBACK_MESSAGE` |
| Conversational context | `ConversationBufferWindowMemory(k=5)` |
| Follow-up questions | `reformulate_query` uses chat history |
| Test with sample reports | Works with any text-based PDF |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `GROQ_API_KEY not found` | Ensure `.env` exists and contains the key |
| `API key not valid` (Gemini) | Regenerate at [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `RateLimitError` from Groq | Wait a minute; free tier = 30 req/min |
| No text extracted from PDF | PDF may be scanned; use OCR (Tesseract) first |
| `streamlit: command not found` | Activate virtual environment first |
| `ModuleNotFoundError` | Re-run `pip install -r requirements.txt` |
| Empty answer / no sources | Confirm PDFs have selectable text; re-process documents |

---

## ⚠️ Security Note

- **Never commit `.env`** — it contains your API keys
- `.gitignore` already excludes `.env`
- If you accidentally commit keys, **revoke them immediately** in the Groq/Gemini consoles

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) — RAG orchestration
- [Groq](https://groq.com) — Free fast LLM inference
- [Google Gemini](https://ai.google.dev) — Free embedding API
- [ChromaDB](https://www.trychroma.com) — Vector database
- [Streamlit](https://streamlit.io) — UI framework
- [PyPDF](https://pypdf.readthedocs.io) — PDF parsing

---

## 👤 Author

**[Your Name]**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your-email@example.com

---

⭐ **If this project helped you, consider giving it a star!**

*Assignment 3 — Generative AI: Intelligent Multi-Document RAG System*
