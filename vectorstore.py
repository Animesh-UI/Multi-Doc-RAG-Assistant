# vectorstore.py
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from config import EMBEDDING_MODEL, GOOGLE_API_KEY, TOP_K


def build_vectorstore(chunks: List[Document]) -> Optional[Chroma]:
    """
    Creates an in‑memory Chroma vector store from the chunked documents.
    Returns None if no chunks are provided.
    """
    if not chunks:
        return None

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="multi_doc_rag",
        # In‑memory: no persist_directory supplied
    )
    return vectorstore


def retrieve(vectorstore: Chroma, query: str, k: int = TOP_K) -> List[Document]:
    """
    Performs similarity search and returns top‑k documents.
    """
    if vectorstore is None:
        return []
    return vectorstore.similarity_search(query, k=k)