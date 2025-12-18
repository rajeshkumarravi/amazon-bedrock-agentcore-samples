"""Exclude/include spans from sampling
# Usage:
from opentelemetry.trace import set_tracer_provider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from filter_span_sampler import FilterSpanSampler, _filter_by_name

# Set the TracerProvider with the custom sampler
resource = Resource.create({"service.name": "my-instrumented-service"})
set_tracer_provider(
    TracerProvider(resource=resource, sampler=FilterSpanSampler(_filter_by_name))
)
"""
# pylint:disable=too-many-arguments,too-many-positional-arguments

from typing import Sequence, Optional
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision
from opentelemetry.context import Context
from opentelemetry.trace import Link, SpanKind, get_current_span
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes


def _get_parent_trace_state(
    parent_context: Optional[Context],
) -> Optional["TraceState"]:
    parent_span_context = get_current_span(parent_context).get_span_context()
    if parent_span_context is None or not parent_span_context.is_valid:
        return None
    return parent_span_context.trace_state


def _filter_by_name(span_name: str):
    """Filter by spans name"""
    # filter by span name, attributes, etc.
    # Drop span names starting with POST
    return not span_name.lower().startswith("post")


class FilterSpanSampler(Sampler):
    """Sampler implemetation to filter by spans"""
    def __init__(self, filter_func):
        """
        Args:
            filter_func: Function that returns True to keep span, False to drop
        """
        self.filter_func = filter_func

    def should_sample(
        self,
        parent_context: Optional["Context"],
        trace_id: int,
        name: str,
        kind: Optional[SpanKind] = None,
        attributes: Attributes = None,
        links: Optional[Sequence["Link"]] = None,
        trace_state: Optional["TraceState"] = None,
    ) -> SamplingResult:
        if self.filter_func(name):
            return SamplingResult(
                decision=Decision.RECORD_AND_SAMPLE,
                attributes=attributes,
                trace_state=_get_parent_trace_state(parent_context)
            )
        return SamplingResult(decision=Decision.DROP)

    def get_description(self) -> str:
        return "SpanFilterSampler"


def get_filter_span_sampler(sampler_argument: str) -> FilterSpanSampler:
    """Factory method to create the sampler instance."""
    # try:
    #     # OTEL_TRACES_SAMPLER_ARG value is passed here as a string
    #     rate = float(sampler_argument)
    # except (ValueError, TypeError):
    #     # Default rate if the argument is missing or invalid
    #     rate = 0.5
    print(f"Sampler arg: {sampler_argument}")
    return FilterSpanSampler(_filter_by_name)
