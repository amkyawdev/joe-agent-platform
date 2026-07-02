"""Health Routes - System health check endpoints."""

from typing import Dict, Any
from fastapi import APIRouter

from monitoring.health import HealthChecker


router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/health/detailed")
async def detailed_health() -> Dict[str, Any]:
    """Detailed health check with service status."""
    from monitoring.health import HealthChecker
    checker = HealthChecker()
    return checker.check_all()


@router.get("/health/ready")
async def readiness_check() -> Dict[str, Any]:
    """Kubernetes readiness probe."""
    return {"ready": True}


@router.get("/health/live")
async def liveness_check() -> Dict[str, Any]:
    """Kubernetes liveness probe."""
    return {"alive": True}