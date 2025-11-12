# AI Agents Workshop - AWS, MCP & Frameworks

Hands-on workshop covering AI agent frameworks, Model Context Protocol, and AWS AgentCore.

## Workshop Structure (3.5 hours)

### Section 1: AI Agent Frameworks 
Build agents using LangChain
- **Theory**: Framework comparison, when to use each
- **Labs**: Build 3 different agents with increasing complexity

### Section 2: Model Context Protocol - MCP 
Connect AI agents to data sources using MCP
- **Theory**: MCP architecture and benefits
- **Labs**: Build MCP server and integrate with Claude

### Section 3: AWS Bedrock AgentCore
Deploy production-ready agents on AWS
- **Theory**: AgentCore services and features
- **Labs**: Deploy agents with runtime, memory, and observability

---

## Prerequisites

```bash
# Required
- AWS account with Bedrock access enabled
- Python 3.9+
- AWS CLI configured

# Setup
git clone https://github.com/aitechnav/ai_agents_aws.git
cd ai_agents_aws
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your AWS credentials
```

---

## Section 1: Agent Frameworks

### Quick Comparison
- **LangChain**: Simple chains, prototyping → Use for basic agents
- **LangGraph**: Complex workflows, state management → Use for multi-step processes
- **CrewAI**: Multi-agent teams → Use for specialized collaboration

### Lab 1: Basic LangChain Agent
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_aws import ChatBedrock

@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions"""
    return str(eval(expression))

llm = ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0")
agent = create_tool_calling_agent(llm, [calculator], prompt)
executor = AgentExecutor(agent=agent, tools=[calculator])

result = executor.invoke({"input": "What is 157 * 23?"})
```

### Lab 2: LangGraph Workflow
```python
from langgraph.graph import StateGraph

workflow = StateGraph(State)
workflow.add_node("classify", classify_query)
workflow.add_node("process", process_query)
workflow.add_conditional_edges("classify", route_query)
app = workflow.compile()

result = app.invoke({"query": "user question"})
```

### Lab 3: CrewAI Multi-Agent
```python
from crewai import Agent, Task, Crew

researcher = Agent(role='Researcher', goal='Research AWS services')
writer = Agent(role='Writer', goal='Write documentation')

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
```

---

## Section 2: Model Context Protocol (MCP)

### What is MCP?
Open standard for connecting AI models to data sources. Think USB-C for AI.

### Lab 1: Build MCP Server
```python
from mcp.server import Server
from mcp.types import Resource, Tool

app = Server("aws-mcp-server")

@app.list_resources()
async def list_resources():
    return [Resource(uri="aws://s3/buckets", name="S3 Buckets")]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_buckets":
        return s3.list_buckets()
```

### Lab 2: Use MCP with Claude
```python
# Configure Claude Desktop with your MCP server
# ~/.config/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "aws": {
      "command": "python",
      "args": ["path/to/aws_mcp_server.py"]
    }
  }
}
```

---

## Section 3: AWS AgentCore

### AgentCore Services
- **Runtime**: Deploy and scale agents securely
- **Memory**: Persistent context across sessions
- **Gateway**: Transform APIs into agent tools
- **Observability**: Monitor with CloudWatch and X-Ray

### Lab 1: Deploy to AgentCore Runtime
```python
from strands import Agent, Tool
from strands.runtime import AgentCoreRuntime

agent = Agent(
    name="aws-assistant",
    instructions="You are an AWS expert assistant",
    model=llm,
    tools=[search_docs, calculate_cost]
)

runtime = AgentCoreRuntime(region="us-east-1")
deployed_agent = runtime.create_agent(agent, name="prod-agent")

# Invoke
response = deployed_agent.invoke(
    input="How much does Lambda cost?",
    session_id="user-123"
)
```

### Lab 2: Add Memory
```python
from strands.memory import AgentCoreMemory

memory = AgentCoreMemory(memory_id="support-agent-memory")
agent = Agent(name="support-agent", model=llm, memory=memory)

# Memory persists across sessions
response = agent.run(input=message, user_id="user-123")
```

### Lab 3: Enable Observability
```python
from strands.observability import AgentCoreObservability

observability = AgentCoreObservability(
    log_group="/aws/agentcore/agent",
    enable_xray=True
)

runtime = AgentCoreRuntime(observability=observability)
# All invocations now logged to CloudWatch and X-Ray
```

---

## Quick Start

```bash
# Test basic agent
python examples/basic_agent.py

# Test agent with tools
python examples/agent_with_tools.py

# Run interactive mode
python examples/basic_agent.py
# Choose option 2 for interactive chat
```

---

## Resources

- **LangChain**: https://python.langchain.com/docs/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **CrewAI**: https://docs.crewai.com/
- **MCP**: https://spec.modelcontextprotocol.io/
- **AgentCore**: https://aws.amazon.com/bedrock/agentcore/

---

## Cost Estimate

Workshop duration: ~$3-5 total
- Bedrock (Claude Sonnet): ~$2
- AgentCore Runtime: ~$1
- Other services: ~$1

---

## Troubleshooting

**Bedrock Access Denied**: Go to AWS Console → Bedrock → Model Access → Enable Claude models

**Dependencies Failed**: 
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**AWS Credentials**: 
```bash
aws configure
aws sts get-caller-identity
```

---

## Repository Structure

```
ai_agents_aws/
├── section-01-frameworks/
│   ├── lab-1-langchain/
│   ├── lab-2-langgraph/
│   └── lab-3-crewai/
├── section-02-mcp/
│   ├── lab-1-server/
│   └── lab-2-client/
├── section-03-agentcore/
│   ├── lab-1-runtime/
│   ├── lab-2-memory/
│   └── lab-3-observability/
├── examples/
├── requirements.txt
├── .env.example
└── README.md
```

---

**Maintainer**: [Anuj Kumar](https://github.com/aitechnav)  
**License**: MIT
