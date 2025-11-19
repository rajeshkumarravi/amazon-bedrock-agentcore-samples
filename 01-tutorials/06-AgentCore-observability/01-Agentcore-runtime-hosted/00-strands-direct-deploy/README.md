# Get started with Amazon Bedrock AgentCore Runtime and Observability with direct code deployment

## Prerequisites

Before you start, make sure you have:
* AWS Account with credentials configured. To configure your AWS credentials, see Configuration and credential file settings in the AWS CLI.
* UV installed and Python 3.10+ installed
* AWS Permissions: To create and deploy an agent with the starter toolkit, you must have appropriate permissions. For information, see Use the starter toolkit.
* Model access: Anthropic Claude Sonnet 4.0 enabled in the Amazon Bedrock console. For information about using a different model with the Strands Agents see the Model Providers section in the Strands Agents SDK documentation.

## Step 1: Set up project and install dependencies

Initialize your project with the following commands:
```
uv init agentcore_runtime_direct_deploy --python 3.13
cd agentcore_runtime_direct_deploy
```

Add core packages:
```
uv add -r requirements.txt
```
Package descriptions:
- **bedrock-agentcore**: The Amazon Bedrock AgentCore SDK for building AI agents
- **strands-agents**: The Strands Agents SDK
- **aws-opentelemetry-distro**: - Enable Amazon Bedrock AgentCore observability traces.

UV will automatically create a `pyproject.toml` file with dependencies, `uv.lock` file with dependency closure and `.venv` directory.

## Step 2: Create your agent

Create/Edit an entrypoint file for your agent code named `agent.py`. Add the following code:
```
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp(debug=True)
agent = Agent()

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    app.logger.info(f"User message: {user_message}")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
```


## Step 3: Test locally

