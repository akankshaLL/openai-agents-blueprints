"""Interactive Demo Agent Example

This example demonstrates interactive conversation capabilities:
- Using run_demo_loop for continuous chat sessions
- Asynchronous agent execution with async/await
- Building conversational agents that maintain engagement
- Handling user input in real-time interactive scenarios

Perfect for prototyping chatbots and conversational AI applications.

Usage:
    python 04_interactive_demo.py
    (Type 'quit' to exit the conversation)
"""

import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, run_demo_loop

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

async def main():
    conversational_agent = Agent(
        name="FriendlyAssistant",
        instructions="""
        You are a friendly, helpful AI assistant. Keep your responses 
        conversational and engaging. Ask follow-up questions when 
        appropriate to keep the conversation flowing naturally.
        """
    )
    
    print("Starting interactive conversation. Type 'quit' to exit.")
    await run_demo_loop(conversational_agent)

if __name__ == "__main__":
    asyncio.run(main())
