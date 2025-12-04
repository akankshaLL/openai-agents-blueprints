"""Combined Memory and Context Example

This example demonstrates combining conversation memory with application context:
- Using both conversation history (manual memory) and application context
- Managing session data alongside conversation state
- Building agents that maintain both dialogue context and user context
- Practical pattern for production conversational applications

Shows how to combine multiple memory patterns for comprehensive state management.

Usage:
    python 13_combined_memory_context.py
"""

import os
import asyncio
from dataclasses import dataclass
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

@dataclass
class AppContext:
    user_id: str
    session_id: str

async def chat_with_memory():
    context = AppContext(user_id="123", session_id="session_456")
    agent = Agent[AppContext](name="Assistant", instructions="Be helpful.")
    
    # Start conversation
    result = await Runner.run(agent, "Hi, I'm building a website", context=context)
    
    # Continue with memory
    history = result.to_input_list()
    history.append({"role": "user", "content": "What technologies should I use?"})
    result = await Runner.run(agent, history, context=context)
    
    return result

async def main():
    result = await chat_with_memory()
    print("Final response:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
