"""API Schemas - Pydantic models for API."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class CompletionRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096


class CompletionResponse(BaseModel):
    text: str
    model: Optional[str] = None
    usage: Optional[Dict[str, int]] = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096


class ChatResponse(BaseModel):
    message: ChatMessage
    model: Optional[str] = None
    usage: Optional[Dict[str, int]] = None


class ChatHistoryRequest(BaseModel):
    limit: int = 50


class ChatHistoryResponse(BaseModel):
    messages: List[Dict[str, Any]]


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    collection: Optional[str] = None


class SearchResult(BaseModel):
    text: str
    score: float
    metadata: Dict[str, Any] = {}


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int