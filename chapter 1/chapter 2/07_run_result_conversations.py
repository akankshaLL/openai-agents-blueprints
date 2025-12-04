"""RunResult Conversations Example

This example demonstrates conversation flow management with RunResult:
- Building conversation history across multiple turns
- Using to_input_list() to maintain context between interactions
- Analyzing token usage and conversation growth over time
- Managing conversation state for multi-turn dialogues

Essential pattern for building conversational agents that remember context.

Usage:
    python 07_run_result_conversations.py
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

@function_tool
def get_current_time() -> str:
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def conversation_with_analysis():
    agent = Agent(
        name="Assistant",
        instructions="You are helpful and remember our conversation.",
        tools=[get_current_time]
    )
    
    conversations = [
        "What time is it?",
        "Remember that time - what was it?",
        "How long ago was that?"
    ]
    
    conversation_history = []
    
    for i, user_input in enumerate(conversations):
        print(f"\n--- Turn {i+1} ---")
        print(f"User: {user_input}")
        
        # Build input with conversation history
        if conversation_history:
            full_input = conversation_history + [{"role": "user", "content": user_input}]
        else:
            full_input = user_input
        
        # Execute and analyze
        result = await Runner.run(agent, full_input)
        print(f"Assistant: {result.final_output}")
        
        # Update conversation history
        conversation_history = result.to_input_list()
        
        # Quick analysis
        if result.raw_responses:
            usage = result.raw_responses[0].usage
            print(f"Tokens: {usage.input_tokens} in, {usage.output_tokens} out")
        
        print(f"Conversation Length: {len(conversation_history)} messages")

async def main():
    print("💬 Conversation Analysis Demo")
    print("=" * 40)
    print("This demo shows how to track conversation history")
    print("and analyze RunResult objects across multiple turns.\n")
    
    await conversation_with_analysis()
    
    print(f"\n{'='*40}")
    print("Demo completed! Notice how the conversation history")
    print("builds up and the agent maintains context.")

if __name__ == "__main__":
    asyncio.run(main())
