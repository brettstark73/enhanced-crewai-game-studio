from crewai import Task
from agents import product_manager, software_architect, full_stack_developer, qa_engineer, devops_engineer

# Product Requirements Task
requirements_task = Task(
    description="""Analyze the project idea and create comprehensive product requirements:
    - Define the core problem being solved
    - Identify target users and their needs
    - Create user stories and acceptance criteria
    - Define MVP features vs future enhancements
    - Specify functional and non-functional requirements
    - Consider scalability and performance requirements
    - Define success metrics
    
    Project idea: {project_idea}
    Target audience: {target_audience}
    Timeline: {timeline}""",
    agent=product_manager,
    expected_output="Detailed product requirements document with user stories, features, and acceptance criteria"
)

# Architecture Design Task
architecture_task = Task(
    description="""Based on the product requirements, design the system architecture:
    - Choose appropriate technology stack
    - Design system architecture and components
    - Define database schema and data models
    - Plan API design and endpoints
    - Consider security requirements
    - Plan for scalability and performance
    - Create technical specifications
    - Define development environment setup
    
    Requirements: {requirements}""",
    agent=software_architect,
    expected_output="Comprehensive technical architecture document with technology choices, system design, and specifications"
)

# Development Task
development_task = Task(
    description="""Implement the application based on architecture and requirements:
    - Set up project structure and development environment
    - Implement core features according to requirements
    - Create database models and migrations
    - Build API endpoints and business logic
    - Implement frontend components and user interface
    - Add proper error handling and validation
    - Write unit tests for critical functionality
    - Follow coding best practices and standards
    - Create comprehensive documentation
    
    Architecture: {architecture}
    Requirements: {requirements}""",
    agent=full_stack_developer,
    expected_output="Complete application code with proper structure, documentation, and basic tests"
)

# Testing Task
testing_task = Task(
    description="""Create comprehensive testing strategy and test cases:
    - Review code quality and adherence to requirements
    - Create detailed test plan covering all features
    - Design unit tests for all components
    - Plan integration tests for API endpoints
    - Create end-to-end test scenarios
    - Plan performance and load testing
    - Define security testing approach
    - Create user acceptance test cases
    - Document bug reporting and tracking process
    
    Application code: {application_code}
    Requirements: {requirements}""",
    agent=qa_engineer,
    expected_output="Complete testing strategy with test plans, test cases, and quality assurance guidelines"
)

# Deployment Task
deployment_task = Task(
    description="""Design deployment strategy and infrastructure:
    - Choose appropriate hosting platform
    - Design CI/CD pipeline
    - Create deployment scripts and configuration
    - Plan database deployment and migrations
    - Configure monitoring and logging
    - Plan backup and disaster recovery
    - Define security and access controls
    - Create deployment documentation
    - Plan scaling strategy
    - Estimate costs and resource requirements
    
    Application: {application_code}
    Architecture: {architecture}""",
    agent=devops_engineer,
    expected_output="Complete deployment guide with infrastructure setup, CI/CD pipeline, and operational procedures"
)