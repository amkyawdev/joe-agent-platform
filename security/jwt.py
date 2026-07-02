"""JWT - JWT token utilities."""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

from jose import jwt, JWTError


class JWTHandler:
    """Handle JWT tokens."""
    
    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
        expire_minutes: int = 30
    ):
        self.secret_key = secret_key or os.getenv("SECRET_KEY", "dev-secret-key")
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expire_delta: Optional[timedelta] = None
    ) -> str:
        """Create access token."""
        to_encode = data.copy()
        
        if expire_delta:
            expire = datetime.utcnow() + expire_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_access_token(self, token: str) -> Dict[str, Any]:
        """Decode access token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise ValueError("Invalid token")


def create_access_token(data: Dict[str, Any], **kwargs) -> str:
    """Create access token (convenience function)."""
    handler = JWTHandler()
    return handler.create_access_token(data, **kwargs)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode access token (convenience function)."""
    handler = JWTHandler()
    return handler.decode_access_token(token)