import boto3

AGENT_NAME = "strands_direct_deploy"
AGENT_RUNTIME_ID = "strands_direct_deploy-5iGWAs2am7"
REGION = "us-east-1"

ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')
S3_BUCKET_NAME = f"bedrock-agentcore-code-{ACCOUNT_ID}-{REGION}"
S3_PREFIX = f"{AGENT_NAME}/deployment_package.zip"
#AC_EXEC_ROLE_ARN = f"arn:aws:iam::{ACCOUNT_ID}:role/AmazonBedrockAgentCoreSDKRuntimeDirect-{REGION}"
AC_EXEC_ROLE_ARN = "arn:aws:iam::467801433859:role/AmazonBedrockAgentCoreSDKRuntimeDirect-us-east-1"


def deploy():
    s3_client = boto3.client('s3', region_name='us-west-2')
    print("Uploading deployment.zip to S3...")
    s3_client.upload_file( 
        'deployment_package.zip', # archive on file system
        S3_BUCKET_NAME, # bucket name
        S3_PREFIX, # prefix
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
