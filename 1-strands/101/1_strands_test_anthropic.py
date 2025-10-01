from strands import Agent
from strands.models import AnthropicModel  # Change this import

# Model Provider - Anthropic
# export ANTHROPIC_API_KEY="your-key-here"
model = AnthropicModel(
    model_id="claude-sonnet-4-5-20250929",  # or other Claude models
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
print(output)