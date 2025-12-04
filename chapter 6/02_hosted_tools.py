"""OpenAI's Hosted Tools Example

Shows how to use OpenAI's hosted tools:
- WebSearchTool for internet search capabilities
- Configuring hosted tools with parameters
- Using tools that run on OpenAI's servers
- Real-time information retrieval

Usage:
    python 02_hosted_tools.py
"""

import asyncio
from agents import Agent, Runner, WebSearchTool

# Create research agent with web search tool
research_agent = Agent(
    name="Research Assistant",
    instructions="""You are a research assistant that helps users find current, 
    accurate information. Always search for the most recent information available 
    and cite your sources clearly.""",
    tools=[
        WebSearchTool(
            user_location={"type": "approximate", "city": "New York"},
            search_context_size="medium"
        )
    ],
)

# Create news agent with different search configuration
news_agent = Agent(
    name="News Reporter",
    instructions="""You are a news reporter focused on current events. 
    Search for the latest news and provide factual, unbiased reporting 
    with proper source attribution.""",
    tools=[
        WebSearchTool(
            user_location={"type": "approximate", "city": "London"},
            search_context_size="low"
        )
    ],
)

async def demo_hosted_tools():
    """Demonstrate hosted tools with web search"""
    
    queries = [
        ("research_agent", "What are the latest developments in quantum computing?"),
        ("research_agent", "Current status of renewable energy adoption worldwide"),
        ("news_agent", "Latest news about artificial intelligence regulations"),
        ("research_agent", "Recent breakthroughs in medical AI applications"),
        ("news_agent", "What's happening with climate change policies this week?")
    ]
    
    print("🌐 HOSTED TOOLS DEMONSTRATION")
    print("Using OpenAI's WebSearchTool for real-time information")
    print("=" * 70)
    
    for i, (agent_type, query) in enumerate(queries, 1):
        agent = research_agent if agent_type == "research_agent" else news_agent
        
        print(f"\n{i}️⃣ Agent: {agent.name}")
        print(f"Query: {query}")
        print("-" * 50)
        
        try:
            result = await Runner.run(agent, query)
            print(f"Response: {result.final_output}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_hosted_tools())
