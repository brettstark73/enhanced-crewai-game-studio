#!/usr/bin/env python3
"""
Chunked CrewAI Runner - Handles large requests by breaking them into smaller chunks
Prevents TPM (tokens per minute) rate limit errors
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any
from crewai import Crew, Agent, Task

class ChunkedCrewRunner:
    """Runs CrewAI tasks in chunks to avoid rate limits"""

    def __init__(self, max_tokens_per_chunk=180000, delay_between_chunks=65):
        # OpenAI TPM limit: 200K tokens per minute for gpt-4o-mini
        # Daily limit: 2.5M tokens for mini models
        self.max_tokens_per_chunk = max_tokens_per_chunk  # Just under 200K TPM limit
        self.delay_between_chunks = delay_between_chunks   # Wait > 1 minute for TPM reset

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 chars)"""
        return len(text) // 4

    def create_chunked_tasks(self, project_idea: str) -> List[Dict]:
        """Break game development into smaller, manageable tasks"""

        base_context = f"Creating a {project_idea} game."

        chunks = [
            {
                "name": "game_structure",
                "description": f"{base_context} Create the basic HTML structure and canvas setup. Include DOCTYPE, html, head, body, and canvas element. Keep it minimal - no game logic yet.",
                "expected_output": "HTML file with basic game structure (under 500 lines)"
            },
            {
                "name": "game_mechanics",
                "description": f"{base_context} Create the core game mechanics and logic. Include player movement, enemy behavior, collision detection, and scoring. Use JavaScript classes and functions.",
                "expected_output": "JavaScript code for game mechanics (under 800 lines)"
            },
            {
                "name": "visual_styling",
                "description": f"{base_context} Create CSS styling and visual enhancements. Include responsive design, colors, fonts, animations, and mobile support.",
                "expected_output": "CSS file with complete styling (under 400 lines)"
            },
            {
                "name": "integration",
                "description": f"{base_context} Integrate all components into a single working HTML file. Combine HTML structure, JavaScript logic, and CSS styling into one playable game file.",
                "expected_output": "Complete working game as single HTML file"
            }
        ]

        return chunks

    def run_chunked_crew(self, crew: Crew, project_idea: str, **kwargs) -> Dict:
        """Run crew tasks in chunks to avoid rate limits"""

        print("🔧 CHUNKED CREW EXECUTION")
        print("=" * 50)
        print(f"📊 Max tokens per chunk: {self.max_tokens_per_chunk:,}")
        print(f"⏱️  Delay between chunks: {self.delay_between_chunks}s")
        print()

        chunks = self.create_chunked_tasks(project_idea)
        results = {}

        for i, chunk in enumerate(chunks, 1):
            print(f"🎯 CHUNK {i}/{len(chunks)}: {chunk['name']}")
            print(f"📝 Task: {chunk['description'][:100]}...")

            # Estimate if this chunk might be too large
            estimated_tokens = self.estimate_tokens(chunk['description'])
            print(f"📊 Estimated tokens: {estimated_tokens:,}")

            if estimated_tokens > self.max_tokens_per_chunk:
                print("⚠️ Chunk may be too large, but proceeding...")

            try:
                # Create a simplified task for this chunk
                chunk_task = Task(
                    description=chunk['description'],
                    expected_output=chunk['expected_output'],
                    agent=crew.agents[0]  # Use first agent
                )

                # Execute just this chunk
                start_time = time.time()
                result = chunk_task.execute_sync()
                execution_time = time.time() - start_time

                results[chunk['name']] = {
                    'result': result,
                    'execution_time': execution_time,
                    'estimated_tokens': estimated_tokens,
                    'timestamp': datetime.now().isoformat()
                }

                print(f"✅ Completed in {execution_time:.1f}s")

                # Wait between chunks (except for last one)
                if i < len(chunks):
                    print(f"⏳ Waiting {self.delay_between_chunks}s before next chunk...")
                    time.sleep(self.delay_between_chunks)

            except Exception as e:
                error_msg = str(e)
                print(f"❌ Chunk failed: {error_msg}")

                if "RateLimitError" in error_msg:
                    print("🔄 Rate limit detected - increasing delay...")
                    extra_delay = 120  # Extra 2 minutes
                    print(f"⏳ Waiting additional {extra_delay}s...")
                    time.sleep(extra_delay)

                    # Retry this chunk once
                    try:
                        print(f"🔄 Retrying chunk {i}...")
                        result = chunk_task.execute_sync()
                        results[chunk['name']] = {
                            'result': result,
                            'retry': True,
                            'timestamp': datetime.now().isoformat()
                        }
                        print("✅ Retry successful!")
                    except Exception as retry_error:
                        results[chunk['name']] = {
                            'error': str(retry_error),
                            'failed_after_retry': True,
                            'timestamp': datetime.now().isoformat()
                        }
                        print(f"❌ Retry also failed: {retry_error}")
                else:
                    results[chunk['name']] = {
                        'error': error_msg,
                        'timestamp': datetime.now().isoformat()
                    }

            print()

        # Combine results if all successful
        if all('error' not in result for result in results.values()):
            print("🎉 All chunks completed successfully!")
            combined_result = self.combine_chunk_results(results)
            results['combined'] = combined_result
        else:
            print("⚠️ Some chunks failed - check individual results")

        return results

    def combine_chunk_results(self, chunk_results: Dict) -> str:
        """Combine individual chunk results into final output"""

        combined = []
        combined.append("# Complete Game Development Output")
        combined.append(f"Generated: {datetime.now().isoformat()}")
        combined.append("")

        for chunk_name, chunk_data in chunk_results.items():
            if chunk_name == 'combined':
                continue

            combined.append(f"## {chunk_name.replace('_', ' ').title()}")

            if 'error' in chunk_data:
                combined.append(f"**Error:** {chunk_data['error']}")
            else:
                result = chunk_data.get('result', '')
                if hasattr(result, 'raw'):
                    combined.append(str(result.raw))
                else:
                    combined.append(str(result))

            combined.append("")

        return "\n".join(combined)

def run_space_invaders_chunked():
    """Run space invaders generation with chunking"""

    from crew import dev_team_crew  # Import your existing crew

    runner = ChunkedCrewRunner(
        max_tokens_per_chunk=180000,  # Just under 200K TPM limit
        delay_between_chunks=65       # Just over 1 minute for TPM reset
    )

    project_idea = "space invaders arcade game with HTML5 canvas"

    print("🚀 Starting chunked space invaders generation...")
    results = runner.run_chunked_crew(dev_team_crew, project_idea)

    # Save results
    output_file = f"games/space-invaders-chunked/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"💾 Results saved to: {output_file}")

    if 'combined' in results:
        combined_file = output_file.replace('.json', '_combined.md')
        with open(combined_file, 'w') as f:
            f.write(results['combined'])
        print(f"📄 Combined output: {combined_file}")

    return results

if __name__ == "__main__":
    run_space_invaders_chunked()