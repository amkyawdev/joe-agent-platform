"""Unit tests for Agent module."""

import pytest

from agent.planner import Planner, Task, TaskStatus
from agent.memory import ConversationMemory, Message
from agent.tools import ToolRegistry, Tool


class TestPlanner:
    """Test task planner."""
    
    def test_task_creation(self):
        """Test creating a task."""
        task = Task(id="test_1", description="Test task")
        assert task.id == "test_1"
        assert task.status == TaskStatus.PENDING
    
    def test_task_can_execute_no_deps(self):
        """Test task can execute with no dependencies."""
        task = Task(id="test_1", description="Test task", dependencies=[])
        assert task.can_execute([])
    
    def test_task_can_execute_with_deps(self):
        """Test task can execute with satisfied dependencies."""
        task = Task(id="test_2", description="Test task", dependencies=["test_1"])
        assert task.can_execute(["test_1"])
        assert not task.can_execute([])


class TestMemory:
    """Test conversation memory."""
    
    def test_add_message(self):
        """Test adding messages to memory."""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Hello"
    
    def test_max_messages(self):
        """Test max messages limit."""
        memory = ConversationMemory(max_messages=5)
        for i in range(10):
            memory.add_message("user", f"Message {i}")
        
        assert len(memory.messages) <= 5
    
    def test_clear_memory(self):
        """Test clearing memory."""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        memory.clear()
        assert len(memory.messages) == 0
    
    def test_search_memory(self):
        """Test searching memory."""
        memory = ConversationMemory()
        memory.add_message("user", "Hello world")
        memory.add_message("user", "Goodbye world")
        
        results = memory.search("Hello")
        assert len(results) == 1
        assert "Hello" in results[0].content


class TestToolRegistry:
    """Test tool registry."""
    
    def test_register_tool(self):
        """Test registering a tool."""
        registry = ToolRegistry()
        
        async def dummy_handler():
            return "result"
        
        tool = Tool(
            name="test_tool",
            description="A test tool",
            parameters={},
            handler=dummy_handler
        )
        
        registry.register(tool)
        retrieved = registry.get("test_tool")
        assert retrieved is not None
        assert retrieved.name == "test_tool"
    
    def test_get_all_tools(self):
        """Test getting all tools."""
        registry = ToolRegistry()
        tools = registry.get_all()
        assert len(tools) > 0
    
    def test_execute_tool(self):
        """Test executing a tool."""
        registry = ToolRegistry()
        
        async def dummy_handler():
            return "executed"
        
        tool = Tool(
            name="exec_test",
            description="Test execution",
            parameters={},
            handler=dummy_handler
        )
        
        registry.register(tool)
        
        import asyncio
        result = asyncio.run(registry.execute("exec_test"))
        assert result == "executed"