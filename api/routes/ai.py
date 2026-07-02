"""AI Routes - LLM and AI endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_llm_client
from api.schemas import (
    CompletionRequest,
    CompletionResponse,
    ChatRequest,
    ChatResponse
)
from llm.client import LLMClient


router = APIRouter()


@router.post("/ai/complete", response_model=CompletionResponse)
async def complete(
    request: CompletionRequest,
    llm: LLMClient = Depends(get_llm_client)
) -> CompletionResponse:
    """Generate text completion."""
    try:
        response = llm.complete(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return CompletionResponse(text=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm: LLMClient = Depends(get_llm_client)
) -> ChatResponse:
    """Generate chat completion."""
    try:
        response = llm.chat(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return ChatResponse(message={"role": "assistant", "content": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/stream")
async def stream_complete(
    request: CompletionRequest,
    llm: LLMClient = Depends(get_llm_client)
):
    """Stream text completion."""
    from fastapi.responses import StreamingResponse
    
    async def generate():
        for chunk in llm.stream(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ):
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")