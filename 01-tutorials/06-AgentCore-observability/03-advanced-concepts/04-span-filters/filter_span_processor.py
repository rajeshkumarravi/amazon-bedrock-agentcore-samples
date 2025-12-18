"""Exclude/include spans from processing
# Usage:
# from strands.telemetry import StrandsTelemetry
from opentelemetry.trace import get_tracer_provider
from filter_span_processor import FilterSpanProcessor

tracer_provider = get_tracer_provider()
tracer_provider.add_span_processor(FilterSpanProcessor())
# tracer_provider.add_span_processor(FilterSpanProcessor(span_exporter))
# telemetry = StrandsTelemetry(tracer_provider=provider)

"""
# pylint:disable=logging-fstring-interpolation,protected-access,import-outside-toplevel
import json
import logging
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


# class FilterSpanProcessor(SpanProcessor):
#     """Filtering span processor impmenetation"""

#     def on_end(self, span: ReadableSpan):

#         logger.debug(f"Processing span: {span.name}")
#         original_attrs = dict(span._attributes)
#         logger.debug(json.dumps(original_attrs, sort_keys=True, default=str))
#         # Custom logic: Drop spans named "health_check"
#         if span.name == "health_check":
#             return
#         # Custom logic: Drop spans named starting with "POST"
#         if span.name.lower().startswith("post"):
#             span.context.trace_flags.sampled = True
#             logger.debug(f"Excluded span: {span.name}")
#             return
#         # Otherwise, proceed with normal batching/exporting
#         super().on_end(span)


class FilterSpanProcessor(SpanProcessor):
    """Custom span processor that filters spans based on criteria"""

    def __init__(self, filter_func):
        """
        Args:
            filter_func: Function that returns True to keep span, False to drop
        """
        self.filter_func = filter_func

    # def on_start(self, span, parent_context=None):
    #     """Called when a span is started"""
    #     if self.filter_func(span):
    #         self.next_processor.on_start(span, parent_context)

    def on_end(self, span: ReadableSpan):
        """Called when a span is ended"""
        if self.filter_func(span):
            super().on_end(span)
        else:
            logger.debug(f"Excluded span: {span.name}")

    # def shutdown(self):
    #     """Shutdown the processor"""
    #     self.next_processor.shutdown()

    # def force_flush(self, timeout_millis=None):
    #     """Force flush the processor"""
    #     return self.next_processor.force_flush(timeout_millis)


def filter_spans(span: ReadableSpan):
    """Filter by spans name"""
    # filter by span name, attributes, etc.
    return not span.name.lower().startswith("post")


def filter_by_attributes(span: ReadableSpan):
    """Filter by span attributes"""
    if hasattr(span, 'attributes'):
        # Drop spans from specific endpoints
        if span.attributes.get('http.route') == '/health':
            return False
        # Keep only error spans
        if span.attributes.get('error') is True:
            return True
    return True


def filter_by_name_pattern(span: ReadableSpan):
    """Filter by span name pattern"""
    import re
    # Drop spans matching pattern
    return not re.match(r'^internal\..*', span.name)

def filter_by_duration(span: ReadableSpan):
    """Filter by duration (requires ReadableSpan)"""
    if isinstance(span, ReadableSpan):
        duration_ns = span.end_time - span.start_time
        duration_ms = duration_ns / 1_000_000
        return duration_ms > 100  # Keep spans > 100ms
    return True
