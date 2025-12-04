"""Dynamic Instructions Agent Example

This example demonstrates runtime instruction modification:
- Dynamically changing agent behavior based on user roles
- Adapting agent personality and expertise for different contexts
- Role-based instruction templates for specialized responses
- Maintaining conversation history across instruction changes

Powerful pattern for building adaptive agents that serve multiple user types.

Usage:
    python 01_dynamic_instructions.py
"""

import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

async def main():
    # Base agent with dynamic instructions
    base_agent = Agent(
        name="DynamicAssistant",
        instructions="You are a helpful assistant."
    )
    
    # Dynamic instruction based on user role
    def get_role_instructions(role: str) -> str:
        instructions_map = {
            "student": "You are a helpful tutor. Explain concepts clearly and provide examples.",
            "developer": "You are a coding assistant. Provide code examples and technical explanations.",
            "business": "You are a business consultant. Focus on strategy and practical advice.",
            "creative": "You are a creative partner. Help brainstorm ideas and provide inspiration."
        }
        return instructions_map.get(role, "You are a helpful assistant.")
    
    # Test different roles with conversation history
    roles = ["student", "developer", "business", "creative"]
    
    for role in roles:
        print(f"\n{'='*50}")
        print(f"TESTING {role.upper()} ROLE")
        print(f"{'='*50}")
        
        # Update agent instructions dynamically
        base_agent.instructions = get_role_instructions(role)
        print(f"📝 Instructions: {base_agent.instructions}")
        
        # Start conversation with role-specific context
        conversation_history = [
            {"role": "user", "content": f"Hello, I'm a {role}. Can you help me?"}
        ]
        
        # First interaction
        result1 = await Runner.run(base_agent, conversation_history)
        print(f"\n🙋 User: Hello, I'm a {role}. Can you help me?")
        print(f"🤖 Agent: {result1.final_output}")
        
        # Update conversation history
        conversation_history = result1.to_input_list()
        
        # Second interaction - test role-specific knowledge
        role_queries = {
            "student": "Can you explain how photosynthesis works?",
            "developer": "How do I implement a binary search algorithm?",
            "business": "What are the key factors for market analysis?",
            "creative": "I need ideas for a new marketing campaign."
        }
        
        conversation_history.append({"role": "user", "content": role_queries[role]})
        result2 = await Runner.run(base_agent, conversation_history)
        
        print(f"\n🙋 User: {role_queries[role]}")
        print(f"🤖 Agent: {result2.final_output}")
        
        # Show conversation summary
        print(f"\n📊 Conversation Summary:")
        print(f"   - Role: {role}")
        print(f"   - Total messages: {len(result2.to_input_list())}")
        print(f"   - Tokens used: {sum(r.usage.total_tokens for r in result2.raw_responses)}")
        
        print(f"\n{'='*50}")

if __name__ == "__main__":
    asyncio.run(main())
