"""RunResult Basics Example

This example demonstrates essential RunResult properties and usage:
- Accessing final_output for the main agent response
- Examining execution metadata (agent info, item counts)
- Using to_input_list() for conversation continuation
- Monitoring token usage and API costs

Foundational knowledge for working with agent responses and building conversational flows.

Usage:
    python 05_run_result.py
"""

import os
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

agent = Agent(
    name="TimeKeeper",
    instructions="Help users with time-related queries using available tools.",
    tools=[get_current_time]
)

result = Runner.run_sync(agent, "What time is it?")

# Primary output
print(f"Final Response: {result.final_output}")

# Execution metadata
print(f"Executing Agent: {result.last_agent.name}")
print(f"Total Items Generated: {len(result.new_items)}")
print(f"Raw API Responses: {len(result.raw_responses)}")

# Conversation continuation
conversation_history = result.to_input_list()
print(f"Messages for Next Turn: {len(conversation_history)}")

# Usage analytics
if result.raw_responses:
    usage = result.raw_responses[0].usage
    print(f"Tokens Used: {usage.total_tokens} (Input: {usage.input_tokens}, Output: {usage.output_tokens})")
