"""Chat Routes - Conversation endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_conversation_memory
from api.schemas import ChatMessage, ChatHistoryRequest, ChatHistoryResponse
from agent.memory import ConversationMemory


router = APIRouter()


@router.post("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    request: ChatHistoryRequest,
    memory: ConversationMemory = Depends(get_conversation_memory)
) -> ChatHistoryResponse:
    """Get chat history."""
    messages = memory.get_last_n(request.limit)
    return ChatHistoryResponse(messages=[m.to_dict() for m in messages])


@router.post("/chat/clear")
async def clear_chat(
    memory: ConversationMemory = Depends(get_conversation_memory)
) -> dict:
    """Clear chat history."""
    memory.clear()
    return {"status": "success", "message": "Chat history cleared"}


@router.post("/chat/search")
async def search_chat(
    query: str,
    memory: ConversationMemory = Depends(get_conversation_memory)
) -> dict:
    """Search chat history."""
    results = memory.search(query)
    return {
        "query": query,
        "results": [m.to_dict() for m in results]
    }