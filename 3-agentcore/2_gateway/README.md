# AWS Agent Core Gateway: Lambda to MCP Tools Tutorial

Transform your AWS Lambda functions into secure MCP (Model Context Protocol) tools using AWS Bedrock Agent Core Gateway. This tutorial demonstrates how to build enterprise-ready AI agents with OAuth authentication and serverless scaling.

## Architecture Overview

```
AI Agent → Agent Core Gateway → AWS Lambda Function
    ↑            ↑                    ↑
Strands      OAuth + MCP         Business Logic
Framework    Protocol
```

## What You'll Build

- **Secure MCP Gateway** with OAuth authentication via AWS Cognito
- **Lambda-powered Tools** for weather and time queries
- **Interactive AI Agent** using AWS Strands framework
- **Complete Integration** from Lambda to AI agent

## Prerequisites

- AWS account with appropriate permissions
- Python 3.10+ installed
- AWS CLI configured with credentials

## Installation

1. **Clone this repository**
```bash
git clone https://github.com/yourusername/aws-agentcore-gateway
cd aws-agentcore-gateway
```

## Quick Start

### Step 1: Create Lambda Function

1. Go to AWS Lambda Console
2. Create new function named `test_lambda`
3. Copy the code from `lambda_function.py`
4. **Important**: Click "Deploy" to save changes

### Step 2: Create MCP Gateway

1. Update the Lambda ARN in `create_gateway_with_targets.py`
2. Run the gateway creation script:
```bash
python create_gateway_with_targets.py
```

### Step 3: Test the Gateway

```bash
python test_gateway.py
```

### Step 4: Run Interactive Agent

```bash
python agent_with_gateway.py
```

## File Structure

```
aws-agentcore-mcp-tutorial/
├── README.md
├── lambda_function.py              # Lambda function code
├── create_gateway_with_targets.py  # Gateway setup script
├── test_gateway.py                 # Gateway testing script
├── agent_with_gateway.py           # Interactive AI agent


```

## Key Components

### AWS Services Used

- **AWS Bedrock Agent Core Gateway**: Managed MCP server
- **AWS Lambda**: Serverless function backend
- **AWS Cognito**: OAuth authentication
- **AWS Strands**: AI agent framework

### Agent Core Specific Features

- **Tool Name Prefixing**: Gateway adds target name prefix (`WeatherAndTimeTools___get_weather`)
- **Client Context**: Tool names passed via `context.client_context.custom['bedrockAgentCoreToolName']`
- **OAuth Integration**: Automatic Cognito user pool creation
- **Semantic Search**: Built-in tool discovery

## Configuration

The setup script generates `gateway_config.json` with:

```json
{
  "gateway_url": "https://your-gateway-url.amazonaws.com/mcp",
  "gateway_id": "your-gateway-id",
  "client_id": "your-oauth-client-id",
  "client_secret": "your-oauth-secret",
  "cognito_info": {...},
  "target_id": "your-target-id"
}
```

## Usage Examples

### Test Weather Tool
```bash
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -X POST "YOUR_GATEWAY_URL" \
     -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "WeatherAndTimeTools___get_weather", "arguments": {"location": "Boston"}}}'
```

### Interactive Agent Queries
- "What's the weather in Miami?"
- "What time is it in Tokyo?"
- "Get me the weather for Seattle"

## Token Management

Cognito tokens expire after 1 hour. Use the provided utility:

```bash
# Refresh token and test gateway
source get_token_and_test.sh
```

## Traditional MCP vs Agent Core Gateway

| Aspect | Traditional MCP | Agent Core Gateway |
|--------|----------------|-------------------|
| **Deployment** | Manual server setup | One-command creation |
| **Authentication** | DIY implementation | Built-in OAuth |
| **Scaling** | Manual configuration | Automatic serverless |
| **Security** | Custom SSL/certs | Managed TLS |
| **Monitoring** | Custom metrics | CloudWatch integration |
| **Cost** | Always-on servers | Pay-per-use |

## Troubleshooting

### Common Issues

**"Invalid Bearer token"**
- Token expired (1-hour limit)
- Run `source get_token_and_test.sh` to refresh

**"Unknown tool: unknown"**
- Lambda not parsing tool names correctly
- Check `bedrockAgentCoreToolName` key casing

**Lambda changes not applied**
- Must click "Deploy" button in Lambda console
- Code changes don't take effect until deployed

### Debug Commands

```bash
# Check token validity
python -c "
import json
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
with open('gateway_config.json', 'r') as f:
    config = json.load(f)
client = GatewayClient(region_name='us-east-1')
token = client.get_access_token_for_cognito(config['cognito_info']['client_info'])
print('Token valid:', len(token) > 100)
"

# Test Lambda directly
aws lambda invoke --function-name test_lambda --payload '{"tool_name":"get_weather","location":"Boston"}' response.json
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request
