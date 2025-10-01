"""Agents Orchestrator Package - A multi-agent system for specialized task routing."""

from .orchestrator import AgentsOrchestrator
from .config import get_model
from .tools import get_available_tools

__version__ = "0.0.1"
__author__ = "Anuj Tyagi"
__description__ = "A multi-agent orchestrator system using Strands SDK"

__all__ = [
    "AgentsOrchestrator",
    "get_model",
    "get_available_tools"
] 