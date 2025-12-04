"""Multiple Handoff Router Example

This example demonstrates intelligent routing between multiple specialized agents:
- Creating language-specific specialist agents
- Building a router agent that intelligently delegates to specialists
- Handling multiple handoff targets with clear routing logic
- Language learning and practice use case with specialized responses

Advanced pattern for building multi-specialist agent systems.

Usage:
    python 02_multiple_handoff_router.py
"""

import asyncio
from agents import Agent, Runner

# Create language specialists
spanish_agent = Agent(
    name="Spanish Specialist",
    instructions="Eres un especialista en español. Responde siempre en español y ayuda con práctica del idioma."
)

french_agent = Agent(
    name="French Specialist", 
    instructions="Vous êtes un spécialiste français. Répondez toujours en français et aidez avec la pratique de la langue."
)

german_agent = Agent(
    name="German Specialist",
    instructions="Sie sind ein deutscher Spezialist. Antworten Sie immer auf Deutsch und helfen Sie beim Sprachenlernen."
)

# Use direct agent handoffs
main_agent = Agent(
    name="Language Router",
    instructions="""You are a language routing assistant. When users 
    want to practice or communicate in a specific language, hand off to 
    the appropriate language specialist:
    - For Spanish: hand off to Spanish Specialist
    - For French: hand off to French Specialist  
    - For German: hand off to German Specialist""",
    handoffs=[spanish_agent, french_agent, german_agent],
)

async def demo_custom_handoff():
    """Demonstrate custom handoff routing"""
    
    queries = [
        "What languages do you support?",
        "I want to practice Spanish conversation",
        "Help me learn French phrases", 
        "Can you teach me German grammar?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = await Runner.run(main_agent, query)
        print(f"Response: {result.final_output}")
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(demo_custom_handoff())
