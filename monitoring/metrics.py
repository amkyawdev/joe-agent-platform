"""Metrics - Prometheus metrics collection."""

from prometheus_client import Counter, Histogram, Gauge, Summary
import time


request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

llm_calls = Counter(
    'llm_calls_total',
    'Total LLM calls',
    ['model', 'status']
)

llm_latency = Histogram(
    'llm_latency_seconds',
    'LLM call latency',
    ['model']
)


class MetricsCollector:
    """Collect application metrics."""
    
    @staticmethod
    def record_request(method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics."""
        request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    @staticmethod
    def record_llm_call(model: str, status: str, duration: float):
        """Record LLM call metrics."""
        llm_calls.labels(model=model, status=status).inc()
        llm_latency.labels(model=model).observe(duration)
    
    @staticmethod
    def set_active_connections(count: int):
        """Set active connections gauge."""
        active_connections.set(count)