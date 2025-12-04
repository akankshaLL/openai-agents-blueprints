"""Basic Tools Example

Shows how to create function tools for agents:
- @function_tool decorator to create tools
- Pydantic models for structured data
- Multiple tools per agent
- Tool documentation with docstrings

Usage:
    python 01_basic_tools.py
"""

import asyncio
from agents import Agent, Runner, function_tool
from pydantic import BaseModel
from typing import List

class WeatherData(BaseModel):
    city: str
    temperature: float
    conditions: str
    humidity: int
    forecast: List[str]

@function_tool
def get_current_weather(city: str) -> WeatherData:
    """Get current weather conditions for a specified city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Current weather data including temperature and conditions
    """
    # Mock weather data - in real implementation, call weather API
    weather_db = {
        "new york": WeatherData(
            city="New York",
            temperature=18.5,
            conditions="Cloudy",
            humidity=72,
            forecast=["Light rain tomorrow", "Sunny weekend"]
        ),
        "london": WeatherData(
            city="London", 
            temperature=12.0,
            conditions="Rainy",
            humidity=85,
            forecast=["Overcast tomorrow", "Clearing up Friday"]
        ),
        "tokyo": WeatherData(
            city="Tokyo",
            temperature=25.3,
            conditions="Sunny",
            humidity=58,
            forecast=["Hot and humid tomorrow", "Thunderstorms possible"]
        )
    }
    
    return weather_db.get(city.lower(), WeatherData(
        city=city,
        temperature=20.0,
        conditions="Data unavailable",
        humidity=50,
        forecast=["No forecast available"]
    ))

@function_tool
def get_weather_alerts(city: str) -> List[str]:
    """Get weather alerts and warnings for a city.
    
    Args:
        city: The name of the city to check for alerts
        
    Returns:
        List of active weather alerts
    """
    # Mock alert data
    alerts_db = {
        "miami": ["Hurricane watch in effect", "Flood warning until 6 PM"],
        "denver": ["Snow advisory - 3-6 inches expected"],
        "phoenix": ["Extreme heat warning - temperatures over 110°F"]
    }
    
    return alerts_db.get(city.lower(), [])

# Create weather agent with tools
weather_agent = Agent(
    name="Weather Assistant",
    instructions="""You are a helpful weather assistant. Use the available tools to provide 
    accurate, up-to-date weather information for any city users ask about.
    
    Available tools:
    - get_current_weather: Get current conditions and forecast
    - get_weather_alerts: Check for weather warnings and alerts
    
    Always provide comprehensive weather information including current conditions and any alerts.""",
    tools=[get_current_weather, get_weather_alerts],
)

async def demo_basic_tools():
    """Demonstrate basic function tools with structured data"""
    
    queries = [
        "What's the weather like in New York?",
        "Is there any weather alert for Miami?", 
        "Tell me about the weather in Tokyo and any warnings",
        "What's the forecast for London?",
        "Check weather and alerts for Phoenix"
    ]
    
    print("🛠️ BASIC TOOLS DEMONSTRATION")
    print("Function tools with structured data and multiple tool usage")
    print("=" * 70)
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}️⃣ Query: {query}")
        print("-" * 50)
        
        result = await Runner.run(weather_agent, query)
        print(f"Response: {result.final_output}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_basic_tools())
