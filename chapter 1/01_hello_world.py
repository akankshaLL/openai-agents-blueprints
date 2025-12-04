"""Hello World Agent Example

This is the simplest possible OpenAI Agents SDK example demonstrating:
- Basic agent creation with minimal configuration
- Synchronous agent execution using Runner.run_sync()
- Accessing the final output from agent responses
- Environment setup and API key validation

Perfect starting point for understanding the core Agent → Runner → Result pattern.

Usage:
    python 01_hello_world.py
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

# Step 1: Create an agent blueprint
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant",    
)

# Step 2: Execute the agent with a prompt
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")

# Step 3: Access the result
print(result.final_output)

# Expected output:
# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
