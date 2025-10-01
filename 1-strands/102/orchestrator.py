"""Main orchestrator module for routing queries to specialized agents."""

import logging
from typing import Optional, Dict, Any
from strands import Agent
from config import get_model, MAIN_SYSTEM_PROMPT
from tools import get_available_tools
from utils import log_query_response, sanitize_query, format_response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentsOrchestrator:
    """Main orchestrator class for routing queries to specialized agents."""
    
    def __init__(self, callback_handler: Optional[Any] = None):
        """
        Initialize the orchestrator with configured model and tools.
        
        Args:
            callback_handler: Optional callback handler for the agent
        """
        logger.info("Initializing Agents Orchestrator...")
        
        self.model = get_model()
        self.tools = get_available_tools()
        
        self.agent = Agent(
            model=self.model,
            system_prompt=MAIN_SYSTEM_PROMPT,
            tools=self.tools,
            callback_handler=callback_handler
        )
        
        logger.info(f"Orchestrator initialized with {len(self.tools)} tools")
    
    def _extract_tool_usage(self, agent_result: Any, response: str) -> Optional[str]:
        """
        Extract tool usage information from agent result or response.
        
        Args:
            agent_result: The AgentResult object
            response: The string response
            
        Returns:
            Name of the tool used, or None if not determinable
        """
        try:
            # Try to get tool info from AgentResult object attributes
            if hasattr(agent_result, 'tool_calls') and agent_result.tool_calls:
                return agent_result.tool_calls[0].get('name', 'unknown_tool')
            elif hasattr(agent_result, 'metadata') and agent_result.metadata:
                return agent_result.metadata.get('tool_used')
            
            # Fallback: analyze response content for tool indicators
            response_lower = response.lower()
            if 'research_assistant' in response_lower or 'processing url' in response_lower:
                return 'research_assistant'
            elif 'aws_assistant' in response_lower or 's3 bucket' in response_lower or 'aws' in response_lower:
                return 'aws_assistant'
            
        except Exception as e:
            logger.debug(f"Could not extract tool usage: {str(e)}")
        
        return None
    
    def process_query(self, query: str, include_metadata: bool = False) -> Dict[str, Any]:
        """
        Process a query and return the response.
        
        Args:
            query: The input query to process
            include_metadata: Whether to include metadata in the response
            
        Returns:
            Dictionary containing the response and optional metadata
        """
        try:
            # Sanitize input
            sanitized_query = sanitize_query(query)
            logger.info(f"Processing query: {sanitized_query[:50]}...")
            
            # Get response from orchestrator
            agent_result = self.agent(sanitized_query)
            
            # Extract text from AgentResult object
            response = str(agent_result) if agent_result else "No response received"
            
            # Try to extract tool usage information
            tool_used = self._extract_tool_usage(agent_result, response)
            
            # Log the interaction
            log_query_response(sanitized_query, response, tool_used)
            
            # Format and return response
            return format_response(response, include_metadata)
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)
            return format_response(error_msg, include_metadata)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the orchestrator configuration.
        
        Returns:
            Dictionary with orchestrator information
        """
        # Get model info from config instead of model object
        from config import MODEL_CONFIG
        
        return {
            "model_id": MODEL_CONFIG.get("model_id", "unknown"),
            "region": MODEL_CONFIG.get("region_name", "unknown"),
            "available_tools": len(self.tools),
            "tool_names": [tool.__name__ for tool in self.tools],
            "model_type": type(self.model).__name__
        }