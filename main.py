#!/usr/bin/env python3
"""
CrewAI Development Team - Build software with AI agents
"""

import os
from dotenv import load_dotenv
from crew import build_app

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please copy .env.example to .env and add your OpenAI API key")
        return
    
    print("🎮 CrewAI Development Team - Pixel Snake Game Project")
    print("=" * 60)
    print("This AI crew will plan and build a modern Snake game!")
    print("The team includes:")
    print("👔 Product Manager - Requirements & scope")
    print("🏗️  Software Architect - System design")
    print("💻 Full Stack Developer - Implementation")
    print("🔍 QA Engineer - Testing & quality")
    print("🚀 DevOps Engineer - Deployment")
    print("=" * 60)
    
    # Predefined project details for Pixel Snake Game
    project_idea = "A modern browser-based Snake game with retro pixel art styling, smooth animations, score system, high scores saved to localStorage, multiple difficulty levels, responsive design that works on desktop and mobile, game over screen, and start screen with instructions"
    target_audience = "casual gamers who enjoy retro/nostalgic games, web users looking for quick entertainment during breaks, mobile users who want simple but engaging games"
    timeline = "3 weeks"
    
    print(f"\n🎮 Project: {project_idea}")
    print(f"👥 Target Audience: {target_audience}")
    print(f"⏰ Timeline: {timeline}")
    
    print(f"\n🚀 Starting development project...")
    
    try:
        result = build_app(project_idea, target_audience, timeline)
        
        print("\n" + "=" * 60)
        print("✅ Development planning completed!")
        print("=" * 60)
        print(result)
        
        # Save comprehensive output
        filename = "pixel_snake_game_development_plan.md"
        with open(filename, 'w') as f:
            f.write(f"# Development Plan: Pixel Snake Game\n\n")
            f.write(f"**Target Audience:** {target_audience}\n")
            f.write(f"**Timeline:** {timeline}\n\n")
            f.write("## Complete Development Plan\n\n")
            f.write(str(result))
        
        print(f"\n💾 Complete development plan saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API key and try again")

if __name__ == "__main__":
    main()