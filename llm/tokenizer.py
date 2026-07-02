"""Tokenizer - Token counting utilities."""

from typing import List, Union
import re


class TokenCounter:
    """Simple token counter for estimating token usage."""
    
    @staticmethod
    def count(text: str) -> int:
        """Estimate token count for text."""
        if not text:
            return 0
        
        tokens = 0
        words = re.findall(r'\S+', text)
        
        for word in words:
            if re.match(r'^[\W_]+$', word):
                tokens += 1
            else:
                tokens += max(1, len(word) // 4)
        
        tokens += text.count('\n') * 0.5
        
        return int(tokens)
    
    @staticmethod
    def count_messages(messages: List[dict]) -> int:
        """Count tokens in a message list."""
        total = 0
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            total += 4
            total += TokenCounter.count(role)
            total += TokenCounter.count(content)
        
        total += 2
        
        return int(total)
    
    @staticmethod
    def truncate(text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit."""
        tokens = TokenCounter.count(text)
        
        if tokens <= max_tokens:
            return text
        
        words = text.split()
        target_words = int(max_tokens * 4 * 0.75)
        
        return " ".join(words[:target_words])


class TiktokenCounter:
    """Tiktoken-based token counter (when available)."""
    
    _instance = None
    _encoder = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize tiktoken encoder."""
        try:
            import tiktoken
            self._encoder = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            self._encoder = None
    
    def count(self, text: str) -> int:
        """Count tokens using tiktoken."""
        if self._encoder is None:
            return TokenCounter.count(text)
        
        return len(self._encoder.encode(text))
    
    def encode(self, text: str) -> List[int]:
        """Encode text to tokens."""
        if self._encoder is None:
            return TokenCounter.count(text)
        
        return self._encoder.encode(text)
    
    def decode(self, tokens: List[int]) -> str:
        """Decode tokens to text."""
        if self._encoder is None:
            return ""
        
        return self._encoder.decode(tokens)