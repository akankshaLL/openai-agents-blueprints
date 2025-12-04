"""Production Conversation Example

This example demonstrates production-ready conversation management:
- Building a ConversationManager class for multi-turn dialogues
- Automatic conversation history management and trimming
- Session metadata and context preservation
- Production patterns for conversation state management

Practical pattern for building conversational applications with proper state management.

Usage:
    python 10_production_example_conversation.py
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

class ConversationManager:
    """Manages multi-turn conversations with context preservation."""
    
    def __init__(self, agent, max_history_length=20):
        self.agent = agent
        self.conversation_history = []
        self.max_history_length = max_history_length
        self.session_metadata = {}
    
    def add_context(self, key, value):
        """Add metadata to the session context."""
        self.session_metadata[key] = value
    
    async def send_message(self, user_message):
        """Send a message and maintain conversation state."""
        
        # Build input: conversation history + new message
        if self.conversation_history:
            current_input = self.conversation_history + [
                {"role": "user", "content": user_message}
            ]
        else:
            current_input = user_message
        
        # Execute agent
        result = await Runner.run(self.agent, current_input)
        
        # Update conversation history
        self.conversation_history = result.to_input_list()
        
        # Trim history if it gets too long
        if len(self.conversation_history) > self.max_history_length:
            # Keep first message (usually system/instructions) and recent messages
            self.conversation_history = (
                self.conversation_history[:1] + 
                self.conversation_history[-(self.max_history_length-1):]
            )
        
        return result
    
    def get_conversation_summary(self):
        """Get a summary of the conversation for analysis."""
        return {
            "total_messages": len(self.conversation_history),
            "session_metadata": self.session_metadata,
            "last_agent": self.conversation_history[-1].get("role") if self.conversation_history else None
        }

async def main():
    print("🏢 Production Conversation Manager Demo")
    print("=" * 50)
    
    # Usage example
    support_agent = Agent(
        name="SupportAgent",
        instructions="""
        You are a customer support agent. Remember customer details shared 
        in the conversation and provide personalized assistance.
        """
    )

    conversation = ConversationManager(support_agent)
    conversation.add_context("customer_tier", "premium")

    # Multi-turn conversation
    print("Starting customer support conversation...\n")
    
    response1 = await conversation.send_message("Hi, I'm having trouble with my account login")
    print(f"🙋 Customer: Hi, I'm having trouble with my account login")
    print(f"🤖 Agent: {response1.final_output}\n")

    response2 = await conversation.send_message("My username is john.doe@email.com")
    print(f"🙋 Customer: My username is john.doe@email.com")
    print(f"🤖 Agent: {response2.final_output}\n")

    response3 = await conversation.send_message("Can you check my account status?")
    print(f"🙋 Customer: Can you check my account status?")
    print(f"🤖 Agent: {response3.final_output}\n")

    print("📊 Conversation Summary:")
    summary = conversation.get_conversation_summary()
    print(f"   Total Messages: {summary['total_messages']}")
    print(f"   Session Metadata: {summary['session_metadata']}")
    print(f"   Last Agent Role: {summary['last_agent']}")
    
    print(f"\n{'='*50}")
    print("Demo completed! Notice how the agent maintains context")
    print("across multiple conversation turns.")

if __name__ == "__main__":
    asyncio.run(main())