Make sure port 8080 is free before starting. See _Port 8080_ in use (local only) in [Common issues and solutions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-toolkit.html#common-issues).

Open a terminal window and start your agent with the following command:
```
uv run agent.py
```
Test your agent by opening another terminal window and enter the following command:
```
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```
**Success:** You should see a response like `{"result": "Hello! I'm here to help..."}`. In the terminal window that's running the agent, enter `Ctrl+C` to stop the agent.


## Step 4: Enable observability for your agent

[Amazon Bedrock AgentCore Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html) helps you trace, debug, and monitor agents that you host in AgentCore Runtime. First enable CloudWatch Transaction Search by following the instructions at [Enabling Amazon Bedrock AgentCore runtime observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html#observability-configure-builtin). To observe your agent, see [View observability data for your Amazon Bedrock AgentCore agents](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-view.html).


## Step 5: Deploy to AgentCore Runtime and invoke

### Deploy your agent with starter kit

Install starter kit:
```
uv add --dev bedrock-agentcore-starter-toolkit
```

The following steps will be required to deploy an agent to AgentCore Runtime, refer to Get started with the Amazon Bedrock AgentCore starter toolkit, for detailed steps. If Uv is available, the starter toolkit will recommend direct code deployment. Otherwise it will default to container deployment type.

First command is configure, which will start an interactive session where you configure the S3 bucket to upload the zip.
```
# provides an interactive CLI to configure
agentcore configure -e agent.py -n strands_kit_direct_deploy --deployment_type direct_code_deploy --disable-memory
```

Next is launch which will create a zip deployment package, upload to the specified bucket and deploy the agent.
```
agentcore launch
```

Let's prompt the agent to tell a joke!
```
agentcore invoke '{"prompt":"Tell me a joke"}'
```

The first deployment takes time to install dependencies but subsequent updates to the agent optimizes this by re-using zipped dependencies


### Deploy your agent using `zip + boto3`:
To download a wheel that's compatible with AgentCore Runtime, you use the uv pip `--python-platform` option. AgentCore Runtime only supports **arm64** instruction set architecture, run the following command. Replace `--python 3.x` with the version of the Python runtime you are using.
```
pip install \
--platform manylinux2014_aarch64 \
--python-version 3.13 \
--implementation cp \
--target=deployment_package \
--only-binary=:all: \
-r requirements.txt
```

Create a `.zip` file with the installed libraries at the project root.
```
cd deployment_package
zip -r ../deployment_package.zip .
```

Add the `agent.py` file and other files in your package to the root of the `.zip` file.
```
cd ..
zip deployment_package.zip agent.py
```

After you have created your `.zip` deployment package, you can use it to create a new AgentCore Runtime or update an existing one. You can deploy your `.zip` package using AgentCore Runtime API, AgentCore Runtime console and AWS Command Line Interface. Amazon Bedrock AgentCore starter toolkit will take care of above steps to create .zip.

> [!NOTE]
> 1. The maximum size for a `.zip` deployment package for AgentCore Runtime is 250 MB (zipped) and 750 MB (unzipped). Note that this limit applies to the combined size of all the files you upload.
> 2. The AgentCore Runtime needs permission to read the files in your deployment package. In Linux permissions octal notation, AgentCore Runtime needs 644 permissions for non-executable files (rw-r—r--) and 755 permissions (rwxr-xr-x) for directories and executable files.
> 3. In Linux and MacOS, use the chmod command to change file permissions on files and directories in your deployment package. For example, to give a non-executable file the correct permissions, run the following command, chmod 644 <filepath>. To change file permissions in Windows, see [Set, View, Change, or Remove Permissions on an Object](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc731667(v=ws.10)) in the Microsoft Windows documentation.
> 4. If you don't grant AgentCore Runtime the permissions it needs to access directories in your deployment package, AgentCore Runtime sets the permissions for those directories to 755 (rwxr-xr-x).

A ZIP archive containing Linux arm64 dependencies needs to be uploaded to S3 as a pre-requisite to Create Agent Runtime. The below code requires the specified S3 bucket to already exist. Please follow the AWS documentation here to create an bucket using boto3. Following boto3 `deploy.py` will upload .zip file archive to a s3 and create Amazon Bedrock AgentCore runtime.

```
import boto3
from dotenv import dotenv_values

config = dotenv_values(".env")

REGION = config.get("AWS_REGION", "us-east-1")
AGENT_NAME = config.get("AGENT_NAME", "strands_direct_deploy")
AGENT_RUNTIME_ID = config.get("AGENT_RUNTIME_ID", "")
S3_BUCKET_NAME = config.get("S3_BUCKET_NAME", "")
S3_PREFIX = f"{AGENT_NAME}/deployment_package.zip"
AC_EXEC_ROLE_ARN = config.get("AC_EXEC_ROLE_ARN", "")
ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')


def deploy():
    s3_client = boto3.client('s3', region_name='us-west-2')
    print("Uploading deployment.zip to S3...")
    s3_client.upload_file( 
        'deployment_package.zip',  # archive on file system
        S3_BUCKET_NAME,
        S3_PREFIX,
        ExtraArgs={'ExpectedBucketOwner': ACCOUNT_ID}  # ownership check
    )
    print("Upload completed successfully!") 
    print(f"S3 Location: s3://{S3_BUCKET_NAME}/{S3_PREFIX}")

    agentcore_client = boto3.client('bedrock-agentcore-control', region_name=REGION)
    params = {
        # "agentRuntimeName": AGENT_NAME,
        "agentRuntimeArtifact": {
            'codeConfiguration': {
                'code': {
                    's3': {
                        'bucket': S3_BUCKET_NAME,
                        'prefix': S3_PREFIX
                    }
                },
                'runtime': 'PYTHON_3_13',
                'entryPoint': ['opentelemetry-instrument', 'agent.py']
            }  # if not adding otel dependency, remove opentelemetry-instrument from entrypoint array
        },
        "networkConfiguration": {"networkMode": "PUBLIC"},
        "roleArn": AC_EXEC_ROLE_ARN
    }
    if AGENT_RUNTIME_ID:
        params['agentRuntimeId'] = AGENT_RUNTIME_ID
        response = agentcore_client.update_agent_runtime(**params)
    else:
        params['agentRuntimeName'] = AGENT_NAME
        response = agentcore_client.create_agent_runtime(**params)
    print("Agent Runtime created successfully!")
    print(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
    print(f"Status: {response['status']}")


if __name__ == "__main__":
    deploy()
```

Open a terminal window and deploy your agent with the following command:
```
uv run deploy.py
```

Navigate to AgentCore Runtime sandbox to test the agent
```
{"prompt": "How big is sun?"}
```