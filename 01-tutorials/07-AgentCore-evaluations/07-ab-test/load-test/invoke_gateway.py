"""
Invoke AgentCore Gateway target with SigV4 authentication.

Sends multiple prompts to a gateway target endpoint to simulate
realistic agent traffic (useful for A/B testing scenarios).
"""

# pylint: disable=W1203,W0718

import os
import uuid
import time
import json
import logging
import random

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GATEWAY_URL = os.getenv("GATEWAY_URL")
REGION = os.getenv("AWS_REGION", "us-east-1")
SERVICE = "bedrock-agentcore"
NUM_REQUESTS = int(os.getenv("NUM_REQUESTS", "30"))
DELAY_SECONDS = float(os.getenv("DELAY_SECONDS", "2"))

PROMPTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.txt")


def load_prompts(filepath):
    """Load prompts from a text file (one prompt per line, skipping blank lines) and shuffle."""
    with open(filepath, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
    random.shuffle(prompts)
    return prompts


PROMPTS = load_prompts(PROMPTS_FILE)


def get_credentials():
    """Get AWS credentials from the default credential chain."""
    session = boto3.Session(region_name=REGION)
    credentials = session.get_credentials().get_frozen_credentials()
    return credentials


def sign_request(method, url, headers, body, credentials):
    """Sign a request with SigV4."""
    aws_request = AWSRequest(
        method=method,
        url=url,
        data=body,
        headers=headers,
    )
    SigV4Auth(credentials, SERVICE, REGION).add_auth(aws_request)
    return dict(aws_request.headers)


def invoke_gateway(prompt, credentials):
    """Send a single signed request to the gateway target."""
    session_id = str(uuid.uuid4())
    payload = json.dumps({"prompt": prompt})

    headers = {
        "Content-Type": "application/json",
        "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": session_id,
    }

    # Sign the request
    signed_headers = sign_request("POST", GATEWAY_URL, headers, payload, credentials)

    # Send the request
    response = requests.post(
        GATEWAY_URL,
        headers=signed_headers,
        data=payload,
        timeout=120,
    )

    return response


def main():
    """Send multiple prompts to the gateway."""
    credentials = get_credentials()
    logger.info(f"Gateway URL: {GATEWAY_URL}")
    logger.info(f"Sending {NUM_REQUESTS} requests with {DELAY_SECONDS}s delay")

    for i in range(1, NUM_REQUESTS + 1):
        prompt = PROMPTS[(i - 1) % len(PROMPTS)]
        logger.info(f"=== Request {i}/{NUM_REQUESTS}: {prompt} ===")

        try:
            response = invoke_gateway(prompt, credentials)
            logger.info(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(response.text)
            else:
                logger.error(f"Error: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            logger.error(f"Request failed: {e}")

        if i < NUM_REQUESTS:
            time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    main()
