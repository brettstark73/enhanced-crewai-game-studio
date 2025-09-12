"""
CrewAI Framework - Reusable utilities for CrewAI projects

Provides validation, debugging, and enhanced configuration for CrewAI workflows.
"""

from .crewai_validator import CrewAIValidator, validate_before_run
from .agent_factory import AgentFactory
from .task_builder import TaskBuilder
from .crew_debugger import CrewDebugger, run_crew_with_debugging

__version__ = "1.0.0"
__all__ = [
    'CrewAIValidator',
    'validate_before_run',
    'AgentFactory', 
    'TaskBuilder',
    'CrewDebugger',
    'run_crew_with_debugging'
]