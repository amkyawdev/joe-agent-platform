"""Tools - Agent tool registry and definitions."""

from typing import Dict, List, Any, Optional, Callable, Awaitable
from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable[..., Awaitable[Any]]
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        return await self.handler(*args, **kwargs)


class ToolRegistry:
    """Registry for agent tools."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
            cls._instance._register_default_tools()
        return cls._instance
    
    def _register_default_tools(self) -> None:
        """Register default tools."""
        self.register(Tool(
            name="search",
            description="Search the web for information",
            parameters={"query": {"type": "string", "required": True}},
            handler=self._search_tool
        ))
        
        self.register(Tool(
            name="crawl",
            description="Crawl a URL and extract content",
            parameters={"url": {"type": "string", "required": True}},
            handler=self._crawl_tool
        ))
        
        self.register(Tool(
            name="calculate",
            description="Perform calculations",
            parameters={"expression": {"type": "string", "required": True}},
            handler=self._calculate_tool
        ))
    
    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def unregister(self, name: str) -> None:
        """Unregister a tool."""
        self._tools.pop(name, None)
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_all(self) -> Dict[str, Tool]:
        """Get all registered tools."""
        return self._tools.copy()
    
    async def execute(self, name: str, *args, **kwargs) -> Any:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        return await tool.execute(*args, **kwargs)
    
    async def _search_tool(self, query: str, **kwargs) -> List[Dict[str, str]]:
        """Default search tool implementation."""
        from rag.retriever import Retriever
        retriever = Retriever()
        results = retriever.search(query, top_k=5)
        return results
    
    async def _crawl_tool(self, url: str, **kwargs) -> str:
        """Default crawl tool implementation."""
        from crawler.fetcher import WebFetcher
        fetcher = WebFetcher()
        return fetcher.fetch(url)
    
    async def _calculate_tool(self, expression: str, **kwargs) -> Any:
        """Default calculate tool implementation."""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return result
        except Exception as e:
            return f"Error: {str(e)}"


class WebSearchTool(Tool):
    """Web search tool."""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information",
            parameters={
                "query": {"type": "string", "required": True},
                "num_results": {"type": "integer", "default": 10}
            },
            handler=self._search
        )
    
    async def _search(self, query: str, num_results: int = 10, **kwargs) -> List[Dict]:
        """Execute web search."""
        from rag.retriever import Retriever
        retriever = Retriever()
        return retriever.search(query, top_k=num_results)


class CodeExecutionTool(Tool):
    """Code execution tool with sandboxing."""
    
    def __init__(self):
        super().__init__(
            name="code",
            description="Execute Python code safely",
            parameters={
                "code": {"type": "string", "required": True},
                "timeout": {"type": "integer", "default": 30}
            },
            handler=self._execute
        )
    
    async def _execute(self, code: str, timeout: int = 30, **kwargs) -> str:
        """Execute Python code."""
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            exec(code, {"__builtins__": {}})
            output = sys.stdout.getvalue()
            return output or "Code executed successfully (no output)"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            sys.stdout = old_stdout