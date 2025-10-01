
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json
import sys

try:
    # Load gateway configuration
    print("Loading gateway configuration...")
    with open('gateway_config.json', 'r') as f:
        config = json.load(f)
    print("✓ Configuration loaded")

    # Get access token from Cognito
    print("Getting access token...")
    client = GatewayClient(region_name="us-east-1")
    access_token = client.get_access_token_for_cognito(config['cognito_info']['client_info'])
    print("✓ Access token obtained")

    # Create MCP transport with authentication using streamable HTTP
    print("Creating MCP transport...")
    transport = streamablehttp_client(
        config['gateway_url'], 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print("✓ Transport created")

    # Initialize Bedrock model
    print("Initializing Bedrock model...")
    model = BedrockModel(
        inference_profile_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.7,
        streaming=True
    )
    print("✓ Model initialized")

    # Create MCP client
    print("Creating MCP client...")
    mcp_client = MCPClient(lambda: transport)
    print("✓ MCP client created")

    # Create and run agent
    with mcp_client:
        # Discover available tools
        print("Discovering tools...")
        tools = mcp_client.list_tools_sync()
        print(f"✓ Connected to gateway with {len(tools)} tools")
        
        # List available tools
        print("\nAvailable tools:")
        for tool in tools:
            print(f"  - {tool.tool_name}") #: {tool.description}")
        
        # Create agent with discovered tools
        agent = Agent(model=model, tools=tools)
        
        print("\n" + "="*50)
        print("🤖 AI Agent Ready!")
        print("Ask questions about weather or time.")
        print("Type 'exit' or 'quit' to stop.")
        print("="*50 + "\n")
        
        # Interactive chat loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                    
                print("Agent: ", end="", flush=True)
                response = agent(user_input)
                print()  # Add newline after response
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'exit' to quit.\n")

except FileNotFoundError:
    print("❌ gateway_config.json not found")
    print("Please run create_gateway_with_targets.py first")
    sys.exit(1)
except Exception as e:
    print(f"❌ Failed to initialize agent: {e}")
    print("Please check your configuration and try again")
    sys.exit(1)
