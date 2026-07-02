"""LLM Models - Model configurations and registry."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    model_id: str
    provider: str
    name: str
    description: str
    context_length: int
    capabilities: List[str]


AVAILABLE_MODELS: Dict[str, Dict[str, Any]] = {
    # === 💯 FREE CODING MODELS (Best for AI Coder Agent) ===
    # Auto-routes to best available free model
    "openrouter-free": {
        "id": "openrouter/free",
        "provider": "openrouter",
        "name": "OpenRouter Free ⭐ AUTO",
        "description": "Auto-routes to best available free model",
        "context_length": 262144,
        "capabilities": ["chat", "code", "reasoning"],
        "is_free": True,
        "cost": "FREE"
    },
    "google-gemma": {
        "id": "google/gemma-4-31b-it:free",
        "provider": "openrouter",
        "name": "Google Gemma 4 ⭐ FREE",
        "description": "Google's powerful free model for coding and reasoning",
        "context_length": 32768,
        "capabilities": ["chat", "code"],
        "is_free": True,
        "cost": "FREE"
    },
    "cohere-north-code": {
        "id": "cohere/north-mini-code:free",
        "provider": "openrouter",
        "name": "Cohere North Mini Code ⭐ FREE",
        "description": "Fast code generation model great for agentic workflows",
        "context_length": 32768,
        "capabilities": ["chat", "code"],
        "is_free": True,
        "cost": "FREE"
    },
    "nvidia-nemotron": {
        "id": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "provider": "openrouter",
        "name": "NVIDIA Nemotron 3 Ultra ⭐ FREE",
        "description": "Powerful free model from NVIDIA for coding tasks",
        "context_length": 1000000,
        "capabilities": ["chat", "code", "reasoning"],
        "is_free": True,
        "cost": "FREE"
    },
    "nvidia-nemotron-super": {
        "id": "nvidia/nemotron-3-super-120b-a12b:free",
        "provider": "openrouter",
        "name": "NVIDIA Nemotron 3 Super ⭐ FREE",
        "description": "Large NVIDIA model for complex coding tasks",
        "context_length": 262144,
        "capabilities": ["chat", "code", "reasoning"],
        "is_free": True,
        "cost": "FREE"
    },
    "poolside-laguna": {
        "id": "poolside/laguna-m.1:free",
        "provider": "openrouter",
        "name": "Poolside Laguna M ⭐ FREE",
        "description": "Good for coding and reasoning",
        "context_length": 262144,
        "capabilities": ["chat", "code"],
        "is_free": True,
        "cost": "FREE"
    },
    "google-gemma": {
        "id": "google/gemma-4-31b-it:free",
        "provider": "openrouter",
        "name": "Google Gemma 4 ⭐ FREE",
        "description": "Google's powerful free model for various tasks",
        "context_length": 32768,
        "capabilities": ["chat", "code"],
        "is_free": True,
        "cost": "FREE"
    },
    # === 💰 PAID MODELS ===
    "gpt-4-turbo-preview": {
        "id": "gpt-4-turbo-preview",
        "provider": "openrouter",
        "name": "GPT-4 Turbo",
        "description": "Fast and capable GPT-4 model with 128K context",
        "context_length": 128000,
        "capabilities": ["chat", "function_calling", "vision"]
    },
    "gpt-4": {
        "id": "gpt-4",
        "provider": "openrouter",
        "name": "GPT-4",
        "description": "Most capable GPT-4 model",
        "context_length": 8192,
        "capabilities": ["chat", "function_calling", "vision"]
    },
    "gpt-3.5-turbo": {
        "id": "gpt-3.5-turbo",
        "provider": "openrouter",
        "name": "GPT-3.5 Turbo",
        "description": "Fast and affordable GPT-3.5 model",
        "context_length": 16385,
        "capabilities": ["chat", "function_calling"]
    },
    "claude-3-opus": {
        "id": "anthropic/claude-3-opus",
        "provider": "openrouter",
        "name": "Claude 3 Opus",
        "description": "Most capable Claude model for complex tasks",
        "context_length": 200000,
        "capabilities": ["chat", "vision", "long_context"]
    },
    "claude-3-sonnet": {
        "id": "anthropic/claude-3-sonnet",
        "provider": "openrouter",
        "name": "Claude 3 Sonnet",
        "description": "Balanced Claude model",
        "context_length": 200000,
        "capabilities": ["chat", "vision", "long_context"]
    },
    "claude-3-haiku": {
        "id": "anthropic/claude-3-haiku",
        "provider": "openrouter",
        "name": "Claude 3 Haiku",
        "description": "Fast and efficient Claude model",
        "context_length": 200000,
        "capabilities": ["chat", "vision"]
    },
    "gemini-pro": {
        "id": "google/gemini-pro",
        "provider": "openrouter",
        "name": "Gemini Pro",
        "description": "Google's Gemini Pro model",
        "context_length": 32768,
        "capabilities": ["chat", "vision"]
    },
    "mixtral-8x7b": {
        "id": "mistralai/mixtral-8x7b",
        "provider": "openrouter",
        "name": "Mixtral 8x7B",
        "description": "Mixture of Experts model from Mistral",
        "context_length": 32768,
        "capabilities": ["chat"]
    },
    "llama-3-70b": {
        "id": "meta-llama/llama-3-70b",
        "provider": "openrouter",
        "name": "Llama 3 70B",
        "description": "Meta's Llama 3 70B model",
        "context_length": 8192,
        "capabilities": ["chat"]
    },
    "qwen-72b": {
        "id": "qwen/qwen-72b",
        "provider": "openrouter",
        "name": "Qwen 72B",
        "description": "Alibaba's Qwen 72B model",
        "context_length": 32768,
        "capabilities": ["chat"]
    }
}


class ModelRegistry:
    """Registry for managing model configurations."""
    
    def __init__(self):
        self._models = AVAILABLE_MODELS.copy()
    
    def register(self, model_id: str, config: Dict[str, Any]) -> None:
        """Register a new model."""
        self._models[model_id] = config
    
    def get(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model configuration."""
        return self._models.get(model_id)
    
    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """List all models."""
        return self._models.copy()
    
    def filter_by_capability(self, capability: str) -> List[Dict[str, Any]]:
        """Filter models by capability."""
        return [
            {"id": k, **v} for k, v in self._models.items()
            if capability in v.get("capabilities", [])
        ]
    
    def filter_by_provider(self, provider: str) -> List[Dict[str, Any]]:
        """Filter models by provider."""
        return [
            {"id": k, **v} for k, v in self._models.items()
            if v.get("provider") == provider
        ]