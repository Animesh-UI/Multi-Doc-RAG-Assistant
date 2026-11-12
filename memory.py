# memory.py
from langchain_classic.memory import ConversationBufferWindowMemory
from config import MEMORY_WINDOW_K


def create_memory() -> ConversationBufferWindowMemory:
    """
    Keeps the last k conversational turns.
    memory_key="chat_history" will be injected into prompts.
    """
    return ConversationBufferWindowMemory(
        k=MEMORY_WINDOW_K,
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )