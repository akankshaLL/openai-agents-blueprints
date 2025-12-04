"""Core Result Inspection Example

This example demonstrates how to inspect RunResult objects for monitoring:
- Accessing final_output for the main response
- Examining execution metadata (agent info, turn count)
- Monitoring API usage and token consumption
- Understanding the structure of agent responses

Critical for debugging, monitoring, and optimizing agent performance.

Usage:
    python 06_core_result.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

agent = Agent(name="Analyzer", instructions="Analyze the given input.")
result = Runner.run_sync(agent, "What are the benefits of renewable energy?")

# Primary output
print(f"Final response: {result.final_output}")

# Execution metadata
print(f"Executing agent: {result.last_agent.name}")
print(f"Total turns: {len(result.raw_responses)}")
print(f"New items generated: {len(result.new_items)}")

# API usage information
if result.raw_responses:
    for i, response in enumerate(result.raw_responses):
        usage = response.usage
        print(f"Turn {i+1}: {usage.total_tokens} tokens")
