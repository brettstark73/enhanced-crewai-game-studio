#!/usr/bin/env python3
"""
Improved CrewAI Setup using the CrewAI Framework
This version should actually build the Snake game properly
"""

import os
from dotenv import load_dotenv
from crewai import Crew, Process

# Import our new framework
from crewai_framework import (
    AgentFactory, 
    TaskBuilder, 
    validate_before_run, 
    run_crew_with_debugging
)

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your OpenAI API key")
        return
    
    print("🎮 Improved CrewAI Development Team - Pixel Snake Game Project")
    print("=" * 70)
    print("Using CrewAI Framework for reliable execution!")
    print("=" * 70)
    
    # Project configuration
    project_inputs = {
        'project_idea': "A modern browser-based Snake game with retro pixel art styling, smooth animations, score system, high scores saved to localStorage, multiple difficulty levels, responsive design that works on desktop and mobile, game over screen, and start screen with instructions",
        'target_audience': "casual gamers who enjoy retro/nostalgic games, web users looking for quick entertainment during breaks, mobile users who want simple but engaging games",
        'timeline': "1 day for implementation"
    }
    
    print(f"🎮 Project: {project_inputs['project_idea']}")
    print(f"👥 Target Audience: {project_inputs['target_audience']}")
    print(f"⏰ Timeline: {project_inputs['timeline']}")
    print()
    
    # 1. Create agents using the factory
    print("🏭 Creating development team with proper tools...")
    factory = AgentFactory()
    agents = factory.create_development_team()
    
    # 2. Create tasks with proper dependencies
    print("📋 Creating tasks with proper context dependencies...")
    builder = TaskBuilder()
    tasks = builder.create_development_workflow_tasks(agents, project_inputs)
    
    # 3. Create crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=False  # Disabled due to ChromaDB issues
    )
    
    # 4. Validate crew configuration
    print("🔍 Validating crew configuration...")
    if not validate_before_run(crew, project_inputs):
        print("❌ Validation failed. Please fix issues before proceeding.")
        return
    
    print("✅ Validation passed! Starting execution...")
    print()
    
    # 5. Run crew with debugging
    try:
        print("🚀 Starting improved development project...")
        result = run_crew_with_debugging(
            crew=crew, 
            inputs=project_inputs,
            output_dir="improved_crew_output"
        )
        
        print("\n" + "=" * 70)
        print("✅ IMPROVED DEVELOPMENT COMPLETED!")
        print("=" * 70)
        print("📁 Check improved_crew_output/ for detailed outputs from each agent")
        print("📄 Check for actual game files that should have been created!")
        print("=" * 70)
        
        # Check if files were actually created
        game_files = ['index.html', 'style.css', 'script.js']
        created_files = [f for f in game_files if os.path.exists(f)]
        
        if created_files:
            print(f"🎉 SUCCESS: Found created game files: {created_files}")
            if len(created_files) == len(game_files):
                print("🎮 Complete game should be ready to play!")
        else:
            print("⚠️  WARNING: No game files found in current directory")
            print("   Check improved_crew_output/ to see what was actually produced")
        
    except Exception as e:
        print(f"❌ Error during improved crew execution: {e}")
        print("Check improved_crew_output/ for partial results")
        import traceback
        traceback.print_exc()

def test_framework():
    """Test the framework components independently"""
    print("🧪 Testing CrewAI Framework Components...")
    
    # Test agent factory
    factory = AgentFactory()
    agents = factory.create_development_team()
    print(f"✅ Created {len(agents)} agents with tools")
    
    # Test task builder  
    builder = TaskBuilder()
    test_inputs = {'project_idea': 'test', 'target_audience': 'test', 'timeline': 'test'}
    tasks = builder.create_development_workflow_tasks(agents, test_inputs)
    print(f"✅ Created {len(tasks)} interconnected tasks")
    
    # Test validation
    from crewai_framework import CrewAIValidator
    validator = CrewAIValidator()
    crew = Crew(agents=list(agents.values()), tasks=tasks, process=Process.sequential)
    result = validator.validate_crew(crew, test_inputs)
    print(f"✅ Validation found {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    
    print("🎉 Framework components working correctly!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_framework()
    else:
        main()