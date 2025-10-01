from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

# Connect to an MCP server using stdio transport
# Note: uvx command syntax differs by platform

# Utilize built-in MCP server, example AWS docs
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))

# Connect to your local MCP server (Python script)
local_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="python3",
        args=["main.py"]  
    )
))

# Create an agent with MCP tools
with stdio_mcp_client, local_mcp_client:
    # Get the tools from the MCP server
    tools = stdio_mcp_client.list_tools_sync() + local_mcp_client.list_tools_sync()
    available_tools = []
    for tool in tools:
        print("Name:", tool.tool_name)
        print("Type:", tool.tool_type)
        print("Spec:", tool.tool_spec)
        print("Display:", tool.get_display_properties())
        print("-" * 40)
        available_tools.append(tool.tool_name)
    print(f"Available tools: {available_tools}")
    # Create an agent with these tools
    agent = Agent(tools=tools)
    print("-------------------")
    print("Request one:")
    agent("What is AWS Lambda?")
    print("-------------------")
    print("Request two:")
    agent("Tell me about Chicken Tikka - price, spiciness and calories")