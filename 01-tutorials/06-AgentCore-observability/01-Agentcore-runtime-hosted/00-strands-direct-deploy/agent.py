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
