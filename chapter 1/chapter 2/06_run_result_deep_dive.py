"""RunResult Deep Dive Example

This example demonstrates comprehensive RunResult analysis:
- Building debugging functions to analyze agent execution
- Understanding new_items breakdown and execution flow
- Token usage tracking and cost estimation
- Performance monitoring and optimization insights

Advanced pattern for building production monitoring and debugging tools.

Usage:
    python 06_run_result_deep_dive.py
"""

import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from datetime import datetime

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

def analyze_runresult(result, title="RunResult Analysis"):
    """Comprehensive analysis of a RunResult object for debugging and monitoring."""
    
    print(f"\n{'='*60}")
    print(f"{title.upper()}")
    print('='*60)
    
    # Basic properties
    print("📊 BASIC PROPERTIES:")
    print(f"   Final Output Type: {type(result.final_output)}")
    print(f"   Final Output Length: {len(str(result.final_output))} characters")
    print(f"   Last Agent: {result.last_agent.name}")
    print(f"   Total New Items: {len(result.new_items)}")
    print(f"   Raw Responses: {len(result.raw_responses)}")
    
    # Item breakdown - understand what happened
    if result.new_items:
        print(f"\n📝 NEW ITEMS BREAKDOWN:")
        item_types = {}
        for item in result.new_items:
            item_type = item.type
            item_types[item_type] = item_types.get(item_type, 0) + 1
        
        for item_type, count in item_types.items():
            print(f"   {item_type}: {count}")
    
    # Token usage and cost tracking
    if result.raw_responses:
        print(f"\n💰 TOKEN USAGE:")
        total_input = 0
        total_output = 0
        
        for i, response in enumerate(result.raw_responses):
            usage = response.usage
            total_input += usage.input_tokens
            total_output += usage.output_tokens
            print(f"   Turn {i+1}: {usage.input_tokens} in, {usage.output_tokens} out")
        
        print(f"   TOTAL: {total_input} in, {total_output} out")
        
        # Cost estimation (example rates for GPT-4)
        cost_per_1k_input = 0.0015
        cost_per_1k_output = 0.002
        estimated_cost = (total_input / 1000 * cost_per_1k_input) + (total_output / 1000 * cost_per_1k_output)
        print(f"   Estimated Cost: ${estimated_cost:.4f}")
    
    # Conversation continuation readiness
    print(f"\n💬 CONVERSATION MANAGEMENT:")
    input_list = result.to_input_list()
    print(f"   Input List Length: {len(input_list)}")
    print(f"   Ready for Continuation: {'✅' if input_list else '❌'}")

@function_tool
def get_current_time() -> str:
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def main():
    """Demo the deep RunResult analysis."""
    print("🔍 Deep RunResult Analysis Demo")
    print("=" * 50)
    
    # Create an agent with tools
    agent = Agent(
        name="AnalyticsAgent",
        instructions="You are a helpful assistant that can use tools. When asked about time, use the time tool.",
        tools=[get_current_time]
    )
    
    # Simple query
    print("\n📋 Testing simple query...")
    result1 = await Runner.run(agent, "What time is it?")
    analyze_runresult(result1, "Simple Time Query")
    
    # Complex query that might use tools
    print("\n📋 Testing complex query...")
    result2 = await Runner.run(agent, "Can you tell me the current time and then explain why time tracking is important?")
    analyze_runresult(result2, "Complex Query with Tool Usage")
    
    # Show the actual responses
    print(f"\n🤖 Agent Response 1: {result1.final_output}")
    print(f"🤖 Agent Response 2: {result2.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
