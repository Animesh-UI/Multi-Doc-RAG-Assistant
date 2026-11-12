# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# API Keys (set these in a .env file)
# ------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")          # https://console.groq.com/keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")      # https://aistudio.google.com/app/apikey

# ------------------------------------------------------------------
# LLM & Embedding Model Names
# ------------------------------------------------------------------
LLM_MODEL = "openai/gpt-oss-20b"                  # Groq production model
EMBEDDING_MODEL = "gemini-embedding-001"          # Gemini text embedding model

# ------------------------------------------------------------------
# Chunking Parameters
# ------------------------------------------------------------------
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ------------------------------------------------------------------
# Retrieval & Guardrail Parameters
# ------------------------------------------------------------------
TOP_K = 4
SIMILARITY_THRESHOLD = 0.65   # Chroma cosine similarity (higher = more similar)
MEMORY_WINDOW_K = 5           # Number of recent turns to keep in memory

# ------------------------------------------------------------------
# Fallback Response
# ------------------------------------------------------------------
FALLBACK_MESSAGE = (
    "I could not find this information in the uploaded documents. "
    "Please try rephrasing your question or upload additional documents."
)