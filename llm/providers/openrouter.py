"""OpenRouter Provider - OpenRouter API integration."""

from typing import List, Dict, Any, Optional, AsyncIterator
import httpx
import os

from llm.prompts import SYSTEM_PROMPT


class OpenRouterProvider:
    """OpenRouter API provider."""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self._api_key = api_key
        self._loaded = False
    
    @property
    def api_key(self) -> str:
        """Lazy load API key from environment."""
        if not self._loaded:
            # Load dotenv if not already loaded
            from dotenv import load_dotenv
            load_dotenv()
            self._loaded = True
        
        if self._api_key:
            return self._api_key
        return os.getenv("OPENROUTER_API_KEY", "")
    
    def _get_headers(self, api_key: Optional[str] = None) -> Dict[str, str]:
        """Get request headers."""
        key = api_key or self.api_key
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://joe-agent-platform.dev",
            "X-Title": "Joe-Agent-Platform"
        }
    
    def complete(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate completion."""
        messages = [{"role": "user", "content": prompt}]
        return self.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate chat completion."""
        if not self.api_key and not api_key:
            return self._mock_response(messages)
        
        url = f"{self.BASE_URL}/chat/completions"
        headers = self._get_headers(api_key)
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return self._mock_response(messages, error=str(e))
    
    def stream(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream completion."""
        messages = [{"role": "user", "content": prompt}]
        yield from self.chat_stream(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key
        )
    
    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream chat completion."""
        if not self.api_key and not api_key:
            content = self._mock_response(messages)
            for chunk in self._chunk_text(content):
                yield chunk
            return
        
        url = f"{self.BASE_URL}/chat/completions"
        headers = self._get_headers(api_key)
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            **kwargs
        }
        
        try:
            with httpx.Client(timeout=120.0) as client:
                with client.stream("POST", url, json=payload, headers=headers) as response:
                    for line in response.iter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            import json
                            chunk = json.loads(data)
                            content = chunk["choices"][0].get("delta", {}).get("content", "")
                            if content:
                                yield content
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def _mock_response(self, messages: List[Dict[str, str]], error: Optional[str] = None) -> str:
        """Mock response when API key is not available."""
        if error:
            return f"I encountered an error: {error}. Please configure your API key."
        
        last_message = messages[-1]["content"] if messages else ""
        
        return f"This is a mock response for: '{last_message[:50]}...'. Please configure your OpenRouter API key for real responses."
    
    def _chunk_text(self, text: str, chunk_size: int = 10) -> AsyncIterator[str]:
        """Split text into chunks for streaming."""
        words = text.split()
        for i in range(0, len(words), chunk_size):
            yield " ".join(words[i:i + chunk_size]) + " "


import asyncio

async def _async_wrapper(sync_func, *args, **kwargs):
    """Wrapper to make sync functions async."""
    return sync_func(*args, **kwargs)