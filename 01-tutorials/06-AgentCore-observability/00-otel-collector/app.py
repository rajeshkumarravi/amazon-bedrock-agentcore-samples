#!/usr/bin/env python3
"""CDK app entry point for the ADOT OpenTelemetry collector stack."""

import aws_cdk as cdk

from otel_collector.collector_stack import OtelCollectorStack

app = cdk.App()
OtelCollectorStack(
    app,
    "OtelCollectorStack",
    # Uses the CLI's default account/region (from the AWS profile/env).
    env=cdk.Environment(),
)
app.synth()
