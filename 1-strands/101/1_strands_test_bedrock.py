from strands import Agent
from strands.models import BedrockModel #select appropriate Model Provider

# Model Provider
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1",
    temperature=0.9,
    # max_tokens=2048,
)

# built-in tools
from strands_tools import calculator

# Define Agent
agent_built_in_tools = Agent(
    model=model,
    tools=[calculator]
)

output = agent_built_in_tools("What is the square root of 1764")
print (output)
