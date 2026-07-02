"""Workflow - Orchestrate complex agent workflows."""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import asyncio

from agent.planner import Planner, Task, TaskStatus
from agent.executor import Executor, ExecutionResult
from agent.memory import ConversationMemory
from agent.reasoning import Reasoner


@dataclass
class WorkflowState:
    tasks: List[Task]
    current_task: Optional[Task] = None
    context: Dict[str, Any] = None
    results: Dict[str, Any] = None
    
    def __post_init__(self):
        self.context = self.context or {}
        self.results = self.results or {}


class Workflow:
    """Manages complex multi-step workflows."""
    
    def __init__(self, name: str):
        self.name = name
        self.planner = Planner()
        self.executor = Executor()
        self.reasoner = Reasoner()
        self.memory = ConversationMemory()
    
    async def run(self, objective: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a complete workflow."""
        state = WorkflowState(tasks=[], context=context or {})
        
        self.memory.add_message("user", objective)
        
        tasks = await self.planner.plan(objective, context)
        state.tasks = tasks
        
        for task in tasks:
            if not task.can_execute([t.id for t in state.tasks if t.status == TaskStatus.COMPLETED]):
                continue
            
            state.current_task = task
            task.status = TaskStatus.IN_PROGRESS
            
            result = await self.executor.execute_task(task, state.context)
            
            if result.success:
                task.status = TaskStatus.COMPLETED
                task.result = result.result
                state.results[task.id] = result.result
                state.context[task.id] = result.result
            else:
                task.status = TaskStatus.FAILED
                task.error = result.error
                break
        
        self.memory.add_message("assistant", str(state.results))
        
        return {
            "status": "completed" if all(t.status == TaskStatus.COMPLETED for t in state.tasks) else "failed",
            "tasks": state.tasks,
            "results": state.results
        }
    
    async def run_with_reasoning(self, objective: str) -> Dict[str, Any]:
        """Run workflow with explicit reasoning steps."""
        reasoning_steps = await self.reasoner.think(objective)
        
        summary = "\n".join(
            f"{i+1}. {step.thought}" 
            for i, step in enumerate(reasoning_steps)
        )
        
        final_result = await self.run(objective, {"reasoning": summary})
        final_result["reasoning_steps"] = reasoning_steps
        
        return final_result


class WorkflowBuilder:
    """Builder for constructing reusable workflows."""
    
    def __init__(self, name: str):
        self.name = name
        self._steps: List[Callable] = []
        self._handlers: Dict[str, Callable] = {}
    
    def add_step(self, name: str, handler: Callable) -> "WorkflowBuilder":
        """Add a workflow step."""
        self._steps.append(handler)
        self._handlers[name] = handler
        return self
    
    def build(self) -> Workflow:
        """Build the workflow."""
        workflow = Workflow(self.name)
        return workflow
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all steps in sequence."""
        results = {}
        current_data = input_data
        
        for step_name, handler in self._handlers.items():
            try:
                result = await handler(current_data)
                results[step_name] = result
                current_data.update(result)
            except Exception as e:
                results[step_name] = {"error": str(e), "status": "failed"}
                break
        
        return results