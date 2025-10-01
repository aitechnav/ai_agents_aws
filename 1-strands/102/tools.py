"""Custom tools for the agents orchestrator."""

import logging
from strands import Agent, tool
from strands_tools import http_request, use_aws
from config import RESEARCH_ASSISTANT_PROMPT, AWS_ASSISTANT_PROMPT

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def research_assistant(url: str) -> str:
    """
    Process links and return the content of the link.

    Args:
        url: A URL to parse and return the content of the link

    Returns:
        The content of the link
    """
    try:
        logger.info(f"Processing URL: {url}")
        
        # Create specialized research agent
        research_agent = Agent(
            system_prompt=RESEARCH_ASSISTANT_PROMPT,
            tools=[http_request]
        )

        # Make a simple GET request to URL provided
        response = research_agent.tool.http_request(
            method="GET",
            url=url,
            convert_to_markdown=True
        )

        output = response['content'][2]['text']
        logger.info("Successfully processed URL content")
        return output
        
    except Exception as e:
        error_msg = f"Error in research assistant: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def aws_assistant(query: str) -> str:
    """
    Answer questions about AWS services.

    Args:
        query: A question about AWS services

    Returns:
        A detailed answer to the question
    """
    try:
        logger.info(f"Processing AWS query: {query[:50]}...")
        
        aws_agent = Agent(
            system_prompt=AWS_ASSISTANT_PROMPT,
            tools=[use_aws]
        )
        
        agent_result = aws_agent(query)
        response = str(agent_result) if agent_result else "No response received"
        logger.info("Successfully processed AWS query")
        return response
        
    except Exception as e:
        error_msg = f"Error in AWS assistant: {str(e)}"
        logger.error(error_msg)
        return error_msg

def get_available_tools():
    """Return a list of available tools."""
    return [research_assistant, aws_assistant] 