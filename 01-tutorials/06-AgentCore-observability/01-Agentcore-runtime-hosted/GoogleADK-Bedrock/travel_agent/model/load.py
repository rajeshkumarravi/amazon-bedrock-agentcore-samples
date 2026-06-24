import os
import subprocess
import time
import logging
import requests

logger = logging.getLogger(__name__)

# LiteLLM proxy configuration
LITELLM_PORT = 4000
LITELLM_BASE_URL = f"http://localhost:{LITELLM_PORT}"

_litellm_process = None


def _start_litellm_proxy() -> None:
    """
    Start the LiteLLM proxy server as a background process.
    LiteLLM translates OpenAI-compatible requests to Amazon Bedrock API calls.
    """
    global _litellm_process

    # Check if proxy is already running
    try:
        resp = requests.get(f"{LITELLM_BASE_URL}/health", timeout=2)
        if resp.status_code == 200:
            logger.info("LiteLLM proxy already running")
            return
    except requests.exceptions.ConnectionError:
        pass

    bedrock_model_id = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    config_content = f"""
model_list:
  - model_name: "{bedrock_model_id}"
    litellm_params:
      model: "bedrock/{bedrock_model_id}"
      aws_region_name: "{aws_region}"
"""

    config_path = "/tmp/litellm_config.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)

    logger.info(f"Starting LiteLLM proxy on port {LITELLM_PORT} for model {bedrock_model_id}...")
    _litellm_process = subprocess.Popen(
        ["litellm", "--config", config_path, "--port", str(LITELLM_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for proxy to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            resp = requests.get(f"{LITELLM_BASE_URL}/health", timeout=2)
            if resp.status_code == 200:
                logger.info("LiteLLM proxy is ready")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)

    raise RuntimeError(f"LiteLLM proxy failed to start after {max_retries} seconds")


def load_model() -> None:
    """
    Set up LiteLLM proxy for Amazon Bedrock model access.
    LiteLLM acts as an OpenAI-compatible proxy that translates requests
    to Amazon Bedrock, allowing Google ADK to use Claude models via
    the OpenAI-compatible interface.

    Authentication uses the IAM role attached to the AgentCore runtime
    (no API keys needed for Bedrock).
    """
    _start_litellm_proxy()

    # Configure Google ADK to use the LiteLLM OpenAI-compatible endpoint
    os.environ["OPENAI_API_KEY"] = "dummy-key-for-litellm"
    os.environ["OPENAI_BASE_URL"] = f"{LITELLM_BASE_URL}/v1"
