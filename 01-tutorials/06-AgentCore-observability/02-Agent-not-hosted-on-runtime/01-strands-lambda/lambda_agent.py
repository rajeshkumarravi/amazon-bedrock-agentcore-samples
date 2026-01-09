"""Strands on Lambda demo"""

# pylint:disable=logging-fstring-interpolation

import logging
from strands import Agent

logger = logging.getLogger()
logger.setLevel("INFO")

# Initialize Strands agent
agent = Agent()


def handler(event, context=None):
    """AI agent invocation"""
    logger.debug(f"Event: {event}")
    logger.debug(f"Context: {context}")

    user_message = event.get("prompt", "Hello! How can I help you today?")
    logger.info(f"User message: {user_message}")
    result = agent(user_message)
    return {"result": result.message}


if __name__ == "__main__":
    payload = {"prompt": "How far is moon from earth?"}
    handler(payload)
