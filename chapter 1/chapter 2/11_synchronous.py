"""Synchronous Agent Execution Example

This example demonstrates blocking, synchronous agent execution:
- Using Runner.run_sync() for simple, blocking execution
- When to use synchronous vs asynchronous execution patterns
- Simpler code flow for scripts and batch processing
- Understanding the trade-offs between sync and async approaches

Basic pattern for simple scripts and non-concurrent applications.

Usage:
    python 11_synchronous.py
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

# Synchronous execution example
agent = Agent(name="Analyst", instructions="Provide concise analysis.")

# This blocks until complete
result = Runner.run_sync(agent, "Analyze the benefits of renewable energy.")
print(result.final_output)
