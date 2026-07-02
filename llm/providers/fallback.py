"""Fallback Provider - Fallback LLM provider when others fail."""

from typing import List, Dict, Any, Optional, AsyncIterator
import random


class FallbackProvider:
    """Fallback provider for basic responses."""
    
    def __init__(self):
        self.fallback_responses = [
            "I understand your request. Let me help you with that.",
            "Thank you for your message. I'm processing this now.",
            "I've received your input and am working on a response.",
            "Could you provide more details about what you need?",
            "I'm here to help. Please let me know more about your question."
        ]
    
    def complete(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate fallback completion."""
        return self._generate_fallback_response(prompt)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate fallback chat response."""
        last_message = messages[-1]["content"] if messages else ""
        return self._generate_fallback_response(last_message)
    
    def stream(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream fallback completion."""
        response = self._generate_fallback_response(prompt)
        for chunk in self._chunk_response(response):
            yield chunk
    
    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream fallback chat response."""
        last_message = messages[-1]["content"] if messages else ""
        response = self._generate_fallback_response(last_message)
        for chunk in self._chunk_response(response):
            yield chunk
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a fallback response."""
        base_response = random.choice(self.fallback_responses)
        
        return f"{base_response}\n\nNote: This is a fallback response because the primary LLM service is unavailable. Please configure your API keys for full functionality."
    
    def _chunk_response(self, response: str) -> AsyncIterator[str]:
        """Split response into chunks for streaming simulation."""
        words = response.split()
        for i in range(0, len(words), 5):
            yield " ".join(words[i:i + 5]) + " "
            import asyncio
            asyncio.sleep(0.05)