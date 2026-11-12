# rag_chain.py
from typing import List, Tuple

from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from config import (
    LLM_MODEL,
    GROQ_API_KEY,
    TOP_K,
    SIMILARITY_THRESHOLD,
    FALLBACK_MESSAGE,
)
from guardrails import (
    NO_SOURCES_FOUND,
    SENSITIVE_SOURCE_MESSAGE,
    UNSAFE_REQUEST_MESSAGE,
    contains_sensitive_data,
    is_request_allowed,
    validate_question,
    validate_response,
)


# ------------------------------------------------------------------
# 1. Query Reformulation (history‑aware)
# ------------------------------------------------------------------
REFORMULATE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the following chat history, rewrite the user's latest "
            "question as a self‑contained search query that can be used "
            "to retrieve relevant documents. Do not answer the question; "
            "only output the rewritten query.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


def reformulate_query(llm: ChatGroq, question: str, chat_history: List) -> str:
    """
    Uses the LLM to turn a context‑dependent follow‑up into a standalone query.
    """
    if not chat_history:
        return question

    chain = REFORMULATE_PROMPT | llm | StrOutputParser()
    standalone = chain.invoke(
        {"chat_history": chat_history, "question": question}
    )
    return standalone.strip()


# ------------------------------------------------------------------
# 2. Guardrail: LLM‑based relevance check
# ------------------------------------------------------------------
GUARDRAIL_PROMPT = ChatPromptTemplate.from_template(
    """You are a relevance checker. Decide whether the following context
contains enough information to answer the question.

Context:
{context}

Question: {question}

Answer ONLY with "YES" if the context is sufficient, or "NO" if it is not.
"""
)


def context_is_relevant(llm: ChatGroq, question: str, context: str) -> bool:
    """
    Returns True if the LLM judges the retrieved context sufficient.
    """
    chain = GUARDRAIL_PROMPT | llm | StrOutputParser()
    verdict = chain.invoke({"context": context, "question": question})
    return "YES" in verdict.upper()


# ------------------------------------------------------------------
# 3. Grounded Generation with Citations
# ------------------------------------------------------------------
ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer the user's question using "
            "ONLY the context provided below. If the context does not contain "
            "the answer, say you don't know. Do not use outside knowledge. "
            "When you use information from the context, cite the source "
            "using the format [Source: filename, page X].",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ]
)


def format_context(docs: List[Document]) -> Tuple[str, str]:
    """
    Converts retrieved Documents into a single context string and
    collects unique source citations.
    """
    context_parts = []
    sources = set()

    for doc in docs:
        src = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        context_parts.append(
            f"[Source: {src}, Page {page}]\n{doc.page_content}"
        )
        sources.add(f"{src} (page {page})")

    context = "\n\n---\n\n".join(context_parts)
    return context, "; ".join(sorted(sources))


# ------------------------------------------------------------------
# 4. Main RAG Pipeline
# ------------------------------------------------------------------
def answer_question(
    vectorstore,
    llm: ChatGroq,
    memory,
    question: str,
) -> Tuple[str, str]:
    """
    Full pipeline:
      1. Reformat query using history
      2. Retrieve top‑k chunks
      3. Guardrail check
      4. Generate grounded answer with citations
      5. Save turn to memory

    Returns:
      (answer_text, sources_string)
    """
    input_error = validate_question(question)
    if input_error:
        return input_error, NO_SOURCES_FOUND
    if not is_request_allowed(llm, question):
        return UNSAFE_REQUEST_MESSAGE, NO_SOURCES_FOUND

    chat_history = memory.load_memory_variables({})["chat_history"]

    # Step 1: standalone query
    standalone_query = reformulate_query(llm, question, chat_history)

    # Step 2: retrieval
    docs = vectorstore.similarity_search(standalone_query, k=TOP_K)

    if not docs:
        answer = FALLBACK_MESSAGE
        sources = NO_SOURCES_FOUND
        memory.save_context({"input": question}, {"answer": answer})
        return answer, sources

    # Step 3: guardrail – combine similarity + LLM check
    # (similarity check is optional; LLM check is more robust)
    context, sources = format_context(docs)
    if not context_is_relevant(llm, standalone_query, context):
        answer = FALLBACK_MESSAGE
        memory.save_context({"input": question}, {"answer": answer})
        return answer, sources

    # Step 4: grounded generation
    chain = ANSWER_PROMPT | llm | StrOutputParser()
    answer = chain.invoke(
        {
            "chat_history": chat_history,
            "context": context,
            "question": standalone_query,
        }
    )
    answer = validate_response(llm, answer)
    if contains_sensitive_data(sources):
        sources = SENSITIVE_SOURCE_MESSAGE

    # Step 5: memory
    memory.save_context({"input": question}, {"answer": answer})

    return answer, sources