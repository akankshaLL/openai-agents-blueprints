"""Simple Agent Handoff Example

This example demonstrates basic agent-to-agent handoff patterns:
- Creating specialized agents with specific tools and expertise
- Using handoffs parameter to enable agent delegation
- Automatic routing based on query type and agent capabilities
- Building multi-agent systems with clear specialization boundaries

Foundational pattern for creating collaborative agent systems.

Usage:
    python 01_simple_handoff.py
"""

import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    # Mock weather data - in real app, call weather API
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Cloudy, 15°C", 
        "tokyo": "Rainy, 18°C",
        "default": "Partly cloudy, 68°F"
    }
    return weather_data.get(location.lower(), weather_data["default"])

# Create a weather specialist with weather tool
weather_agent = Agent(
    name="Weather Specialist",
    instructions="""You are a weather specialist with access to real-time weather data.
    Use the get_weather tool to provide accurate current weather information.""",
    tools=[get_weather]
)

# Create a general agent that can hand off to weather specialist
general_agent = Agent(
    name="General Assistant", 
    instructions="""You are a helpful general assistant. You can answer general questions,
    but for specific weather requests, hand off to the Weather Specialist who has 
    access to real-time weather data.""",
    handoffs=[weather_agent],
)

async def demo_handoff():
    """Demonstrate agent handoff functionality"""
    
    queries = [
        "What's the weather like in New York?",  # Weather query - should handoff
        "How do I stay healthy?",  # General query - no handoff
        "Is it raining in London right now?",  # Weather query - should handoff  
        "What are some good books to read?",  # General query - no handoff
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = await Runner.run(general_agent, query)
        print(f"Response: {result.final_output}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_handoff())
