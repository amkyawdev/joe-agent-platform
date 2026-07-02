"""Memory - Conversation and context memory management."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, max_messages: int = 100):
        self.max_messages = max_messages
        self.messages: List[Message] = []
    
    def add_message(
        self, 
        role: str, 
        content: str, 
        metadata: Optional[Dict] = None
    ) -> None:
        """Add a message to memory."""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages as dict list."""
        return [{"role": m.role, "content": m.content} for m in self.messages]
    
    def get_last_n(self, n: int) -> List[Message]:
        """Get last n messages."""
        return self.messages[-n:]
    
    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []
    
    def search(self, query: str) -> List[Message]:
        """Search messages by content."""
        return [m for m in self.messages if query.lower() in m.content.lower()]
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps([m.to_dict() for m in self.messages])
    
    @classmethod
    def from_json(cls, json_str: str, max_messages: int = 100) -> "ConversationMemory":
        """Deserialize from JSON."""
        data = json.loads(json_str)
        memory = cls(max_messages=max_messages)
        for msg_data in data:
            msg = Message(
                role=msg_data["role"],
                content=msg_data["content"],
                timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                metadata=msg_data.get("metadata", {})
            )
            memory.messages.append(msg)
        return memory


class PersistentMemory:
    """Persistent memory backed by Redis."""
    
    def __init__(self, namespace: str = "agent:memory"):
        self.namespace = namespace
        self._redis = None
    
    @property
    def redis(self):
        """Lazy load Redis client."""
        if self._redis is None:
            from database.redis import RedisClient
            self._redis = RedisClient()
        return self._redis
    
    def save(self, key: str, value: Any) -> None:
        """Save value to persistent memory."""
        self.redis.set(f"{self.namespace}:{key}", value)
    
    def load(self, key: str) -> Optional[Any]:
        """Load value from persistent memory."""
        return self.redis.get(f"{self.namespace}:{key}")
    
    def delete(self, key: str) -> None:
        """Delete value from persistent memory."""
        self.redis.delete(f"{self.namespace}:{key}")
    
    def list_keys(self, pattern: str = "*") -> List[str]:
        """List keys matching pattern."""
        return self.redis.keys(f"{self.namespace}:{pattern}")