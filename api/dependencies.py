"""Dependencies - FastAPI dependency injection."""

from typing import Generator, Optional
from fastapi import Depends
import redis

from llm.client import LLMClient
from agent.memory import ConversationMemory
from rag.retriever import Retriever
from rag.generator import RAGPipeline


_llm_client: Optional[LLMClient] = None
_retriever: Optional[Retriever] = None
_redis_client: Optional[redis.Redis] = None


def get_llm_client() -> LLMClient:
    """Get LLM client singleton."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def get_retriever() -> Retriever:
    """Get retriever singleton."""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def get_redis() -> redis.Redis:
    """Get Redis client."""
    global _redis_client
    if _redis_client is None:
        from config.settings import Settings
        settings = Settings()
        _redis_client = redis.from_url(settings.redis_url)
    return _redis_client


def get_conversation_memory() -> ConversationMemory:
    """Create new conversation memory."""
    return ConversationMemory()


def get_rag_pipeline() -> RAGPipeline:
    """Get RAG pipeline."""
    return RAGPipeline(retriever=get_retriever())