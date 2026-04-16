"""MCP Client"""

# pylint:disable=W0718

import os
import json
import uuid
import requests
from opentelemetry.trace import get_tracer
from custom_span import otel_span_decorator

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client

HTTP_TIMEOUT = 60
tracer = get_tracer("oauth-invoke-mcp-demo", "1.0.0")


def oauth_broker_ping(url: str) -> dict:
    """Helper function to stroe MCP calls"""
    response = requests.get(
        url=url,
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return {"status": "success"}


def oauth_broker_store_bearer_token(url: str, bearer_token: str) -> dict:
    """Helper function to stroe MCP calls"""
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "user_token": bearer_token
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=payload,
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return {"status": "success"}


def get_inbound_oauth_bearer_token(
        oauth_token_url: str,
        client_id: str,
        client_secret: str,
        scope_string: str
        ) -> dict:
    """Helper function to obtain ACGW inbound OAuth bearer token"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope_string,

    }
    response = requests.post(
        url=oauth_token_url,
        headers=headers,
        data=data,
        timeout=HTTP_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def _invoke_agent(
        bedrock_model,
        mcp_client,
        prompt):
    """strands agent helper"""
    system_prompt = "mask any email or data of birth details"
    with mcp_client:
        tools = mcp_client.list_tools_sync()
        agent = Agent(
            model=bedrock_model,
            tools=tools,
            system_prompt=system_prompt
        )
        return agent(prompt)


def _create_streamable_http_transport(
        gateway_url: str,
        headers):
    """Gateway Streamable HTTP client"""
    return streamablehttp_client(
        gateway_url,
        headers=headers
    )


def _create_sse_transport(
        gateway_url: str,
        headers):
    """Gateway SSE HTTP client"""
    return sse_client(
        gateway_url,
        headers=headers
    )


def _get_bedrock_model(model_id):
    return BedrockModel(
        model_id=model_id
   )


@otel_span_decorator(tracer, "user_profile_agent")
def call_agent(
        gateway_url: str,
        access_token: str,
        prompt: str) -> str:
    """Strands agent to use LinkedIn tool to get user profile"""
    gw_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'MCP-Protocol-Version': '2025-11-25'
    }
    mcp_client = MCPClient(lambda: _create_streamable_http_transport(gateway_url, gw_headers))
    _response = _invoke_agent(
        bedrock_model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0"),
        mcp_client=mcp_client,
        prompt=prompt
    )
    return _response


@otel_span_decorator(tracer, "call_gw_tool")
def call_mcp(
        gateway_url: str,
        access_token: str,
        tool_params: str = None,
        method: str = "tools/list",
        protocol_version: str = '2025-11-25') -> str:
    """Helper function to make MCP calls"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'MCP-Protocol-Version': protocol_version
    }
    payload = {
        "jsonrpc": "2.0",
        "id": f"acgw-demo-{uuid.uuid4().hex}",
        "method": method,
    }
    if tool_params:
        payload["params"] = tool_params
    try:
        response = requests.post(
            gateway_url,
            headers=headers,
            json=payload,
            timeout=HTTP_TIMEOUT
        )
        request_id = (
            response.headers.get('x-amzn-requestid') or
            response.headers.get('x-amz-request-id')
        )
        print("\nAmazon Request ID:", request_id)
        response.raise_for_status()
        print(f"Invoke MCP Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as ex:
        print(ex)
        return


def main():
    """Main function"""

    # Step 1: Check if oauth token broker is online
    oauth_broker_base_url = os.getenv("OAUTH_BROKER_BASE_URL")
    try:
        oauth_broker_ping(url=f"{oauth_broker_base_url}/ping")
    except Exception:
        print("Local OAuth broker not running. Run python oauth2_callback_server.py -r <region>'")
        return

    # Step 2: Obtain Cognito OAuth token for authenticating with ACGW
    cognito_resource_server_id = os.getenv("RESOURCE_SERVER_ID")
    cognito_gateway_scope_name = os.getenv("MCP_TARGET_SCOPE_NAME")
    region = os.getenv("AWS_REGION")
    cognito_user_pool_id = os.getenv("COGNITO_USER_POOL_ID").replace("_", "")
    cognito_client_id = os.getenv("COGNITO_CLIENT_ID")
    cognito_client_secret = os.getenv("COGNITO_CLIENT_SECRET")
    url = f"https://{cognito_user_pool_id}.auth.{region}.amazoncognito.com/oauth2/token"
    try:
        jwt_token = get_inbound_oauth_bearer_token(
            oauth_token_url=url,
            client_id=cognito_client_id,
            client_secret=cognito_client_secret,
            scope_string=f"{cognito_resource_server_id}/{cognito_gateway_scope_name}"
        )
        bearer_token = jwt_token['access_token']
        print(f"Cognito OAuth Bearer Token: {bearer_token[:5]}*****")
    except Exception:
        print("Unable to obtain ACGW inbound OAuth bearer token from Cognito")
        return

    # Step 3: Pass Cognito OAuth bearer token to broker
    # try:
    #     oauth_broker_store_bearer_token(
    #         url=f"{oauth_broker_base_url}/userIdentifier/token",
    #         bearer_token=bearer_token
    #     )
    # except Exception:
    #     print("Error storing OAuth bearer token in broker. Retry.")
    #     return

    # Step 4: Call MCP tool to trigger outbound OAuth
    # gateway_url = os.getenv("ACGW_URL")
    # _meta = {
    #     "aws.bedrock-agentcore.gateway/credentialProviderConfiguration": {
    #         "oauthCredentialProvider": {
    #             # "returnUrl": f"{oauth_broker_base_url}/oauth2/callback",
    #             "forceAuthentication": True
    #         }
    #     }
    # }
    # tool_response = call_mcp(
    #     gateway_url=gateway_url,
    #     access_token=bearer_token,
    #     method="tools/call",
    #     tool_params={
    #         "name": "LinkedInAuthCode___getUserInfo",
    #         "arguments": {},
    #         # "_meta": _meta
    #     }
    # )
    # print(f"tool response: {tool_response}")

    gateway_url = os.getenv("ACGW_URL")
    user_prompt = "Get user name from linkedin user profile"
    agent_response = call_agent(
        gateway_url=gateway_url,
        access_token=bearer_token,
        prompt=user_prompt
    )
    print(f"Agent response: {agent_response}")

if __name__ == "__main__":
    main()
