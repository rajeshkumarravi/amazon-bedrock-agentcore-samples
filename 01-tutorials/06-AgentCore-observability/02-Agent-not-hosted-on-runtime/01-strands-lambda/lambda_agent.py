"""Strands on Lambda demo"""

# pylint:disable=logging-fstring-interpolation

import logging
from strands import Agent
# from strands.telemetry import StrandsTelemetry
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.resources import Resource

logger = logging.getLogger()
logger.setLevel("DEBUG")

# Initialize Strands telemetry with 3P configuration
# strands_telemetry = StrandsTelemetry()
# strands_telemetry.setup_console_exporter()
# strands_telemetry.setup_otlp_exporter()

# Initialize Strands agent
agent = Agent()


def handler(event, context=None):
    """Your AI agent function"""
    logger.debug(f"Event: {event}")
    logger.debug(f"Context: {context}")

    user_message = event.get("prompt", "Hello! How can I help you today?")
    logger.info(f"User message: {user_message}")
    result = agent(user_message)
    return {"result": result.message}


if __name__ == "__main__":
    payload = {"prompt": "How far is moon from earth?"}
    handler(payload)
