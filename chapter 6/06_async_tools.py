"""Asynchronous Tools Example

Shows how to create async tools for external APIs:
- Async function tools for better performance
- External API integration with httpx
- Error handling for network requests
- Real-time data fetching capabilities

Usage:
    python 06_async_tools.py
"""

import asyncio
import httpx
from agents import Agent, Runner, function_tool
from pydantic import BaseModel
from typing import Optional

class PostData(BaseModel):
    id: int
    title: str
    body: str
    userId: int

class WeatherInfo(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int

@function_tool
async def fetch_random_post() -> PostData:
    """Fetch a random post from JSONPlaceholder API.
    
    Returns:
        Random post data from the free JSONPlaceholder API
    """
    try:
        async with httpx.AsyncClient() as client:
            # Use free JSONPlaceholder API
            import random
            post_id = random.randint(1, 100)
            response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
            response.raise_for_status()
            data = response.json()
            
            return PostData(
                id=data["id"],
                title=data["title"],
                body=data["body"],
                userId=data["userId"]
            )
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch post data: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")

@function_tool
async def get_weather_data(city: str) -> WeatherInfo:
    """Fetch current weather information using wttr.in free API.
    
    Args:
        city: Name of the city
        
    Returns:
        Current weather information
    """
    try:
        async with httpx.AsyncClient() as client:
            # Use free wttr.in weather API
            response = await client.get(
                f"https://wttr.in/{city}?format=j1",
                headers={"User-Agent": "curl/7.68.0"}
            )
            response.raise_for_status()
            data = response.json()
            
            current = data["current_condition"][0]
            
            return WeatherInfo(
                city=city.title(),
                temperature=float(current["temp_C"]),
                description=current["weatherDesc"][0]["value"],
                humidity=int(current["humidity"])
            )
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch weather data: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")

@function_tool
async def fetch_user_info(user_id: int) -> dict:
    """Fetch user information from JSONPlaceholder API.
    
    Args:
        user_id: User ID to fetch (1-10)
        
    Returns:
        User information including name, email, and company
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
            response.raise_for_status()
            data = response.json()
            
            return {
                "id": data["id"],
                "name": data["name"],
                "email": data["email"],
                "company": data["company"]["name"],
                "city": data["address"]["city"]
            }
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch user data: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")

# Create content analyst with real API tools
content_analyst = Agent(
    name="Content Analyst",
    instructions="""You are a content analyst with access to real APIs.
    Use the available tools to fetch posts, user information, and provide
    insights about content and users.""",
    tools=[fetch_random_post, fetch_user_info],
)

# Create weather assistant with real weather API
weather_assistant = Agent(
    name="Weather Assistant",
    instructions="""You are a weather assistant with access to real weather data.
    Use the available tools to provide current weather information for any city.""",
    tools=[get_weather_data],
)

async def demo_async_tools():
    """Demonstrate asynchronous tools with external API simulation"""
    
    queries = [
        ("content_analyst", "Fetch a random post and tell me about its author"),
        ("weather_assistant", "What's the weather like in Tokyo?"),
        ("content_analyst", "Get another random post and analyze its content"),
        ("weather_assistant", "Check the weather in London"),
        ("content_analyst", "Fetch user information for user ID 5")
    ]
    
    print("⚡ ASYNCHRONOUS TOOLS DEMONSTRATION")
    print("Using async tools for external API integration")
    print("=" * 70)
    
    for i, (agent_type, query) in enumerate(queries, 1):
        agent = content_analyst if agent_type == "content_analyst" else weather_assistant
        
        print(f"\n{i}️⃣ Agent: {agent.name}")
        print(f"Query: {query}")
        print("-" * 50)
        
        start_time = asyncio.get_event_loop().time()
        try:
            result = await Runner.run(agent, query)
            end_time = asyncio.get_event_loop().time()
            
            print(f"Response: {result.final_output}")
            print(f"⏱️ Execution time: {end_time - start_time:.2f} seconds")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_async_tools())
