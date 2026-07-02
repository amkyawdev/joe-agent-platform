"""Middleware - API middleware components."""

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import structlog


def setup_middleware(app: FastAPI) -> None:
    """Setup API middleware."""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        structlog.get_logger().info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration * 1000
        )
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Handle errors globally."""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            structlog.get_logger().error(
                "request_error",
                error=str(e),
                path=request.url.path
            )
            return {"error": str(e)}