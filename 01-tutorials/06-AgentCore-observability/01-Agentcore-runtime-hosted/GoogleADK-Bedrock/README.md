# Google ADK on AgentCore Runtime using Amazon Bedrock (Claude via LiteLLM)

Demonstrates a Google ADK travel agent hosted in Amazon Bedrock AgentCore Runtime, using **Claude (Anthropic) models on Amazon Bedrock** via [LiteLLM](https://docs.litellm.ai/) as an OpenAI-compatible proxy.

## How it works

Google ADK natively supports OpenAI-compatible model endpoints. This sample uses LiteLLM as a sidecar proxy that:
1. Exposes an OpenAI-compatible API on `localhost:4000`
2. Translates requests to Amazon Bedrock API calls
3. Uses the IAM execution role attached to the AgentCore runtime for authentication (no API keys needed)

The agent model is configured as `openai/<BEDROCK_MODEL_ID>`, which tells Google ADK to route requests through the OpenAI-compatible LiteLLM endpoint.


## Step by step instructions

### Setup dependency libraries

```bash
cd <project folder>
uv sync --reinstall --refresh
```

### Initialize AgentCore Starter Toolkit
**Note:** Starter toolkit is `deprecated`. Migrate to [AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html).

```bash
uv run agentcore configure -c -n google_adk_bedrock_demo -e travel_agent/main.py -dm -ecr auto -ni
```

<details>
  <summary>Sample output:</summary>

```bash

⚠️  The AgentCore CLI (@aws/agentcore) is now the recommended way to create, develop, and deploy agents on Amazon Bedrock AgentCore.
   We recommend migrating to the new CLI: npm install -g @aws/agentcore
   To import existing agents, run: agentcore import
   Set AGENTCORE_SUPPRESS_RECOMMENDATION=1 to silence this warning.

Configuring Bedrock AgentCore...

🚀 Deployment Configuration
Create mode only uses the container deployment type.
✓ Using: Container
✓ Will auto-create ECR repository
✓ Using default IAM authorization
✓ Using default request header configuration
Configuring BedrockAgentCore agent: google_adk_bedrock_demo
Memory disabled
Network mode: PUBLIC
Keeping 'google_adk_bedrock_demo' as default agent
╭───────────────────────────────────────────────────────────── Configuration Success ─────────────────────────────────────────────────────────────╮
│ Agent Details                                                                                                                                   │
│ Agent Name: google_adk_bedrock_demo                                                                                                             │
│ Deployment: container                                                                                                                           │
│ Region: us-east-1                                                                                                                               │
│ Account: 467801433859                                                                                                                           │
│                                                                                                                                                 │
│ Configuration                                                                                                                                   │
│ Execution Role: Auto-create                                                                                                                     │
│ Network Mode: Public                                                                                                                            │
│ ECR Repository: Auto-create                                                                                                                     │
│ Authorization: IAM (default)                                                                                                                    │
│                                                                                                                                                 │
│                                                                                                                                                 │
│ Memory: Disabled                                                                                                                                │
│                                                                                                                                                 │
│                                                                                                                                                 │
│ 📄 Config saved to:                                                                                                                             │
│ /Users/ravizraj/Documents/workspaces/agent-core/rajesh/amazon-bedrock-agentcore-samples/01-tutorials/06-AgentCore-observability/01-Agentcore-ru │
│ ntime-hosted/GoogleADK-Bedrock/.bedrock_agentcore.yaml                                                                                          │
│                                                                                                                                                 │
│ Next Steps:                                                                                                                                     │
│ agentcore deploy agentcore create                                                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
</details>

### Deploy agent to Runtime

**Recommended**
```bash
uv run agentcore deploy -env BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

**With OTEL filters**
```bash
uv run agentcore deploy -env BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0 -env OTEL_PYTHON_EXCLUDED_URLS="/health,/BerriAI/**"
```

<details>
  <summary>Additional ADOT settings:</summary>

Using ADOT native instrumentation

```bash
uv run agentcore deploy -env AWS_REGION=us-east-1 -env AGENT_OBSERVABILITY_ENABLED=true
```

Disable extracting messages from trace to logs

```bash
uv run agentcore deploy -env AWS_REGION=us-east-1 -env AWS_GENAI_CONTENT_EXTRACTION_OPT_OUT=true
```

Using ADOT native instrumentation and disable extracting messages from trace to logs

```bash
uv run agentcore deploy -env AWS_REGION=us-east-1 -env AGENT_OBSERVABILITY_ENABLED=true -env AWS_GENAI_CONTENT_EXTRACTION_OPT_OUT=true
```

</details>



### Check deployment status

```bash
uv run agentcore status
```


### Create online evaluation

*Note:* Online eval will be created with default 15 mins session timeout. Update to desired value from AWS console or using AWS CLI.

```bash
uv run agentcore eval online create -n google_adk_bedrock_demo_eval -s 100 -e "Builtin.Correctness" -e "Builtin.ResponseRelevance" -e "Builtin.ToolParameterAccuracy" -e "Builtin.ToolSelectionAccuracy"
```

### Invoke agent

```bash
uv run agentcore invoke --user-id demo-user --session-id "testing-google-adk-bedrock-$(date +%Y%m%d-%H%M%S)" '{"prompt": "search flights from seattle to NY trip for jul 4th 2026"}'
```

### Cleanup

```bash
uv run agentcore destroy --delete-ecr-repo --force --dry-run
```
