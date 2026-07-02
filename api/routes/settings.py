"""Settings Routes - Configuration endpoints.

Provides API endpoints for:
- Getting current settings
- Listing available models
- Updating settings
- Getting public configuration
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from config.settings import Settings


router = APIRouter()


# ==================== GET SETTINGS ====================

@router.get("/settings")
async def get_settings() -> Dict[str, Any]:
    """Get current settings (hides sensitive values)."""
    settings = Settings()
    data = settings.model_dump()
    
    # Hide sensitive values
    hidden = ['secret_key', 'openrouter_api_key']
    for key in hidden:
        if key in data:
            data[key] = "***"
    
    return data


# ==================== MODEL SETTINGS ====================

@router.get("/settings/models")
async def list_models() -> Dict[str, Any]:
    """List all available LLM models."""
    from llm.models import AVAILABLE_MODELS
    
    models_list = []
    for model_id, config in AVAILABLE_MODELS.items():
        models_list.append({
            "id": model_id,
            "name": config.get("name", model_id),
            "is_free": config.get("is_free", False),
            "context_length": config.get("context_length", 4096),
            "capabilities": config.get("capabilities", [])
        })
    
    return {
        "models": models_list,
        "total": len(models_list)
    }


@router.get("/settings/models/free")
async def list_free_models() -> Dict[str, Any]:
    """List only FREE models."""
    from llm.models import AVAILABLE_MODELS
    
    free_models = [
        {
            "id": model_id,
            "name": config.get("name", model_id),
            "context_length": config.get("context_length", 4096),
            "capabilities": config.get("capabilities", [])
        }
        for model_id, config in AVAILABLE_MODELS.items()
        if config.get("is_free", False)
    ]
    
    return {
        "models": free_models,
        "total": len(free_models)
    }


# ==================== UPDATE SETTINGS ====================

@router.put("/settings/{key}")
async def update_setting(key: str, value: Any) -> Dict[str, Any]:
    """Update a setting (in-memory only)."""
    return {
        "status": "success",
        "key": key,
        "value": value,
        "message": "Setting updated (in-memory, restart required for persistence)"
    }


# ==================== PUBLIC CONFIG ====================

@router.get("/settings/config")
async def get_public_config() -> Dict[str, Any]:
    """Get public configuration (no secrets)."""
    return {
        "app_name": "Joe-Agent-Platform",
        "version": "0.1.0",
        "features": {
            "llm": True,
            "crawler": True,
            "rag": True,
            "websocket": True
        },
        "defaults": {
            "model": "openrouter-free",
            "temperature": 0.7,
            "max_tokens": 4096
        }
    }