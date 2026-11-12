# 📚 Multi-Document RAG System

An intelligent **Retrieval-Augmented Generation (RAG)** assistant that lets you upload multiple PDF documents and ask questions in natural language. The system retrieves relevant information from your documents and generates accurate, **grounded answers with source citations**, while maintaining **conversational memory** for natural follow-up questions.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?logo=langchain)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Usage Guide](#-usage-guide)
- [Testing Scenarios](#-testing-scenarios)
- [API Keys & Free Tiers](#-api-keys--free-tiers)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🧭 Overview

Organizations maintain large collections of documents — technical reports, business documents, policies, and operational manuals. Finding accurate information across multiple documents is time-consuming and error-prone.

This project solves that problem by providing an **intelligent RAG assistant** that:

- Ingests **multiple PDF documents** at once
- Understands **natural language questions**
- **Retrieves** relevant passages from the correct documents
- **Generates** context-grounded answers using a Large Language Model
- **Cites** the exact source file and page number
- **Remembers** the conversation for natural follow-ups
- **Refuses** to answer when the information is not in the documents (no hallucinations)

All powered by **free APIs** — no credit card required.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Multi-PDF Upload** | Upload one or many PDFs simultaneously through the Streamlit UI |
| 🔍 **Semantic Retrieval** | Uses vector embeddings to find the most relevant chunks across all documents |
| 🎯 **Grounded Answers** | Responses are generated **only** from retrieved context |
| 📖 **Source Citations** | Every answer includes `[Source: filename, page X]` references |
| 🛡️ **"I Don't Know" Guardrail** | LLM-based relevance check prevents hallucination on unanswerable queries |
| 🧠 **Conversational Memory** | Keeps the last 5 turns for context-aware follow-up questions |
| 🔄 **Query Reformulation** | Rewrites ambiguous follow-up questions into standalone search queries |
| ⚡ **Fast Inference** | Groq's hardware-accelerated Llama 3.1 delivers near-instant responses |
| 🆓 **100% Free** | No paid APIs — Groq, Gemini Embeddings, and ChromaDB all have free tiers |
| 🎨 **Interactive UI** | Clean Streamlit chat interface with expandable source panels |

---

## 🖼️ Demo

### Example Interaction

> **User:** *"What were the revenue figures mentioned in the 2025 reports?"*
>
> **Assistant:** *"According to the documents, the 2025 annual report shows revenue of $12.4 billion, up 18% year-over-year [Source: annual_report_2025.pdf, Page 12]. The Q3 financial summary also confirms this figure [Source: q3_financials.pdf, Page 3]."*
>
> 📖 **Sources:** `annual_report_2025.pdf (page 12); q3_financials.pdf (page 3)`

> **User:** *"And what about the previous year?"*
>
> **Assistant:** *"In 2024, revenue was $10.5 billion [Source: annual_report_2024.pdf, Page 8]."*

> **User:** *"What is the CEO's favourite colour?"*
>
> **Assistant:** *"I could not find this information in the uploaded documents. Please try rephrasing your question or upload additional documents."*

---

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────────┐
│ User (Streamlit UI) │
└───────────────────────────┬─────────────────────────────────┘
│
┌─────────────▼──────────────┐
│ Multi-PDF Upload (Sidebar)│
└─────────────┬──────────────┘
│
┌─────────────▼──────────────┐
│ Ingestion & Chunking │
│ (PyPDFLoader + Splitter) │
└─────────────┬──────────────┘
│
┌─────────────▼──────────────┐
│ Embedding (Gemini API) │
└─────────────┬──────────────┘
│
┌─────────────▼──────────────┐
│ ChromaDB Vector Store │
└─────────────┬──────────────┘
│
┌───────────────────────▼─────────────────────────┐
│ User asks a question │
└───────────────────────┬─────────────────────────┘
│
┌─────────────▼──────────────┐
│ Query Reformulation │
│ (uses chat history) │
└─────────────┬──────────────┘
│
┌─────────────▼──────────────┐
│ Similarity Search (top-k) │
└─────────────┬──────────────┘
│
┌─────────────▼──────────────┐
│ Guardrail: Is context │
│ sufficient? │
└────┬─────────────────┬──────┘
│ Yes │ No
┌─────────▼───────┐ ┌──────▼─────────┐
│ Generate Answer │ │ Fallback Reply │
│ with Citations │ │ "Not found" │
└─────────┬───────┘ └──────┬─────────┘
│ │
┌─────────▼─────────────────▼──────┐
│ Display Answer + Sources in UI │
│ Save turn to Memory │
└──────────────────────────────────┘

text

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Chat interface + file uploader |
| **Orchestration** | LangChain | Chains, prompts, memory, loaders |
| **LLM (Generation)** | Groq (Llama 3.1 8B) | Fast, free inference |
| **Embeddings** | Google Gemini (`embedding-001`) | Free embedding API |
| **Vector Store** | ChromaDB | In-memory similarity search |
| **PDF Parsing** | PyPDFLoader | Per-page text extraction |
| **Memory** | LangChain `ConversationBufferWindowMemory` | Conversational context |

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **pip** package manager
- Free API keys for **Groq** and **Google Gemini** (see [Free API Keys](#-free-api-keys))

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

# 4. Copy the environment file and add your keys
cp .env.example .env
# Now edit .env and paste your GROQ_API_KEY and GOOGLE_API_KEY

# 5. Run the app
streamlit run app.py
