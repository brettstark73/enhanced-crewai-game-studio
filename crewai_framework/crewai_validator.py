"""
CrewAI Validation Framework
Catches common configuration issues before running crews
"""

import re
from typing import List, Dict, Any
from crewai import Crew, Task, Agent

class CrewAIValidator:
    """Validates CrewAI configurations and identifies common issues"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def validate_crew(self, crew: Crew, inputs: Dict[str, Any] = None) -> Dict[str, List[str]]:
        """
        Comprehensive crew validation
        Returns dict with 'errors', 'warnings', and 'suggestions'
        """
        self.issues = []
        self.warnings = []
        
        if inputs:
            self._validate_task_templates(crew.tasks, inputs)
        
        self._validate_task_dependencies(crew.tasks)
        self._validate_agent_capabilities(crew.agents, crew.tasks)
        self._validate_expected_outputs(crew.tasks)
        self._validate_crew_process(crew)
        
        return {
            'errors': self.issues,
            'warnings': self.warnings,
            'suggestions': self._generate_suggestions(crew)
        }
    
    def _validate_task_templates(self, tasks: List[Task], inputs: Dict[str, Any]):
        """Check if template variables in task descriptions match available inputs"""
        available_vars = set(inputs.keys())
        
        for i, task in enumerate(tasks):
            template_vars = self._extract_template_vars(task.description)
            missing_vars = template_vars - available_vars
            
            if missing_vars:
                self.issues.append(
                    f"Task {i+1} ({task.agent.role}): Missing template variables: {missing_vars}"
                )
                self.issues.append(
                    f"Available variables: {available_vars}"
                )
    
    def _extract_template_vars(self, text: str) -> set:
        """Extract {variable} patterns from text"""
        return set(re.findall(r'{(\w+)}', text))
    
    def _validate_task_dependencies(self, tasks: List[Task]):
        """Check if tasks have proper context dependencies for sequential execution"""
        for i, task in enumerate(tasks[1:], 1):  # Skip first task
            if not hasattr(task, 'context') or not task.context:
                self.warnings.append(
                    f"Task {i+1} ({task.agent.role}): No context from previous tasks. "
                    f"May not receive output from Task {i}"
                )
    
    def _validate_agent_capabilities(self, agents: List[Agent], tasks: List[Task]):
        """Check if agents have tools needed for their tasks"""
        capability_keywords = {
            'file': ['write', 'create', 'save', 'generate files'],
            'read': ['read', 'analyze', 'review'],
            'web': ['fetch', 'scrape', 'api'],
            'database': ['database', 'sql', 'store']
        }
        
        for i, (agent, task) in enumerate(zip(agents, tasks)):
            task_text = task.description.lower()
            agent_tools = getattr(agent, 'tools', []) or []
            
            # Check for file operations
            if any(keyword in task_text for keyword in capability_keywords['file']):
                if not any('file' in str(tool).lower() or 'write' in str(tool).lower() 
                          for tool in agent_tools):
                    self.warnings.append(
                        f"Task {i+1} ({agent.role}): Requires file operations but agent has no file tools"
                    )
    
    def _validate_expected_outputs(self, tasks: List[Task]):
        """Check if expected outputs are specific enough"""
        vague_outputs = ['document', 'plan', 'strategy', 'analysis']
        
        for i, task in enumerate(tasks):
            if hasattr(task, 'expected_output') and task.expected_output:
                output_lower = task.expected_output.lower()
                if any(vague in output_lower for vague in vague_outputs):
                    if not any(specific in output_lower for specific in 
                             ['file', 'code', 'html', 'json', 'specific']):
                        self.warnings.append(
                            f"Task {i+1} ({task.agent.role}): Expected output is vague. "
                            f"Consider specifying file types or formats."
                        )
    
    def _validate_crew_process(self, crew: Crew):
        """Validate crew process configuration"""
        if len(crew.tasks) > 1 and crew.process.name == 'sequential':
            # Check if tasks build on each other
            if not any(hasattr(task, 'context') and task.context for task in crew.tasks[1:]):
                self.warnings.append(
                    "Sequential process but no task contexts defined. "
                    "Tasks may not share information properly."
                )
    
    def _generate_suggestions(self, crew: Crew) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Suggest adding context to sequential tasks
        if crew.process.name == 'sequential' and len(crew.tasks) > 1:
            suggestions.append(
                "Consider adding context=[previous_task] to tasks 2+ for better information flow"
            )
        
        # Suggest adding tools to agents
        for agent in crew.agents:
            if not getattr(agent, 'tools', None):
                suggestions.append(
                    f"Consider adding tools to {agent.role} agent for enhanced capabilities"
                )
        
        return suggestions
    
    def print_validation_report(self, validation_result: Dict[str, List[str]]):
        """Print a formatted validation report"""
        print("🔍 CrewAI Validation Report")
        print("=" * 50)
        
        if validation_result['errors']:
            print("❌ ERRORS (Must Fix):")
            for error in validation_result['errors']:
                print(f"   • {error}")
            print()
        
        if validation_result['warnings']:
            print("⚠️  WARNINGS:")
            for warning in validation_result['warnings']:
                print(f"   • {warning}")
            print()
        
        if validation_result['suggestions']:
            print("💡 SUGGESTIONS:")
            for suggestion in validation_result['suggestions']:
                print(f"   • {suggestion}")
            print()
        
        if not any(validation_result.values()):
            print("✅ No issues found!")


def validate_before_run(crew: Crew, inputs: Dict[str, Any] = None) -> bool:
    """
    Convenience function to validate and optionally abort if errors found
    Returns True if safe to proceed, False if errors exist
    """
    validator = CrewAIValidator()
    result = validator.validate_crew(crew, inputs)
    validator.print_validation_report(result)
    
    return len(result['errors']) == 0