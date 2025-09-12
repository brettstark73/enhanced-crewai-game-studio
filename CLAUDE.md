# Claude Code Configuration

This file contains project context and commands for Claude Code.

## Project Overview
CrewAI-powered development project to create a pixel-style Snake game. Uses AI agents (Product Manager, Software Architect, Full Stack Developer, QA Engineer, DevOps Engineer) to plan and design the game.

## Key Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt
pip install crewai-tools  # For file writing capabilities

# Setup environment
cp .env.example .env
# Then edit .env to add OPENAI_API_KEY

# Run the ORIGINAL AI development team (has issues)
python main.py

# Run the IMPROVED AI development team (uses framework)
python improved_crew.py

# Test the CrewAI framework
python improved_crew.py test
```

### Development Commands
```bash
# Run the original CrewAI workflow (produces only deployment plans)
python main.py

# Run the improved CrewAI workflow (should build actual game)
python improved_crew.py

# Check Python syntax/style (if you add linting tools)
python -m py_compile *.py
```

## Project Structure
- `main.py` - Entry point for CrewAI workflow
- `agents.py` - AI agent definitions (Product Manager, Architect, Developer, QA, DevOps)
- `tasks.py` - Task definitions for each agent
- `crew.py` - CrewAI crew configuration and orchestration
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template

## Environment Variables
- `OPENAI_API_KEY` - Required for AI agent functionality
- `OPENAI_MODEL_NAME` - Model to use (default: gpt-4)

## Notes
This is a CrewAI project focused on AI-driven development planning rather than direct game implementation. The output will be comprehensive plans, specifications, and architectural designs for building the Snake game.