"""Custom OTEL span creation"""

import time
from functools import wraps
from opentelemetry.trace import Tracer, StatusCode


def otel_span_decorator(tracer: Tracer, span_name: str = None):
    """
    A decorator to create a custom OpenTelemetry span for a function.
    """
    def decorator(func):
        @wraps(func)  # Preserves the original function's name and metadata
        def wrapper(*args, **kwargs):
            # Use a context manager to automatically set the span as current
            # and ensure it ends even on exceptions
            with tracer.start_as_current_span(span_name or func.__name__) as span:
                # Optional: Add custom attributes/tags to the span
                span.set_attribute("function.name", func.__name__)
                start_time = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    # Optional: Add return value info or status
                    return result
                except Exception as e:
                    # Record exceptions and set span status to error
                    span.record_exception(e)
                    span.set_status(StatusCode.ERROR, description=str(e))
                    raise
                finally:
                    end_time = time.perf_counter()
                    span.set_attribute("execution.duration_ms", (end_time - start_time) * 1000)
                    # The 'with' block automatically ends the span, but this
                    # pattern works for manual span management too
        return wrapper
    return decorator
