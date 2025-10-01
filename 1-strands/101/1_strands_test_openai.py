import os
from strands import Agent
from strands.models import OpenAIModel
from strands_tools import calculator

# Set in your terminal first:
# export OPENAI_API_KEY="your-key-here"

# Auto-reads from OPENAI_API_KEY environment variable
model = OpenAIModel(
    model_id="gpt-4o",
    temperature=0.9,
    # max_tokens=2048,
)

# Define Agent
agent_built_in_tools = Agent(
    model=model,
    tools=[calculator]
)

output = agent_built_in_tools("What is the square root of 1764")
print(output)