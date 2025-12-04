"""No Memory Agent Example

This example demonstrates the default stateless behavior of agents:
- Each Runner.run_sync() call is independent
- Agents don't remember previous conversations by default
- Shows the need for explicit memory management
- Illustrates the baseline behavior before adding memory features

Important for understanding when and why to implement memory patterns.

Usage:
    python 08_no_memory.py
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

agent = Agent(name="Conversationalist", instructions="You are helpful.")

# First interaction
result1 = Runner.run_sync(agent, "My name is Alice.")
print(result1.final_output) 

# Second interaction - agent does not remember the name
result2 = Runner.run_sync(agent, "What's my name?")
print(result2.final_output)
