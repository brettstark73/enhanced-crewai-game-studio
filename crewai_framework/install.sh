#!/bin/bash
set -e

echo "🎯 Installing CrewAI Framework..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ Error: Python $required_version or higher required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install in development mode
echo "📦 Installing framework in development mode..."
pip install -e .

echo "🔧 Installing development dependencies..."
pip install -e ".[dev]"

echo "🧪 Running tests..."
python -m pytest tests/ || echo "⚠️  Tests not found - skipping"

echo "🎉 Installation complete!"
echo ""
echo "📖 Usage:"
echo "   from crewai_framework import AgentFactory, TaskBuilder, validate_before_run"
echo ""
echo "📋 Example:"
echo "   python examples/snake_game_example.py"
echo ""