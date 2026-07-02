"""LLM Client - Main interface for language model interactions."""

from typing import List, Dict, Any, Optional, AsyncIterator
import httpx

from llm.router import ModelRouter
from llm.models import ModelConfig


class LLMClient:
    """Main client for LLM interactions."""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None
    ):
        self.router = ModelRouter()
        self.model = model or self.router.default_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
    
    def complete(self, prompt: str, **kwargs) -> str:
        """Generate completion for a prompt."""
        provider = self.router.get_provider(self.model)
        config = self.router.get_model_config(self.model)
        
        return provider.complete(
            prompt=prompt,
            model=config.model_id,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            api_key=self.api_key
        )
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat completion."""
        provider = self.router.get_provider(self.model)
        config = self.router.get_model_config(self.model)
        
        return provider.chat(
            messages=messages,
            model=config.model_id,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            api_key=self.api_key
        )
    
    def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream completion for a prompt."""
        provider = self.router.get_provider(self.model)
        config = self.router.get_model_config(self.model)
        
        return provider.stream(
            prompt=prompt,
            model=config.model_id,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            api_key=self.api_key
        )
    
    def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Stream chat completion."""
        provider = self.router.get_provider(self.model)
        config = self.router.get_model_config(self.model)
        
        return provider.chat_stream(
            messages=messages,
            model=config.model_id,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            api_key=self.api_key
        )
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        from llm.tokenizer import TokenCounter
        return TokenCounter.count(text)