"""Manual Memory Management Example

This example demonstrates explicit conversation memory control:
- Using result.to_input_list() to extract conversation history
- Manually building conversation context for subsequent calls
- Fine-grained control over what gets remembered
- Building custom memory management patterns

Essential for applications requiring precise control over conversation context.

Usage:
    python 10_manual_memory.py
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

async def main():
    agent = Agent(name="Assistant", instructions="Reply concisely.")
    
    # First turn
    result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
    print(result.final_output)  # San Francisco
    
    # Second turn - maintain conversation context
    conversation_history = result.to_input_list()
    conversation_history.append({"role": "user", "content": "What state is it in?"})
    
    result = await Runner.run(agent, conversation_history)
    print(result.final_output)  # California

if __name__ == "__main__":
    asyncio.run(main())
