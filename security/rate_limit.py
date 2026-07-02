"""Rate Limit - Rate limiting utilities."""

from typing import Optional, Callable
from functools import wraps
import time

from database.redis import RedisClient


class RateLimiter:
    """Rate limiting using Redis."""
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst: int = 10
    ):
        self.requests_per_minute = requests_per_minute
        self.burst = burst
        self.redis = RedisClient()
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        rate_key = f"rate:{key}"
        
        current = self.redis.get(rate_key)
        
        if current is None:
            self.redis.set(rate_key, 1, expire=60)
            return True
        
        if current >= self.requests_per_minute:
            return False
        
        self.redis.incr(rate_key)
        return True
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests."""
        current = self.redis.get(f"rate:{key}")
        if current is None:
            return self.requests_per_minute
        return max(0, self.requests_per_minute - current)


def rate_limit(requests_per_minute: int = 60):
    """Decorator for rate limiting."""
    limiter = RateLimiter(requests_per_minute=requests_per_minute)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"func:{func.__name__}"
            
            if not limiter.is_allowed(key):
                from fastapi import HTTPException
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator