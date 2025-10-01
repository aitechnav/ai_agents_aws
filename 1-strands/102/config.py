"""Configuration module for the agents orchestrator."""

from strands.models import BedrockModel

# Model configuration
MODEL_CONFIG = {
    "model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0",
    "region_name": "us-east-1",
}

def get_model() -> BedrockModel:
    """Create and return a configured BedrockModel instance."""
    return BedrockModel(**MODEL_CONFIG)

# Agent prompts
RESEARCH_ASSISTANT_PROMPT = """You are a specialized research assistant, anytime there's a
query with a link, process and parse the content of the link with the http_request tool.
Summarize the content of the link in a few sentences."""

AWS_ASSISTANT_PROMPT = """You are a specialized AWS assistant, answer any questions
about AWS services specifically for the user's account."""

MAIN_SYSTEM_PROMPT = """
You are an assistant that routes queries to specialized agents:

- For research queries and parsing links in the query → Use the research_assistant tool
- For AWS queries, specifically for the user's account → Use the aws_assistant tool

At the end of your response, can you also explain which tool you used and why?
Always select the most appropriate tool based on the user's query.
""" 