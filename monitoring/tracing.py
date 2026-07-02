"""Tracing - Distributed tracing utilities."""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


class TracingManager:
    """Manage distributed tracing."""
    
    def __init__(self, service_name: str = "joe-agent-platform"):
        self.service_name = service_name
        self.tracer = None
        self._setup_tracing()
    
    def _setup_tracing(self) -> None:
        """Setup OpenTelemetry tracing."""
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(self.service_name)
    
    def create_span(self, name: str):
        """Create a trace span."""
        if self.tracer:
            return self.tracer.start_as_current_span(name)
        return nullcontext()


class nullcontext:
    """Null context manager."""
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass