"""
CrewAI Agent Factory
Creates properly configured agents with appropriate tools and capabilities
"""

from crewai import Agent
from crewai_tools import (
    FileWriterTool, 
    FileReadTool, 
    DirectoryReadTool, 
    DirectorySearchTool,
    CodeDocsSearchTool,
    WebsiteSearchTool
)
from langchain_openai import ChatOpenAI
import os
from typing import List, Optional

class AgentFactory:
    """Factory for creating properly configured CrewAI agents"""
    
    def __init__(self, model_name: str = None, temperature: float = 0.3):
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
            temperature=temperature
        )
    
    def create_product_manager(self, tools: Optional[List] = None) -> Agent:
        """Create a Product Manager agent with research capabilities"""
        default_tools = [
            FileReadTool(),
            DirectoryReadTool(),
            WebsiteSearchTool() if 'WebsiteSearchTool' in globals() else None
        ]
        agent_tools = [tool for tool in (tools or default_tools) if tool is not None]
        
        return Agent(
            role='Senior Product Manager',
            goal='Define clear requirements, manage scope, and ensure the product meets user needs',
            backstory="""You are an experienced product manager with 10+ years building successful 
            software products. You excel at understanding user needs, defining clear requirements, 
            breaking down complex projects into manageable features, and making strategic decisions 
            about what to build and when. You always think about user experience and business value.""",
            verbose=True,
            allow_delegation=False,
            tools=agent_tools,
            llm=self.llm
        )
    
    def create_software_architect(self, tools: Optional[List] = None) -> Agent:
        """Create a Software Architect agent with analysis capabilities"""
        default_tools = [
            FileReadTool(),
            DirectoryReadTool(),
            DirectorySearchTool(),
            CodeDocsSearchTool() if 'CodeDocsSearchTool' in globals() else None
        ]
        agent_tools = [tool for tool in (tools or default_tools) if tool is not None]
        
        return Agent(
            role='Senior Software Architect',
            goal='Design scalable, maintainable system architecture and technical specifications',
            backstory="""You are a senior software architect with deep experience in system design, 
            architecture patterns, and technology selection. You excel at designing systems that are 
            scalable, maintainable, and secure. You consider performance, scalability, maintainability, 
            and cost when making architectural decisions. You create clear technical specifications.""",
            verbose=True,
            allow_delegation=False,
            tools=agent_tools,
            llm=self.llm
        )
    
    def create_full_stack_developer(self, tools: Optional[List] = None) -> Agent:
        """Create a Full Stack Developer agent with file creation capabilities"""
        default_tools = [
            FileWriterTool(),
            FileReadTool(),
            DirectoryReadTool(),
            DirectorySearchTool()
        ]
        agent_tools = tools or default_tools
        
        return Agent(
            role='Senior Full Stack Developer',
            goal='Implement high-quality, well-tested code following best practices and CREATE ACTUAL FILES',
            backstory="""You are a senior full-stack developer with expertise in modern web technologies, 
            mobile development, and best practices. You write clean, efficient, well-documented code 
            and follow industry standards. You excel at both frontend and backend development, 
            understand DevOps practices, and always consider security and performance.
            
            IMPORTANT: You MUST create actual files when implementing. Use FileWriterTool to create 
            HTML, CSS, JavaScript, and other code files. Don't just describe what should be built - 
            actually build it by writing the files.""",
            verbose=True,
            allow_delegation=False,
            tools=agent_tools,
            llm=self.llm
        )
    
    def create_qa_engineer(self, tools: Optional[List] = None) -> Agent:
        """Create a QA Engineer agent with testing capabilities"""
        default_tools = [
            FileReadTool(),
            DirectoryReadTool(),
            FileWriterTool()  # For creating test files
        ]
        agent_tools = tools or default_tools
        
        return Agent(
            role='Senior QA Engineer',
            goal='Ensure quality through comprehensive testing and validation strategies',
            backstory="""You are a senior QA engineer with expertise in test strategy, automation, 
            and quality assurance. You understand different testing methodologies, create comprehensive 
            test plans, and ensure applications meet quality standards. You think about edge cases, 
            performance testing, security testing, and user acceptance criteria.""",
            verbose=True,
            allow_delegation=False,
            tools=agent_tools,
            llm=self.llm
        )
    
    def create_devops_engineer(self, tools: Optional[List] = None) -> Agent:
        """Create a DevOps Engineer agent with infrastructure capabilities"""
        default_tools = [
            FileWriterTool(),  # For creating deployment scripts
            FileReadTool(),
            DirectoryReadTool()
        ]
        agent_tools = tools or default_tools
        
        return Agent(
            role='Senior DevOps Engineer',
            goal='Design deployment strategy, CI/CD pipelines, and infrastructure requirements',
            backstory="""You are a senior DevOps engineer with expertise in cloud infrastructure, 
            containerization, CI/CD pipelines, and monitoring. You ensure applications are deployable, 
            scalable, and maintainable in production. You understand security best practices, 
            infrastructure as code, and modern deployment strategies.""",
            verbose=True,
            allow_delegation=False,
            tools=agent_tools,
            llm=self.llm
        )
    
    def create_development_team(self) -> dict:
        """Create a complete development team with all standard roles"""
        return {
            'product_manager': self.create_product_manager(),
            'software_architect': self.create_software_architect(),
            'full_stack_developer': self.create_full_stack_developer(),
            'qa_engineer': self.create_qa_engineer(),
            'devops_engineer': self.create_devops_engineer()
        }
    
    def create_custom_agent(self, 
                          role: str, 
                          goal: str, 
                          backstory: str, 
                          tools: Optional[List] = None,
                          **kwargs) -> Agent:
        """Create a custom agent with specified configuration"""
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=kwargs.get('verbose', True),
            allow_delegation=kwargs.get('allow_delegation', False),
            llm=self.llm
        )