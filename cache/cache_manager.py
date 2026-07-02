"""Cache Manager - Unified caching interface."""

from typing import Any, Optional, Callable
from functools import wraps
import hashlib
import json

from cache.memory_cache import MemoryCache
from database.redis import RedisClient


class CacheManager:
    """Unified cache manager with memory and Redis backends."""
    
    def __init__(self, use_redis: bool = True):
        self.memory_cache = MemoryCache()
        self.redis_cache = RedisClient() if use_redis else None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        value = self.memory_cache.get(key)
        if value is not None:
            return value
        
        if self.redis_cache:
            return self.redis_cache.get(key)
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        self.memory_cache.set(key, value)
        
        if self.redis_cache:
            self.redis_cache.set(key, value, expire=ttl)
    
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        self.memory_cache.delete(key)
        
        if self.redis_cache:
            self.redis_cache.delete(key)
    
    def clear(self) -> None:
        """Clear all cache."""
        self.memory_cache.clear()
    
    def cached(ttl: int = 300):
        """Decorator for caching function results."""
        cache = CacheManager()
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = f"{func.__name__}:{hashlib.md5(str(args).encode()).hexdigest()}"
                
                result = cache.get(key)
                if result is not None:
                    return result
                
                result = func(*args, **kwargs)
                cache.set(key, result, ttl=ttl)
                return result
            return wrapper
        return decorator