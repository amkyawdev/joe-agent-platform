"""Registry - Agent and skill registry."""

from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class AgentConfig:
    name: str
    description: str
    version: str
    capabilities: List[str]
    tools: List[str]
    metadata: Dict[str, Any]


class AgentRegistry:
    """Registry for managing multiple agents."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or "storage/agents.json"
        self._agents: Dict[str, AgentConfig] = {}
        self._load()
    
    def _load(self) -> None:
        """Load agents from storage."""
        path = Path(self.storage_path)
        if path.exists():
            try:
                data = json.loads(path.read_text())
                for agent_data in data.get("agents", []):
                    agent = AgentConfig(**agent_data)
                    self._agents[agent.name] = agent
            except (json.JSONDecodeError, TypeError):
                pass
    
    def _save(self) -> None:
        """Save agents to storage."""
        path = Path(self.storage_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "agents": [agent.__dict__ for agent in self._agents.values()]
        }
        path.write_text(json.dumps(data, indent=2))
    
    def register(self, config: AgentConfig) -> None:
        """Register an agent."""
        self._agents[config.name] = config
        self._save()
    
    def unregister(self, name: str) -> bool:
        """Unregister an agent."""
        if name in self._agents:
            del self._agents[name]
            self._save()
            return True
        return False
    
    def get(self, name: str) -> Optional[AgentConfig]:
        """Get an agent by name."""
        return self._agents.get(name)
    
    def list_agents(self) -> List[AgentConfig]:
        """List all registered agents."""
        return list(self._agents.values())
    
    def find_by_capability(self, capability: str) -> List[AgentConfig]:
        """Find agents with a specific capability."""
        return [
            agent for agent in self._agents.values()
            if capability in agent.capabilities
        ]
    
    def find_by_tool(self, tool: str) -> List[AgentConfig]:
        """Find agents with a specific tool."""
        return [
            agent for agent in self._agents.values()
            if tool in agent.tools
        ]


class SkillRegistry:
    """Registry for agent skills and capabilities."""
    
    def __init__(self):
        self._skills: Dict[str, Dict[str, Any]] = {}
    
    def register(
        self, 
        name: str, 
        handler: Any,
        description: str = "",
        metadata: Optional[Dict] = None
    ) -> None:
        """Register a skill."""
        self._skills[name] = {
            "handler": handler,
            "description": description,
            "metadata": metadata or {}
        }
    
    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a skill by name."""
        return self._skills.get(name)
    
    def list_skills(self) -> List[str]:
        """List all skill names."""
        return list(self._skills.keys())
    
    async def execute(self, name: str, *args, **kwargs) -> Any:
        """Execute a skill."""
        skill = self.get(name)
        if not skill:
            raise ValueError(f"Skill '{name}' not found")
        
        handler = skill["handler"]
        if asyncio.iscoroutinefunction(handler):
            return await handler(*args, **kwargs)
        return handler(*args, **kwargs)


import asyncio