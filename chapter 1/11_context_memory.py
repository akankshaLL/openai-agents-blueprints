"""Context Memory Agent Example

This example demonstrates context-aware agents with custom data:
- Using RunContextWrapper to pass application context to tools
- Creating typed context objects with dataclasses
- Building tools that access user preferences and session data
- Separating conversation memory from application context

Perfect for agents that need access to user profiles, preferences, or application state.

Usage:
    python 11_context_memory.py
"""

import os
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv
from agents import Agent, RunContextWrapper, Runner, function_tool

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

@dataclass
class UserContext:
    user_id: str
    username: str
    preferences: dict

@function_tool
async def get_user_preference(wrapper: RunContextWrapper[UserContext]) -> str:
    user = wrapper.context
    return f"User {user.username} prefers {user.preferences.get('theme', 'default')} theme"

async def main():
    # Create context with user data
    user_context = UserContext(
        user_id="123",
        username="Alice", 
        preferences={"theme": "dark", "language": "en"}
    )
    
    agent = Agent[UserContext](
        name="PersonalAssistant",
        instructions="You are a helpful personal assistant.",
        tools=[get_user_preference]
    )
    
    # Context is available to tools, but conversation memory still needs manual handling
    result = await Runner.run(
        agent, 
        "What's my name and theme preference?", 
        context=user_context
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
