# agent_with_gateway.py
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json
import sys
import boto3
import os

try:
    # Get AWS credentials and force them into environment
    print("Loading AWS credentials...")
    session = boto3.Session(region_name='us-east-1')
    credentials = session.get_credentials()
    
    if credentials is None:
        print("❌ No AWS credentials found!")
        sys.exit(1)
    
    # Force credentials into environment variables for Strands
    frozen_creds = credentials.get_frozen_credentials()
    os.environ['AWS_ACCESS_KEY_ID'] = frozen_creds.access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = frozen_creds.secret_key
    if frozen_creds.token:
        os.environ['AWS_SESSION_TOKEN'] = frozen_creds.token
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['AWS_REGION'] = 'us-east-1'
    
    print(f"✓ Credentials loaded")
    
    # Verify Bedrock access works with boto3 directly
    print("Testing Bedrock access...")
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    test_response = bedrock_runtime.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": "test"}]}]
    )
    print("✓ Bedrock access confirmed")
    
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

    # Create MCP transport
    print("Creating MCP transport...")
    transport = streamablehttp_client(
        config['gateway_url'], 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print("✓ Transport created")

    # Initialize Bedrock model - try passing boto3 client directly
    print("Initializing Bedrock model...")
    
    # Option 1: Try with explicit region and credentials
    model = BedrockModel(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
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
            print(f"  - {tool.tool_name}")
        
        # Create agent with discovered tools
        print("\nCreating agent...")
        agent = Agent(model=model, tools=tools)
        print("✓ Agent created")
        
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
                
                # Try calling the agent
                response = agent(user_input)
                
                # Handle response properly
                if hasattr(response, 'message'):
                    message = response.message
                    if isinstance(message, dict) and 'content' in message:
                        content = message['content']
                        if isinstance(content, list) and len(content) > 0:
                            text = content[0].get('text', '')
                            print(text)
                        else:
                            print(content)
                    else:
                        print(message)
                else:
                    print(str(response))
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
                # Debug: Print more info about the error
                import traceback
                print("\nFull error traceback:")
                traceback.print_exc()
                
                # Check if credentials are still in environment
                print("\nEnvironment check:")
                print(f"  AWS_ACCESS_KEY_ID: {'SET' if os.getenv('AWS_ACCESS_KEY_ID') else 'NOT SET'}")
                print(f"  AWS_SECRET_ACCESS_KEY: {'SET' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'NOT SET'}")
                print(f"  AWS_REGION: {os.getenv('AWS_REGION', 'NOT SET')}")
                
                print("\nPlease try again or type 'exit' to quit.\n")

except FileNotFoundError:
    print("❌ gateway_config.json not found")
    sys.exit(1)
except Exception as e:
    print(f"❌ Failed to initialize agent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
