"""Asynchronous Agent Execution Example

This example demonstrates concurrent agent processing:
- Using asyncio.gather() to run multiple agents simultaneously
- Significant performance improvements for parallel workloads
- Proper async/await patterns for agent execution
- Handling multiple queries efficiently with concurrent processing

Essential pattern for building high-performance agent applications.

Usage:
    python 12_asynchronous.py
"""

import os
import asyncio
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

async def handle_multiple_queries():
    agent = Agent(name="Assistant", instructions="Provide helpful responses.")
    
    # Process multiple queries concurrently
    queries = [
        "What is machine learning?",
        "Explain quantum computing",
        "Define artificial intelligence"
    ]
    
    # Start all queries simultaneously
    tasks = [Runner.run(agent, query) for query in queries]
    
    # Wait for all to complete
    results = await asyncio.gather(*tasks)
    
    for query, result in zip(queries, results):
        print(f"Q: {query}")
        print(f"A: {result.final_output}\n")

# Run the async function
asyncio.run(handle_multiple_queries())
