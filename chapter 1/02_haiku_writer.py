"""Haiku Writer Agent Example

This example demonstrates advanced agent configuration including:
- Custom model settings (temperature, max_tokens)
- Detailed agent instructions for specialized tasks
- RunResult inspection for monitoring and debugging
- Token usage tracking for cost management
- Production-ready error handling patterns

Shows how to create domain-specific agents with fine-tuned behavior.

Usage:
    python 02_haiku_writer.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunResult, ModelSettings

# Load environment variables (this is production-ready pattern)
load_dotenv()

# Verify API key is available (good security practice)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")

print("🚀 Haiku Writer Agent Starting...")

# Create a specialized haiku writing agent with detailed configuration
haiku_agent = Agent(
    name="HaikuWriter",
    model="gpt-4o",                    # Specify which OpenAI model to use
    model_settings=ModelSettings(      # Configure model behavior
        temperature=0.8,               # Higher creativity for poetry
        max_tokens=100                 # Limit response length
    ),
    instructions="""
    You are a master haiku poet with deep appreciation for nature and human emotion.
    
    When writing haikus:
    1. Follow the traditional 5-7-5 syllable pattern strictly
    2. Include a seasonal reference or nature imagery when possible
    3. Create a moment of revelation or emotional insight
    4. Use simple, evocative language
    5. Present your haiku with proper line breaks
    
    Focus on capturing a single moment in time with beauty and precision.
    """
)

# Define the creative task
user_prompt = "Write a haiku about the silence of a winter forest."

print(f"📝 Prompt: {user_prompt}")
print(f"🤖 Agent: {haiku_agent.name} using {haiku_agent.model}")
print("⏳ Generating haiku...")

# Execute the agent and capture comprehensive results
result: RunResult = Runner.run_sync(haiku_agent, user_prompt)

# Display results with formatting
print("\n" + "="*50)
print("🎋 HAIKU GENERATED")
print("="*50)
print(result.final_output)
print("="*50)

# Inspect the technical details for learning purposes
print("\n📊 EXECUTION DETAILS:")
print(f"   • Model used: {result.last_agent.model}")
print(f"   • Total turns: {len(result.raw_responses)}")
print(f"   • Response items: {len(result.new_items)}")

# Access API usage information for cost monitoring
if result.raw_responses:
    usage = result.raw_responses[0].usage
    print(f"   • Tokens used: {usage.total_tokens} (input: {usage.input_tokens}, output: {usage.output_tokens})")

print("\n✅ Haiku generation complete!")
