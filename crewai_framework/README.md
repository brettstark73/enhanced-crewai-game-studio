# CrewAI Framework

A comprehensive framework for building reliable, debuggable CrewAI workflows. This framework prevents common CrewAI issues and provides better tooling for development teams.

## 🚀 Quick Start

```python
from crewai_framework import AgentFactory, TaskBuilder, validate_before_run, run_crew_with_debugging
from crewai import Crew, Process

# 1. Create agents with proper tools
factory = AgentFactory()
agents = factory.create_development_team()

# 2. Create tasks with proper dependencies
builder = TaskBuilder()
tasks = builder.create_development_workflow_tasks(
    agents=agents,
    inputs={'project_idea': 'A Snake game', 'target_audience': 'Gamers'}
)

# 3. Create and validate crew
crew = Crew(
    agents=list(agents.values()),
    tasks=tasks,
    process=Process.sequential,
    verbose=True
)

# 4. Validate before running
if validate_before_run(crew, {'project_idea': 'A Snake game', 'target_audience': 'Gamers'}):
    # 5. Run with debugging
    result = run_crew_with_debugging(crew, {
        'project_idea': 'A Snake game', 
        'target_audience': 'Gamers'
    })
```

## 🛡️ What This Framework Prevents

### Common CrewAI Issues Fixed:

1. **❌ Template Variable Errors**
   - **Problem**: `Template variable 'requirements' not found`
   - **Solution**: Validates all template variables before execution

2. **❌ Missing Context Between Tasks**  
   - **Problem**: Tasks don't receive previous outputs
   - **Solution**: Auto-adds context dependencies for sequential tasks

3. **❌ Agents Without Proper Tools**
   - **Problem**: Developer agents can't write files
   - **Solution**: Pre-configured agents with appropriate tools

4. **❌ Vague Task Outputs**
   - **Problem**: Agents produce plans instead of actual deliverables  
   - **Solution**: Specific expected outputs and validation

5. **❌ No Debugging/Visibility**
   - **Problem**: Can't see what each agent produced
   - **Solution**: Complete output capture and debugging tools

## 📋 Components

### 1. CrewAIValidator
Validates crew configuration before execution:
```python
from crewai_framework import CrewAIValidator

validator = CrewAIValidator()
result = validator.validate_crew(crew, inputs)
validator.print_validation_report(result)
```

### 2. AgentFactory  
Creates properly configured agents:
```python
from crewai_framework import AgentFactory

factory = AgentFactory()
developer = factory.create_full_stack_developer()  # Has FileWriterTool
architect = factory.create_software_architect()    # Has analysis tools
```

### 3. TaskBuilder
Creates tasks with proper dependencies:
```python
from crewai_framework import TaskBuilder

builder = TaskBuilder()
tasks = builder.create_development_workflow_tasks(agents, inputs)
# Automatically adds context=[previous_task] to sequential tasks
```

### 4. CrewDebugger
Captures and saves all outputs:
```python
from crewai_framework import run_crew_with_debugging

result = run_crew_with_debugging(crew, inputs, output_dir="my_output")
# Creates detailed logs and saves each task's output separately
```

## 🎯 Usage Patterns

### Pattern 1: Full Development Workflow
```python
# Complete development team for building applications
agents = factory.create_development_team()
tasks = builder.create_development_workflow_tasks(agents, inputs)
```

### Pattern 2: Custom Workflow
```python
# Build your own custom agents and tasks
custom_agent = factory.create_custom_agent(
    role="Security Specialist",
    goal="Ensure application security",
    backstory="...",
    tools=[FileReadTool()]
)

custom_task = builder.create_simple_task(
    description="Analyze security vulnerabilities...",
    agent=custom_agent,
    expected_output="Security assessment report"
)
```

### Pattern 3: Validation Only
```python
# Just validate an existing crew setup
if validate_before_run(existing_crew, inputs):
    result = existing_crew.kickoff(inputs=inputs)
```

## 📁 Output Management

The framework creates organized outputs:
```
crew_output/
├── complete_output.json          # Full execution data
├── complete_output.md           # Readable summary 
├── task_1_senior_product_manager.md
├── task_2_senior_software_architect.md
├── task_3_senior_full_stack_developer.md
├── task_4_senior_qa_engineer.md
└── task_5_senior_devops_engineer.md
```

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL_NAME=gpt-4  # Optional, defaults to gpt-4
```

### Agent Customization
```python
# Custom LLM settings
factory = AgentFactory(model_name="gpt-3.5-turbo", temperature=0.1)

# Custom tools
from crewai_tools import CustomTool
developer = factory.create_full_stack_developer(tools=[CustomTool()])
```

### Memory Configuration
```python
# For production use - enable memory
crew = Crew(agents=agents, tasks=tasks, memory=True)

# For development/testing - disable memory to avoid ChromaDB issues
crew = Crew(agents=agents, tasks=tasks, memory=False)
```

### Timeout Handling
```python
# For long-running tasks, consider breaking into smaller tasks
# or running with patience for complex implementations
import time
start_time = time.time()
result = crew.kickoff(inputs=inputs)
print(f"Completed in {time.time() - start_time:.1f} seconds")
```

## 🚨 Validation Checks

The validator checks for:
- ✅ Template variables match inputs
- ✅ Task context dependencies
- ✅ Agent capabilities vs task requirements  
- ✅ Expected output specificity
- ✅ Process configuration issues

## 🎮 Example: Snake Game Project

See `improved_crew.py` for a complete example that builds an actual Snake game using this framework.

## 📈 Benefits

- **🛡️ Prevents Common Errors**: Catches issues before execution
- **🔍 Full Visibility**: See exactly what each agent produces
- **📁 Organized Outputs**: Structured output management  
- **🔧 Better Tools**: Agents have appropriate capabilities
- **📋 Reusable Patterns**: Standard workflows for common tasks
- **🚀 Faster Development**: Less debugging, more building

## ⚠️ Known Issues & Workarounds

### ChromaDB Memory Issues
**Problem**: `KeyError: '_type'` when initializing crew with `memory=True`
**Workaround**: Use `memory=False` for development. For production, ensure ChromaDB is properly configured.

### Long Execution Times
**Problem**: Complex tasks can take 5-10 minutes or timeout
**Solution**: 
- Break large tasks into smaller subtasks
- Use simpler language models (gpt-3.5-turbo) for faster execution
- Monitor progress in `crew_output/` directory

### Incomplete File Generation
**Problem**: Agents sometimes create skeleton files instead of complete implementations
**Solution**: 
- Use more specific `expected_output` descriptions
- Add validation steps to check file completeness
- Consider manual completion for critical files

## 🤝 Contributing

This framework is designed to be extended. Add new agent types, validation rules, or output formats as needed for your projects.