"""Executor - Executes tasks using available tools."""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

from agent.planner import Task, TaskStatus
from llm.client import LLMClient
from agent.tools import ToolRegistry


@dataclass
class ExecutionResult:
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class Executor:
    """Executes tasks with tool support."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
        self.tools = ToolRegistry()
    
    async def execute_task(self, task: Task, context: Dict[str, Any]) -> ExecutionResult:
        """Execute a single task."""
        try:
            result = await self._execute_with_tools(task, context)
            return ExecutionResult(
                task_id=task.id,
                success=True,
                result=result,
                metadata={"status": "completed"}
            )
        except Exception as e:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                error=str(e),
                metadata={"status": "failed"}
            )
    
    async def _execute_with_tools(self, task: Task, context: Dict[str, Any]) -> Any:
        """Execute task using appropriate tools."""
        available_tools = self.tools.get_all()
        
        if available_tools:
            tool_descriptions = "\n".join(
                f"- {tool.name}: {tool.description}" 
                for tool in available_tools.values()
            )
            
            prompt = f"""Task: {task.description}
Context: {self._format_context(context)}
Available Tools:
{tool_descriptions}

Determine which tool(s) to use and execute the task. Report the result."""
            
            response = self.llm.complete(prompt)
            
            tool_name = self._extract_tool_call(response)
            if tool_name and tool_name in available_tools:
                tool = available_tools[tool_name]
                return await tool.execute(task.description, context)
        
        return self.llm.complete(task.description)
    
    def _format_context(self, context: Dict) -> str:
        """Format context for prompt."""
        if not context:
            return "No context available."
        return "\n".join(f"- {k}: {v}" for k, v in context.items())
    
    def _extract_tool_call(self, response: str) -> Optional[str]:
        """Extract tool name from LLM response."""
        response_lower = response.lower()
        for tool_name in self.tools.get_all():
            if f"use {tool_name}" in response_lower or f"call {tool_name}" in response_lower:
                return tool_name
        return None


class CodeExecutor:
    """Executes code generation tasks."""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def execute(self, prompt: str) -> str:
        """Execute code generation prompt."""
        code_prompt = f"""Generate executable code based on this request: {prompt}

Requirements:
- Write clean, well-documented code
- Include error handling
- Follow best practices
- Return only the code, no explanations unless requested"""
        
        return self.llm.complete(code_prompt)