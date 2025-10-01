"""Utility functions for the agents orchestrator."""

import logging
from typing import Optional, Dict, Any
import json
from datetime import datetime

logger = logging.getLogger(__name__)


def log_query_response(query: str, response: str, tool_used: Optional[str] = None) -> None:
    """
    Log query and response for debugging purposes.
    
    Args:
        query: The input query
        response: The agent's response
        tool_used: The tool that was used (if any)
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "query": query[:100] + "..." if len(query) > 100 else query,
        "response_length": len(response),
        "tool_used": tool_used
    }
    logger.info(f"Query processed: {json.dumps(log_entry, indent=2)}")


def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL appears valid, False otherwise
    """
    return url.startswith(('http://', 'https://')) and len(url) > 10


def sanitize_query(query: str) -> str:
    """
    Basic query sanitization.
    
    Args:
        query: Input query to sanitize
        
    Returns:
        Sanitized query
    """
    # Remove any potentially harmful characters
    sanitized = query.strip()
    # Limit query length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000] + "..."
    return sanitized


def format_response(response: str, include_metadata: bool = False) -> Dict[str, Any]:
    """
    Format response with optional metadata.
    
    Args:
        response: The response text
        include_metadata: Whether to include metadata
        
    Returns:
        Formatted response dictionary
    """
    result = {"response": response}
    
    if include_metadata:
        result["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "response_length": len(response),
            "word_count": len(response.split())
        }
    
    return result 