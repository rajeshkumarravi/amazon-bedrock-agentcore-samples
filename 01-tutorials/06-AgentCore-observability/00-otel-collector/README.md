# ADOT OpenTelemetry Collector on ECS (API-key protected)

A Python-CDK project that deploys an [AWS Distro for OpenTelemetry (ADOT)](https://aws-otel.github.io/)
collector on **ECS Fargate** and exposes an OTLP/HTTP ingest endpoint through
**API Gateway**, protected by a native API key (`x-api-key` header). The collector
forwards each signal to CloudWatch:

| Signal  | Exporter            | Destination            |
|---------|---------------------|------------------------|
| Traces  | `awsxray`           | AWS X-Ray              |
| Metrics | `awsemf`            | CloudWatch Metrics/Logs (EMF) |
| Logs    | `awscloudwatchlogs` | CloudWatch Logs        |

## Architecture

```
OTLP client
  │  x-api-key: <api-key>
  ▼
API Gateway (REST, prod stage)
  │  native API key enforced by a usage plan bound to the stage
  │
  │  VPC Link
  ▼
internal Network Load Balancer  :4318
  ▼
ECS Fargate service (ADOT collector, desired_count=2)
  ├─► X-Ray            (traces)
  ├─► CloudWatch EMF   (metrics)  → /aws/otel-collector/metrics
  └─► CloudWatch Logs  (logs)     → /aws/otel-collector/logs
```

### Authentication

The ingest method sets `api_key_required=True`, and an API key attached to a
usage plan is bound to the `prod` stage. Clients must send the key in the
`x-api-key` header; requests without a valid key get `403 Forbidden`. The usage
plan also applies request throttling (rate 1000 / burst 2000).

## Project layout

```
00-otel-collector/
├── app.py                          # CDK app entry point
├── cdk.json                        # app = "uv run python app.py"
├── pyproject.toml                  # uv-managed dependencies
├── otel_collector/
│   └── collector_stack.py          # the CDK stack
└── collector/
    ├── collector.yaml              # ADOT collector pipeline config
    └── Dockerfile                  # ADOT image + baked-in config
```

## Prerequisites

- An AWS account and credentials (`aws configure`) with permission to deploy
  VPC/ECS/API Gateway/IAM/Secrets Manager resources.
- [uv](https://docs.astral.sh/uv/) installed.
- [Node.js](https://nodejs.org/) + the AWS CDK CLI (`npm install -g aws-cdk`).
- Docker (or Finch) running — the collector image is built as a CDK asset.
- **Transaction Search enabled** in CloudWatch to view X-Ray spans
  (see the observability get-started guide in this repo).

## Setup

Install dependencies into a local virtual environment with uv:

```bash
cd 01-tutorials/06-AgentCore-observability/00-otel-collector
uv sync
```

## Deploy

```bash
# One-time per account/region:
uv run cdk bootstrap

# Deploy the stack:
export CDK_DOCKER=finch
uv run cdk deploy
```

On success, CDK prints two outputs:

- `IngestEndpoint` — the base URL, e.g. `https://abc123.execute-api.us-east-1.amazonaws.com/prod/`
- `ApiKeyId` — the id of the generated API key.

Retrieve the API key value:

```bash
aws apigateway get-api-key \
  --api-key <ApiKeyId> \
  --include-value \
  --query value --output text
```

## Send telemetry

Point any OTLP/HTTP client at the ingest endpoint and set the `x-api-key`
header to your API key. The OTLP/HTTP signal paths are appended to the base URL:

- Traces:  `<IngestEndpoint>v1/traces`
- Metrics: `<IngestEndpoint>v1/metrics`
- Logs:    `<IngestEndpoint>v1/logs`

Example with the OpenTelemetry SDK environment variables:

```bash
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_ENDPOINT="https://abc123.execute-api.us-east-1.amazonaws.com/prod"
export OTEL_EXPORTER_OTLP_HEADERS="x-api-key=<your-api-key>"
```

Quick smoke test with `curl` (empty trace payload; expect `200`):

```bash
curl -i -X POST \
  "https://abc123.execute-api.us-east-1.amazonaws.com/prod/v1/traces" \
  -H "x-api-key: <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[]}'
```

A missing or wrong key returns `403 Forbidden` from API Gateway.

## Verify in CloudWatch

- **Traces:** CloudWatch → Transaction Search / X-Ray traces.
- **Metrics:** namespace `AgentCore/OTelCollector`, and the EMF log group
  `/aws/otel-collector/metrics`.
- **Logs:** log group `/aws/otel-collector/logs`.
- **Collector's own logs:** `/aws/otel-collector/agent`.

## Configuration notes

- The exporter log-group names in `collector/collector.yaml` must match the log
  groups created in `collector_stack.py`. If you change one, change the other.
- The collector authenticates to AWS with the **ECS task role** (no static keys);
  the task role grants X-Ray, CloudWatch metrics, and CloudWatch Logs write access.
- Adjust `desired_count`, `cpu`, and `memory_limit_mib` in the stack for your load.

## Clean up

```bash
uv run cdk destroy
```

Log groups are created with `RemovalPolicy.DESTROY`, and the API key and usage
plan are removed with the stack.
