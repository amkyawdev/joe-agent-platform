"""Model Router - Route requests to appropriate LLM providers."""

from typing import Optional, Dict, Any, List

from llm.providers.openrouter import OpenRouterProvider
from llm.providers.fallback import FallbackProvider
from llm.models import AVAILABLE_MODELS, ModelConfig


class ModelRouter:
    """Routes LLM requests to appropriate providers."""
    
    def __init__(self):
        self.default_model = "openrouter-free"  # Default to FREE model
        self._providers: Dict[str, Any] = {}
        self._register_providers()
    
    def _register_providers(self) -> None:
        """Register available providers."""
        self._providers["openrouter"] = OpenRouterProvider()
        self._providers["fallback"] = FallbackProvider()
    
    def get_provider(self, model: str) -> Any:
        """Get the provider for a model."""
        model_config = self.get_model_config(model)
        provider_name = model_config.provider
        
        if provider_name in self._providers:
            return self._providers[provider_name]
        
        return self._providers.get("fallback")
    
    def get_model_config(self, model: str) -> ModelConfig:
        """Get configuration for a model."""
        if model in AVAILABLE_MODELS:
            config = AVAILABLE_MODELS[model]
            return ModelConfig(
                model_id=config.get("id", model),
                provider=config.get("provider", "openrouter"),
                name=config.get("name", model),
                description=config.get("description", ""),
                context_length=config.get("context_length", 4096),
                capabilities=config.get("capabilities", [])
            )
        
        return ModelConfig(
            model_id=model,
            provider="openrouter",
            name=model,
            description="",
            context_length=4096,
            capabilities=[]
        )
    
    def list_models(
        self, 
        provider: Optional[str] = None,
        capability: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List available models with optional filtering."""
        models = []
        
        for model_id, config in AVAILABLE_MODELS.items():
            if provider and config.get("provider") != provider:
                continue
            
            if capability and capability not in config.get("capabilities", []):
                continue
            
            models.append({
                "id": model_id,
                **config
            })
        
        return models
    
    def get_default_provider(self) -> Any:
        """Get the default provider."""
        return self._providers.get("openrouter")