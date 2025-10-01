"""
Create OAuth autorizer with cognito service
"""
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import logging
import json
import os

# Setup the client
client = GatewayClient(region_name="us-east-1")  # Change to your region
client.logger.setLevel(logging.DEBUG)

print("Step 1: Creating OAuth authorizer with Cognito...")
# This automatically creates a Cognito user pool for authentication
cognito_response = client.create_oauth_authorizer_with_cognito("LambdaAuthorizer")
print(f"OAuth Client ID: {cognito_response['client_info']['client_id']}")
print(f"OAuth Client Secret: {cognito_response['client_info']['client_secret']}")

print("\nStep 2: Creating the Gateway...")
# Create the gateway with semantic search enabled
gateway = client.create_mcp_gateway(
    name="LambdaMCP",
    authorizer_config=cognito_response["authorizer_config"],
    enable_semantic_search=True
)
print(f"Gateway URL: {gateway['gatewayUrl']}")
print(f"Gateway ID: {gateway['gatewayId']}")

print("\nStep 3: Creating Lambda target...")

# Get Lambda ARN from environment variable or prompt user
lambda_arn = os.getenv('LAMBDA_ARN')
if not lambda_arn:
    print("Please set LAMBDA_ARN environment variable or update this script with your Lambda ARN")
    print("Example: export LAMBDA_ARN=arn:aws:lambda:us-east-1:629057033187:function:test_lambda")
    lambda_arn = input("Enter your Lambda ARN: ").strip()

# Define the tools schema for your Lambda
tool_schema = [
    {
        "name": "get_weather",
        "description": "Get weather information for a location",
        "inputSchema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_time", 
        "description": "Get current time for a timezone",
        "inputSchema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone (e.g., 'UTC', 'America/New_York', 'America/Los_Angeles'). Defaults to UTC if not provided."
                }
            },
            "required": []  # timezone is optional since Lambda has default
        }
    }
]

# Create Lambda target with custom schema
lambda_target = client.create_mcp_gateway_target(
    gateway=gateway,
    name="WeatherAndTimeTools",
    target_type="lambda",
    target_payload={
        "lambdaArn": lambda_arn,
        "toolSchema": {
            "inlinePayload": tool_schema
        }
    }
)
print(f"Lambda target created: {lambda_target['targetId']}")

# Save configuration for later use
config = {
    "gateway_url": gateway['gatewayUrl'],
    "gateway_id": gateway['gatewayId'],
    "client_id": cognito_response['client_info']['client_id'],
    "client_secret": cognito_response['client_info']['client_secret'],
    "cognito_info": cognito_response,
    "target_id": lambda_target['targetId'],
    "lambda_arn": lambda_arn
}

with open('gateway_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("\nConfiguration saved to gateway_config.json")
print(f"Gateway is ready at: {gateway['gatewayUrl']}")
print(f"\nNext steps:")
print(f"1. Run 'python test_gateway.py' to test the gateway")
print(f"2. Run 'python agent_with_gateway.py' to start interactive agent")
