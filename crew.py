from crewai import Crew, Process
from agents import product_manager, software_architect, full_stack_developer, qa_engineer, devops_engineer
from tasks import requirements_task, architecture_task, development_task, testing_task, deployment_task

# Create the development crew
dev_team_crew = Crew(
    agents=[product_manager, software_architect, full_stack_developer, qa_engineer, devops_engineer],
    tasks=[requirements_task, architecture_task, development_task, testing_task, deployment_task],
    process=Process.sequential,  # Tasks executed in order: Requirements → Architecture → Development → Testing → Deployment
    verbose=True,  # Detailed logging
    memory=True,  # Enable memory for better context sharing between agents
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    }
)

def build_app(project_idea, target_audience="general users", timeline="8 weeks"):
    """
    Execute the development crew to build a complete application
    
    Args:
        project_idea (str): Description of the app/software to build
        target_audience (str): Who will use this application
        timeline (str): Expected development timeline
        
    Returns:
        str: Complete development plan and deliverables
    """
    print(f"🚀 Starting development project: {project_idea}")
    print(f"👥 Target audience: {target_audience}")
    print(f"⏰ Timeline: {timeline}")
    print("=" * 60)
    print("🏗️  Development Team Assembling...")
    print("👔 Product Manager: Defining requirements")
    print("🏗️  Software Architect: Designing system")
    print("💻 Full Stack Developer: Building application")
    print("🔍 QA Engineer: Testing and validation")
    print("🚀 DevOps Engineer: Deployment strategy")
    print("=" * 60)
    
    inputs = {
        'project_idea': project_idea,
        'target_audience': target_audience,
        'timeline': timeline
    }
    
    result = dev_team_crew.kickoff(inputs=inputs)
    return result