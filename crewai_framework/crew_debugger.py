"""
CrewAI Debugger and Output Manager
Provides debugging capabilities and better output handling for CrewAI workflows
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from crewai import Crew, Task

class CrewDebugger:
    """Debugging and output management for CrewAI crews"""
    
    def __init__(self, output_dir: str = "crew_output"):
        self.output_dir = output_dir
        self.task_outputs = {}
        self.execution_log = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def setup_crew_logging(self, crew: Crew) -> Crew:
        """Setup logging for crew execution"""
        # Store original tasks for later reference
        self.original_tasks = crew.tasks.copy()
        
        return crew
    
    def log_task_start(self, task: Task, task_index: int):
        """Log when a task starts"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'task_start',
            'task_index': task_index,
            'agent_role': task.agent.role,
            'task_description': task.description[:200] + "..." if len(task.description) > 200 else task.description
        }
        self.execution_log.append(log_entry)
        print(f"🚀 Starting Task {task_index + 1}: {task.agent.role}")
    
    def log_task_completion(self, task: Task, task_index: int, output: Any):
        """Log when a task completes"""
        # Store task output
        task_key = f"task_{task_index + 1}_{task.agent.role.lower().replace(' ', '_')}"
        self.task_outputs[task_key] = {
            'agent_role': task.agent.role,
            'output': str(output),
            'timestamp': datetime.now().isoformat()
        }
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'task_completion',
            'task_index': task_index,
            'agent_role': task.agent.role,
            'output_length': len(str(output))
        }
        self.execution_log.append(log_entry)
        print(f"✅ Completed Task {task_index + 1}: {task.agent.role}")
        
        # Save individual task output
        self._save_task_output(task_index, task.agent.role, output)
    
    def _save_task_output(self, task_index: int, agent_role: str, output: Any):
        """Save individual task output to file"""
        filename = f"task_{task_index + 1}_{agent_role.lower().replace(' ', '_')}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        content = f"# Task {task_index + 1}: {agent_role}\n\n"
        content += f"**Timestamp:** {datetime.now().isoformat()}\n\n"
        content += f"## Output\n\n{output}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def save_complete_output(self, final_result: Any):
        """Save complete crew execution output"""
        # Save all task outputs
        all_outputs = {
            'execution_summary': {
                'total_tasks': len(self.task_outputs),
                'execution_time': datetime.now().isoformat(),
                'final_result': str(final_result)
            },
            'task_outputs': self.task_outputs,
            'execution_log': self.execution_log
        }
        
        # Save as JSON
        json_file = os.path.join(self.output_dir, 'complete_output.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_outputs, f, indent=2, ensure_ascii=False)
        
        # Save as readable markdown
        md_file = os.path.join(self.output_dir, 'complete_output.md')
        self._save_markdown_report(md_file, all_outputs, final_result)
        
        print(f"📁 All outputs saved to {self.output_dir}/")
        return all_outputs
    
    def _save_markdown_report(self, filepath: str, all_outputs: Dict, final_result: Any):
        """Save a comprehensive markdown report"""
        content = "# CrewAI Execution Report\n\n"
        content += f"**Execution Time:** {datetime.now().isoformat()}\n"
        content += f"**Total Tasks:** {len(self.task_outputs)}\n\n"
        
        # Add each task output
        for task_key, task_data in all_outputs['task_outputs'].items():
            content += f"## {task_data['agent_role']}\n\n"
            content += f"**Timestamp:** {task_data['timestamp']}\n\n"
            content += f"### Output\n\n{task_data['output']}\n\n"
            content += "---\n\n"
        
        # Add final result
        content += "## Final Result\n\n"
        content += f"{final_result}\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_task_output(self, task_index: int = None, agent_role: str = None) -> Optional[str]:
        """Get output from a specific task"""
        if agent_role:
            task_key = f"task_{task_index + 1}_{agent_role.lower().replace(' ', '_')}"
        else:
            # Find by index
            task_keys = list(self.task_outputs.keys())
            if task_index < len(task_keys):
                task_key = task_keys[task_index]
            else:
                return None
        
        return self.task_outputs.get(task_key, {}).get('output')
    
    def print_execution_summary(self):
        """Print a summary of the execution"""
        print("\n" + "="*60)
        print("🔍 EXECUTION SUMMARY")
        print("="*60)
        
        for i, (task_key, task_data) in enumerate(self.task_outputs.items()):
            print(f"{i+1}. {task_data['agent_role']}")
            print(f"   Output length: {len(task_data['output'])} characters")
            print(f"   Timestamp: {task_data['timestamp']}")
        
        print(f"\n📁 Detailed outputs saved in: {self.output_dir}/")
        print("="*60)


def run_crew_with_debugging(crew: Crew, inputs: Dict[str, Any], output_dir: str = "crew_output") -> Dict[str, Any]:
    """
    Run a crew with full debugging and output management
    
    Returns:
        Dict with 'result', 'task_outputs', and 'debug_info'
    """
    debugger = CrewDebugger(output_dir)
    
    print("🎬 Starting CrewAI execution with debugging...")
    
    try:
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        # Save all outputs (this is a simplified version - in practice you'd need
        # to hook into CrewAI's execution process to capture individual task outputs)
        debug_info = debugger.save_complete_output(result)
        debugger.print_execution_summary()
        
        return {
            'result': result,
            'task_outputs': debugger.task_outputs,
            'debug_info': debug_info
        }
        
    except Exception as e:
        print(f"❌ Error during crew execution: {e}")
        # Still try to save what we have
        debugger.save_complete_output(f"ERROR: {e}")
        raise