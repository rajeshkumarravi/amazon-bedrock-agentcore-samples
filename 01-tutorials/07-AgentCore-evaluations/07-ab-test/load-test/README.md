# A/B Test - Gateway Invocation

Scripts to invoke an AgentCore Gateway target with SigV4 authentication. Useful for generating traffic during A/B testing scenarios.

## Prerequisites

- Python 3.10+
- AWS credentials configured (via `aws configure`, env vars, or SSO)
- `pip install boto3 requests`

## Files

| File | Description |
|------|-------------|
| `invoke_gateway.py` | Sends signed requests to a gateway target endpoint |
| `streamable_http_sigv4.py` | StreamableHTTP MCP client transport with SigV4 signing |

## Usage

### Setup

```bash
uv sync --reinstall --refresh
```

### Basic run

```bash
cd test_ab
GATEWAY_URL="https://<gateway-id>.gateway.bedrock-agentcore.<region>.amazonaws.com/<control-target-name>/invocations" \
uv run python invoke_gateway.py
```

Alternatively, store environment variables in `.env` file can invoke Python code.
```bash
cd test_ab
uv run --env-file .env python invoke_gateway.py
```

### Configuration (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `GATEWAY_URL` | (hardcoded sample) | Full URL to the gateway target invocations endpoint |
| `AWS_REGION` | `us-east-1` | AWS region for SigV4 signing |
| `NUM_REQUESTS` | `10` | Number of requests to send |
| `DELAY_SECONDS` | `2` | Delay between requests (seconds) |

### Examples

Quick test with 5 requests:

```bash
NUM_REQUESTS=5 DELAY_SECONDS=1 \
  GATEWAY_URL="https://your-gw.gateway.bedrock-agentcore.us-east-1.amazonaws.com/target/invocations" \
  python invoke_gateway.py
```

High-volume traffic for A/B testing:

```bash
NUM_REQUESTS=100 DELAY_SECONDS=0.5 \
  GATEWAY_URL="https://your-gw.gateway.bedrock-agentcore.us-east-1.amazonaws.com/target/invocations" \
  python invoke_gateway.py
```

## How it works

1. Loads AWS credentials from the default credential chain (env vars, profile, SSO, etc.)
2. For each request, generates a unique session ID (`X-Amzn-Bedrock-AgentCore-Runtime-Session-Id`)
3. Signs the request with SigV4 (`bedrock-agentcore` service)
4. POSTs a JSON payload with a prompt to the gateway target URL
5. Prints the response and moves to the next prompt after the configured delay

## Reference

- [A/B Testing (Target-Based)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/ab-testing-target-based.html)
