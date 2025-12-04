"""Debug Agent Execution Example

This example demonstrates comprehensive debugging techniques:
- Creating debug functions to analyze RunResult objects
- Monitoring token usage across multiple API calls
- Tracking guardrail activations and safety measures
- Understanding agent execution flow and performance

Essential for troubleshooting and optimizing agent behavior in development.

Usage:
    python 07_debug_agent.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunResult

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

def debug_agent_execution(result: RunResult):
    """Print detailed debugging information about agent execution."""
    print("=== AGENT EXECUTION DEBUG ===")
    print(f"Final output length: {len(result.final_output or '')}")
    print(f"Total API calls: {len(result.raw_responses)}")
    
    for i, response in enumerate(result.raw_responses):
        print(f"\nTurn {i+1}:")        
        print(f"  Tokens: {response.usage.total_tokens}")        
    
    if result.input_guardrail_results:
        print(f"\nInput guardrails triggered: {len(result.input_guardrail_results)}")
    
    if result.output_guardrail_results:
        print(f"Output guardrails triggered: {len(result.output_guardrail_results)}")

# Create an agent for testing
agent = Agent(
    name="DebugAgent",
    instructions="You are a helpful assistant for debugging purposes."
)

# Use the debugging function
result = Runner.run_sync(agent, "Complex query here...")
debug_agent_execution(result)
