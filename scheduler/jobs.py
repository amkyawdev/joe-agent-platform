"""Jobs - Background job definitions."""

from typing import Callable, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    """Background job definition."""
    id: str
    name: str
    func: Callable
    schedule: str
    enabled: bool = True
    last_run: datetime = None
    next_run: datetime = None
    
    def run(self, *args, **kwargs) -> Any:
        """Execute the job."""
        return self.func(*args, **kwargs)


class JobRegistry:
    """Registry for background jobs."""
    
    def __init__(self):
        self._jobs: dict[str, Job] = {}
    
    def register(self, job: Job) -> None:
        """Register a job."""
        self._jobs[job.id] = job
    
    def unregister(self, job_id: str) -> None:
        """Unregister a job."""
        self._jobs.pop(job_id, None)
    
    def get(self, job_id: str) -> Job:
        """Get a job by ID."""
        return self._jobs.get(job_id)
    
    def list_jobs(self) -> list[Job]:
        """List all registered jobs."""
        return list(self._jobs.values())


def periodic_job(interval_seconds: int):
    """Decorator for periodic jobs."""
    def decorator(func: Callable) -> Callable:
        func._is_periodic_job = True
        func._interval_seconds = interval_seconds
        return func
    return decorator