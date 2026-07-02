"""Dependencies - FastAPI dependency injection."""

from typing import Generator, Optional
from fastapi import Depends

from llm.client import LLMClient
from agent.memory import ConversationMemory

# Optional imports - handle gracefully if not installed
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

try:
    from rag.retriever import Retriever
    from rag.generator import RAGPipeline
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    Retriever = None
    RAGPipeline = None


_llm_client: Optional[LLMClient] = None
_retriever: Optional = None
_redis_client: Optional = None


def get_llm_client() -> LLMClient:
    """Get LLM client singleton."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def get_retriever():
    """Get retriever singleton."""
    if not RAG_AVAILABLE:
        return None
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def get_redis():
    """Get Redis client."""
    if not REDIS_AVAILABLE:
        return None
    global _redis_client
    if _redis_client is None:
        from config.settings import Settings
        settings = Settings()
        _redis_client = redis.from_url(settings.redis_url)
    return _redis_client


def get_conversation_memory() -> ConversationMemory:
    """Create new conversation memory."""
    return ConversationMemory()


def get_rag_pipeline():
    """Get RAG pipeline."""
    if not RAG_AVAILABLE:
        return None
    return RAGPipeline(retriever=get_retriever())