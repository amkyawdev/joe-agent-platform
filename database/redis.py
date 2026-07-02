"""Redis - Redis cache integration."""

import json
from typing import Any, Optional, List
import redis


class RedisClient:
    """Redis client wrapper."""
    
    _instance = None
    
    def __new__(cls, url: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(url)
        return cls._instance
    
    def _init(self, url: Optional[str] = None) -> None:
        """Initialize Redis connection."""
        self.url = url or "redis://localhost:6379"
        self.client = redis.from_url(self.url, decode_responses=True)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key."""
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """Set value with optional expiration."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.client.set(key, value, ex=expire)
    
    def delete(self, key: str) -> None:
        """Delete key."""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return bool(self.client.exists(key))
    
    def keys(self, pattern: str = "*") -> List[str]:
        """Get keys matching pattern."""
        return self.client.keys(pattern)
    
    def incr(self, key: str, amount: int = 1) -> int:
        """Increment value."""
        return self.client.incr(key, amount)
    
    def expire(self, key: str, seconds: int) -> None:
        """Set expiration on key."""
        self.client.expire(key, seconds)
    
    def ttl(self, key: str) -> int:
        """Get time to live."""
        return self.client.ttl(key)