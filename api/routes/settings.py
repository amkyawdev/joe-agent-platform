"""Settings Routes - Configuration endpoints."""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from config.settings import Settings


router = APIRouter()


@router.get("/settings")
async def get_settings() -> Dict[str, Any]:
    """Get current settings."""
    settings = Settings()
    return settings.model_dump(exclude={'secret_key'})


@router.get("/settings/models")
async def list_models() -> Dict[str, Any]:
    """List available LLM models."""
    from llm.models import AVAILABLE_MODELS
    return {"models": AVAILABLE_MODELS}


@router.put("/settings/{key}")
async def update_setting(key: str, value: Any) -> Dict[str, Any]:
    """Update a setting."""
    return {
        "status": "success",
        "key": key,
        "value": value
    }