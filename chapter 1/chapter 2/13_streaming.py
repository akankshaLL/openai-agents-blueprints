"""Streaming Agent Execution Example

This example demonstrates real-time streaming responses:
- Using Runner.run_streamed() for real-time output
- Processing stream events as they arrive from the API
- Building responsive chat interfaces with immediate feedback
- Handling different event types (raw responses, message completion)

Critical pattern for building engaging, responsive conversational interfaces.

Usage:
    python 13_streaming.py
"""

import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

async def demonstrate_streaming_execution():
    """Demonstrate streaming execution with real-time output."""
    
    print("📡 STREAMING EXECUTION DEMO")
    print("="*40)
    
    storyteller = Agent(
        name="Storyteller",
        model="gpt-4o",
        model_settings=ModelSettings(temperature=0.8),
        instructions="You are a creative storyteller. Write engaging, descriptive stories."
    )
    
    print("Starting streaming execution...")
    print("Story output (streaming in real-time):")
    print("-" * 50)
    
    # Start streaming
    result = Runner.run_streamed(
        storyteller, 
        "Write a short story about a robot discovering music for the first time. Keep it to about 100 words."
    )
    
    # Process stream events
    full_text = ""
    async for event in result.stream_events():
        # Handle different event types
        if event.type == "raw_response_event":
            # This contains the raw streaming tokens from OpenAI
            if hasattr(event.data, 'delta') and event.data.delta:
                print(event.data.delta, end="", flush=True)
                full_text += event.data.delta
        elif event.type == "run_item_stream_event":
            # This contains higher-level events like tool calls, message completion
            if event.item.type == "message_output_item":
                # Message completed
                pass
    
    print("\n" + "-" * 50)
    print("✅ Streaming complete!")
    print(f"Total characters streamed: {len(full_text)}")
    print("\nStreaming execution provides real-time feedback to users.")
    print("Use this for: Chat interfaces, long-form content, user engagement\n")

if __name__ == "__main__":
    asyncio.run(demonstrate_streaming_execution())
