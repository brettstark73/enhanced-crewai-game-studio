"""
CrewAI Task Builder
Creates properly connected tasks with context dependencies and clear outputs
"""

from crewai import Task
from typing import List, Dict, Any, Optional

class TaskBuilder:
    """Builder for creating properly connected CrewAI tasks"""
    
    def __init__(self):
        self.tasks = []
    
    def create_sequential_tasks(self, task_configs: List[Dict[str, Any]]) -> List[Task]:
        """
        Create sequential tasks with automatic context dependencies
        
        Args:
            task_configs: List of task configuration dictionaries
                Each should have: description, agent, expected_output
                Optional: context (overrides auto-context)
        """
        tasks = []
        
        for i, config in enumerate(task_configs):
            # Auto-add context from previous task (except first task)
            if i > 0 and 'context' not in config:
                config['context'] = [tasks[i-1]]
            
            task = Task(**config)
            tasks.append(task)
        
        return tasks
    
    def create_development_workflow_tasks(self, agents: Dict[str, Any], inputs: Dict[str, Any]) -> List[Task]:
        """
        Create a standard software development workflow with proper task dependencies
        
        Args:
            agents: Dictionary with keys: product_manager, software_architect, 
                   full_stack_developer, qa_engineer, devops_engineer
            inputs: Available input variables for templates
        """
        
        # Build input variable string for templates
        input_vars = '\n'.join([f"    {key}: {{{key}}}" for key in inputs.keys()])
        
        # 1. Product Requirements Task
        requirements_task = Task(
            description=f"""Analyze the project and create comprehensive product requirements:
            - Define the core problem being solved and key objectives
            - Identify target users and their specific needs
            - Create detailed user stories with acceptance criteria
            - Define MVP features vs future enhancements with clear priorities
            - Specify functional and non-functional requirements
            - Consider scalability and performance requirements
            - Define success metrics and KPIs
            - Create a clear feature specification document
            
            Project Details:
{input_vars}
            
            IMPORTANT: Create a detailed requirements document that the next team members can use.""",
            agent=agents['product_manager'],
            expected_output="Comprehensive product requirements document with user stories, prioritized features, acceptance criteria, and technical requirements"
        )
        
        # 2. Architecture Design Task
        architecture_task = Task(
            description=f"""Based on the product requirements, design the complete system architecture:
            - Choose appropriate technology stack (frontend, backend, database)
            - Design system architecture and component relationships
            - Define database schema and data models if needed
            - Plan API design and endpoints (if applicable)
            - Consider security requirements and implementation
            - Plan for scalability and performance optimization
            - Create detailed technical specifications
            - Define development environment setup requirements
            - Provide clear architectural decisions and rationale
            
            Project Details:
{input_vars}
            
            Use the requirements from the previous task to inform all architectural decisions.""",
            agent=agents['software_architect'],
            context=[requirements_task],
            expected_output="Complete technical architecture document with technology stack, system design diagrams, database schema, and implementation specifications"
        )
        
        # 3. Implementation Task
        development_task = Task(
            description=f"""Implement the complete application based on the architecture and requirements:
            - Set up project structure and development environment
            - Implement ALL core features according to requirements
            - Create database models and setup (if needed)
            - Build all necessary files (HTML, CSS, JavaScript, etc.)
            - Implement user interface and user experience
            - Add proper error handling and input validation
            - Follow coding best practices and standards
            - Create comprehensive inline documentation
            - Ensure responsive design and cross-browser compatibility
            
            Project Details:
{input_vars}
            
            CRITICAL: You MUST create actual files using FileWriterTool. This is not a planning task - 
            you need to write the complete, working application code.
            
            Use both the requirements and architecture from previous tasks to guide implementation.""",
            agent=agents['full_stack_developer'],
            context=[requirements_task, architecture_task],
            expected_output="Complete working application with all source files created (HTML, CSS, JavaScript, etc.) and comprehensive documentation"
        )
        
        # 4. Testing Task
        testing_task = Task(
            description=f"""Create comprehensive testing strategy and test the implemented application:
            - Review the implemented code for quality and adherence to requirements
            - Create detailed test plan covering all implemented features
            - Design and implement unit tests for core functionality
            - Create integration test scenarios for user workflows
            - Perform manual testing of all user-facing features
            - Test responsive design and cross-browser compatibility
            - Validate security considerations and error handling
            - Create user acceptance test cases
            - Document any bugs found and suggested improvements
            
            Project Details:
{input_vars}
            
            Test the actual implemented application from the development task.""",
            agent=agents['qa_engineer'],
            context=[requirements_task, architecture_task, development_task],
            expected_output="Complete testing report with test plans, test results, quality assessment, and any bug reports or recommendations"
        )
        
        # 5. Deployment Task
        deployment_task = Task(
            description=f"""Design deployment strategy and create deployment documentation:
            - Analyze the implemented application's deployment needs
            - Choose appropriate hosting platform and services
            - Create deployment scripts and configuration files
            - Design CI/CD pipeline for automated deployment
            - Plan monitoring, logging, and error tracking
            - Create backup and disaster recovery procedures
            - Define security and access controls for production
            - Create comprehensive deployment documentation
            - Estimate costs and resource requirements
            - Provide step-by-step deployment guide
            
            Project Details:
{input_vars}
            
            Base all deployment decisions on the actual implemented application.""",
            agent=agents['devops_engineer'],
            context=[architecture_task, development_task, testing_task],
            expected_output="Complete deployment guide with infrastructure setup, CI/CD pipeline configuration, and operational procedures"
        )
        
        return [requirements_task, architecture_task, development_task, testing_task, deployment_task]
    
    def create_simple_task(self, 
                          description: str, 
                          agent: Any, 
                          expected_output: str,
                          context: Optional[List[Task]] = None) -> Task:
        """Create a single task with specified parameters"""
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output,
            context=context or []
        )
    
    def add_context_to_task(self, task: Task, context_tasks: List[Task]) -> Task:
        """Add context dependencies to an existing task"""
        if not hasattr(task, 'context') or not task.context:
            task.context = context_tasks
        else:
            task.context.extend(context_tasks)
        return task