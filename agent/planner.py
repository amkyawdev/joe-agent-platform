"""Planner - Task planning and decomposition for the agent."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from llm.client import LLMClient
from agent.prompts import PLANNER_PROMPT


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def can_execute(self, completed_tasks: List[str]) -> bool:
        """Check if all dependencies are satisfied."""
        return all(dep in completed_tasks for dep in self.dependencies)


class Planner:
    """Plans and decomposes complex tasks into executable steps."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    async def plan(self, objective: str, context: Optional[Dict] = None) -> List[Task]:
        """Create a plan to achieve the objective."""
        prompt = PLANNER_PROMPT.format(
            objective=objective,
            context=self._format_context(context or {})
        )
        
        response = self.llm.complete(prompt)
        tasks = self._parse_tasks(response)
        
        return [Task(id=f"task_{i}", description=t) for i, t in enumerate(tasks)]
    
    def _format_context(self, context: Dict) -> str:
        """Format context dictionary for prompt."""
        if not context:
            return "No additional context provided."
        
        return "\n".join(f"- {k}: {v}" for k, v in context.items())
    
    def _parse_tasks(self, response: str) -> List[str]:
        """Parse LLM response into task list."""
        tasks = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                task = line.lstrip('0123456789.-•) ').strip()
                if task:
                    tasks.append(task)
        
        return tasks
    
    def update_plan(self, tasks: List[Task], completed_task_id: str, result: Any) -> List[Task]:
        """Update plan after task completion."""
        completed = False
        for task in tasks:
            if task.id == completed_task_id:
                task.status = TaskStatus.COMPLETED
                task.result = result
                completed = True
            elif completed and task.can_execute([t.id for t in tasks if t.status == TaskStatus.COMPLETED]):
                task.status = TaskStatus.PENDING
        
        return tasks