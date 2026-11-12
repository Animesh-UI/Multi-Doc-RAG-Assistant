# ingest.py
import tempfile
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import CHUNK_SIZE, CHUNK_OVERLAP


def load_and_split_pdfs(uploaded_files: List) -> List[Document]:
    """
    Accepts Streamlit UploadedFile objects.
    Returns a list of chunked Document objects with metadata:
      - source: original filename
      - page: page number (1‑indexed by PyPDFLoader as 0‑indexed internally)
    """
    all_chunks: List[Document] = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    for uploaded_file in uploaded_files:
        # Streamlit UploadedFile is file‑like; write it to a temp path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        try:
            loader = PyPDFLoader(tmp_path)
            pages = loader.load()   # Each element = one page Document

            for page_doc in pages:
                # PyPDFLoader stores 'source' and 'page' in metadata
                page_doc.metadata["source"] = uploaded_file.name
                # page is 0‑indexed; make it human‑readable (1‑indexed)
                if "page" in page_doc.metadata:
                    page_doc.metadata["page"] = page_doc.metadata["page"] + 1

            chunks = splitter.split_documents(pages)
            all_chunks.extend(chunks)

        finally:
            Path(tmp_path).unlink(missing_ok=True)

    return all_chunks