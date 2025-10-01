"""
- Basic example of strands with tools
Tools doc: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/tools_overview/
Available tools: https://github.com/strands-agents/tools/tree/main/src/strands_tools
"""
from strands import Agent
from strands.models import BedrockModel
from strands import tool

# Model Provider
model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1",
    temperature=0.9,
    # max_tokens=2048,
)


# Custom Tool Sample
from transformers import pipeline
classifier = pipeline("sentiment-analysis")


# # https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english
# classifier = pipeline(
#     "sentiment-analysis",
#     model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
#     revision="714eb0f"
# )

@tool
def sent_analyzer(inp_text: str) -> str:
    sent_text = classifier(inp_text)
    return sent_text[0]['label']

# built-in tools
from strands_tools import calculator
from strands_tools import file_read, file_write

# Define Agent with built-in and custom tools
agent_custom_tools = Agent(
    model=model,
    tools=[calculator, sent_analyzer,file_read, file_write]
)

tool1 = agent_custom_tools("Analyze the sentiment of the following text: I am super happy!")
print (tool1)

tool2 = agent_custom_tools("Multiply 50 and 50") # here we can see the calculator is still appropriately used
print (tool2)


system_prompt = "You are an agent which can read and write files to current directory"
local_agent = Agent(
    system_prompt=system_prompt,
    model=model,
    tools=[file_read, file_write],  
)
tool3 = agent_custom_tools("can you create a test123.md file with content about file permissions in Linux ?")
