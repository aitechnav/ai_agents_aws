
# How This Code Works

https://modelcontextprotocol.io/docs/getting-started/intro

```
main.py (FastMCP Server):

Creates MCP Server: FastMCP("hello-mcp-py") creates a local MCP server
Defines Data Model: BioData is a Pydantic model for structured person data
Mock Database: people_db dictionary stores biodata for 5 people
Exposes Tool: @mcp.tool() decorator makes return_biodata available as an MCP tool
Runs Server: mcp.run(transport="stdio") starts the server using stdio transport

Your app.py (MCP Client):

Connects to both AWS docs server and your local server
Lists all available tools from both servers
Creates a Strands Agent with these tools
Makes requests that the agent fulfills using appropriate tools
```

## Steps to Run 

# Run MCP server
python -r requirements.txt
python app.py 

# Install MCP Inspector for testing
npm install -g @modelcontextprotocol/inspector

# Run inspector with your server
mcp-inspector python3 main.py


# How Data flow?

```
When you run python3 app.py:

app.py starts main.py as a subprocess
main.py runs and waits for tool requests
app.py asks main.py: "What tools do you have?"
main.py responds: "I have get_menu_item tool"
app.py creates Agent with this tool
When Agent needs menu data, it calls the tool in main.py
main.py looks up data in menu_db and returns it
Agent receives the data and responds to user

┌─────────────────────────────────────────────────────────────┐
│                         app.py                              │
│              (MCP Client + Strands Agent)                   │
│                                                             │
│  Role: Orchestrator and User Interface                     │
│  - Connects to TWO MCP servers simultaneously              │
│  - Aggregates tools from all servers                       │
│  - Creates Strands AI Agent with combined tools            │
│  - Processes user queries                                  │
│  - Routes requests to appropriate tools                    │
└─────────────────────────────────────────────────────────────┘
                    │                    │
                    │                    │
        ┌───────────┘                    └───────────┐
        │ stdio                                stdio │
        ▼                                            ▼
┌────────────────────────┐              ┌────────────────────────┐
│      main.py           │              │  AWS Documentation     │
│  (Local MCP Server)    │              │    MCP Server          │
│                        │              │  (Remote via uvx)      │
│ Role: Custom Data      │              │                        │
│ - Menu database        │              │ Role: AWS Knowledge    │
│ - get_menu_item tool   │              │ - AWS docs search      │
│ - Fuzzy matching       │              │ - Service info         │
│ - Custom business logic│              │ - Best practices       │
└────────────────────────┘              └────────────────────────┘
```
