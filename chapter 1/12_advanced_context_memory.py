"""Advanced Context Memory Example

This example demonstrates sophisticated memory management with persistent context:
- Building custom memory systems using context objects
- Creating remember_fact and recall_facts tools for long-term memory
- Maintaining persistent state across multiple conversation sessions
- Implementing memory-aware agents that learn and retain information

Advanced pattern for agents that need to remember user information long-term.

Usage:
    python 12_advanced_context_memory.py
"""

import os
import asyncio
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List
from agents import Agent, Runner, RunContextWrapper, function_tool

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

# 1) Define a context object that will *hold* memory between turns
@dataclass
class MemoryCtx:
    """Very simple key–value memory."""
    facts: List[str] = field(default_factory=list)

# 2) Two function tools the model can call to work with that memory
@function_tool
async def remember_fact(wrapper: RunContextWrapper[MemoryCtx], fact: str) -> str:
    """Store a user-supplied fact in long-term memory."""
    wrapper.context.facts.append(fact)
    return "Got it — I'll remember that."

@function_tool
async def recall_facts(wrapper: RunContextWrapper[MemoryCtx]) -> str:
    """Return everything the assistant knows so far."""
    if not wrapper.context.facts:
        return "Memory is empty."
    return "\n".join(wrapper.context.facts)

# 3) Build the agent and give it the two tools
memo_agent = Agent[MemoryCtx](
    name="MemoAssistant",
    model="gpt-4o-mini",
    instructions=(
        "You are a helpful assistant that can *remember* things over time.\n"
        "- When the user tells you something biographical or a preference, call "
        "`remember_fact` with the relevant sentence so you don't forget.\n"
        "- When you're unsure, call `recall_facts` to refresh your memory."
    ),
    tools=[remember_fact, recall_facts],
)

async def main() -> None:
    # Create a *single* MemoryCtx that we reuse for every turn
    memory = MemoryCtx()

    # First interaction — user teaches the agent something
    await Runner.run(
        starting_agent=memo_agent,
        input="My birthday is 29 June.",
        context=memory,
    )

    # Second interaction — model should recall the stored fact
    result = await Runner.run(
        starting_agent=memo_agent,
        input="When is my birthday?",
        context=memory,
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
