"""Simple Tool Integration Example

This example demonstrates basic tool integration with agents:
- Creating function tools with @function_tool decorator
- Automatic tool discovery and execution by agents
- Building agents that can call external functions
- Simple tool patterns for time, weather, and data retrieval

Foundational pattern for extending agent capabilities with custom functions.

Usage:
    python 14_simple_tool.py
"""

import os
from dotenv import load_dotenv
from agents import function_tool, Agent, Runner
from datetime import datetime

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

@function_tool
def get_current_time() -> str:
    """Get the current time in a human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def get_weather(city: str) -> str:
    """Get current weather information for a city."""
    # In a real implementation, you'd call a weather API
    # For demo purposes, we'll return a mock response
    return f"The weather in {city} is sunny with a temperature of 22°C"

# Create an agent with tools
assistant = Agent(
    name="WeatherAssistant",
    instructions="""
    You are a helpful assistant that can provide time and weather information.
    Use the available tools when users ask about time or weather.
    """,
    tools=[get_current_time, get_weather]
)

# The agent can now use these tools automatically
result = Runner.run_sync(assistant, "What time is it and what's the weather like in Tokyo?")
print(result.final_output)
