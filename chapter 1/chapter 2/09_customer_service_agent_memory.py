"""Customer Service Agent Memory Example

This example demonstrates sophisticated conversation management for customer service:
- Building a CustomerServiceAgent class with persistent memory
- Extracting and storing customer information across conversation turns
- Managing conversation length and token limits automatically
- Advanced conversation patterns: branching, merging, and context preservation
- Production-ready error handling and conversation debugging

Comprehensive pattern for building enterprise-grade conversational agents.

Usage:
    python 09_customer_service_agent_memory.py
"""

import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from datetime import datetime
from typing import List, Dict, Any

load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

# Customer service tools
@function_tool
def lookup_order(order_id: str) -> str:
    """Look up order information by order ID."""
    # Simulate database lookup
    orders = {
        "ORD123": "Order ORD123: 2x Wireless Headphones, Status: Shipped, Tracking: TRK456789",
        "ORD456": "Order ORD456: 1x Laptop, Status: Processing, Expected Ship: Tomorrow",
        "ORD789": "Order ORD789: 3x Books, Status: Delivered, Delivered on: 2025-06-25"
    }
    return orders.get(order_id, f"Order {order_id} not found in system")

@function_tool
def check_return_policy() -> str:
    """Get current return policy information."""
    return "30-day return policy. Items must be unused and in original packaging. Free return shipping for defective items."

@function_tool
def create_support_ticket(issue: str, priority: str = "medium") -> str:
    """Create a support ticket for complex issues."""
    ticket_id = f"TKT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return f"Support ticket {ticket_id} created for: {issue}. Priority: {priority}. Expected response: 24-48 hours."

class CustomerServiceAgent:
    def __init__(self):
        self.agent = Agent(
            name="CustomerServiceAgent",
            instructions="""
            You are a helpful customer service representative. 
            
            Key behaviors:
            - Remember customer information throughout the conversation
            - Reference previous parts of the conversation when relevant
            - Use tools to look up orders and create tickets when needed
            - Be friendly, professional, and solution-oriented
            - If you can't resolve an issue, create a support ticket
            
            Always greet customers warmly and ask how you can help.
            """,
            tools=[lookup_order, check_return_policy, create_support_ticket]
        )
        self.conversation_history = []
        self.customer_info = {}
async def customer_service_demo():
    """Demonstrate sophisticated conversation management."""
    
    print("🎧 CUSTOMER SERVICE CONVERSATION DEMO")
    print("="*50)
    
    service_agent = CustomerServiceAgent()
    
    # Simulate a customer service conversation
    conversation_turns = [
        "Hi, my name is Sarah and I need help with my order",
        "I ordered wireless headphones, order number ORD123",
        "When will it arrive? I need it for next week",
        "Actually, I want to return it instead. What's your return policy?",
        "Perfect! Can you help me start the return process?",
        "Thanks! What's my ticket number for reference?"
    ]
    
    print("Starting customer service conversation...\n")
    
    for i, user_message in enumerate(conversation_turns, 1):
        print(f"🗣️ Customer (Turn {i}): {user_message}")
        
        # Process message
        response_data = await service_agent.chat(user_message)
        
        print(f"🤖 Agent: {response_data['response']}")
        print(f"📊 Metrics: {response_data['conversation_length']} messages, "
              f"{response_data['token_usage']['total_tokens']} tokens, "
              f"{response_data['tools_used']} tools used")
        
        # Show customer info extraction
        if response_data['customer_info']:
            print(f"👤 Customer Info: {response_data['customer_info']}")
        
        print("-" * 50)
        
        # Manage conversation length (demo with low threshold)
        await service_agent.manage_conversation_length(max_messages=10)
    
    # Final conversation summary
    summary = service_agent.get_conversation_summary()
    print("\n📋 CONVERSATION SUMMARY:")
    print(f"Total Messages: {summary['total_messages']}")
    print(f"Customer Info Collected: {summary['customer_info']}")
    print(f"Ready for Handoff: {summary['conversation_ready_for_handoff']}")

async def advanced_conversation_patterns():
    """Demonstrate advanced conversation management patterns."""
    
    print("\n🔧 ADVANCED CONVERSATION PATTERNS")
    print("="*50)
    
    agent = Agent(
        name="AdvancedAgent",
        instructions="You are a helpful assistant that can continue conversations seamlessly."
    )
    
    # Pattern 1: Conversation Branching
    print("\n1. CONVERSATION BRANCHING:")
    result1 = await Runner.run(agent, "I'm planning a trip to Japan")
    print(f"Initial: {result1.final_output}")
    
    # Branch A: Focus on activities
    branch_a_input = result1.to_input_list() + [{"role": "user", "content": "What activities should I do?"}]
    result_a = await Runner.run(agent, branch_a_input)
    print(f"Branch A: {result_a.final_output[:100]}...")
    
    # Branch B: Focus on budget (from same starting point)
    branch_b_input = result1.to_input_list() + [{"role": "user", "content": "How much should I budget?"}]
    result_b = await Runner.run(agent, branch_b_input)
    print(f"Branch B: {result_b.final_output[:100]}...")
    
    # Pattern 2: Conversation Merging
    print("\n2. CONVERSATION MERGING:")
    # Combine insights from both branches
    merged_input = result_a.to_input_list() + [
        {"role": "user", "content": "Now considering the budget advice too, what's your top recommendation?"}
    ]
    result_merged = await Runner.run(agent, merged_input)
    print(f"Merged: {result_merged.final_output[:150]}...")
    
    # Pattern 3: Context Preservation
    print("\n3. CONTEXT PRESERVATION:")
    conversation = result_merged.to_input_list()
    
    # Add context about user preferences
    conversation.append({"role": "user", "content": "By the way, I'm vegetarian and love art"})
    result_context = await Runner.run(agent, conversation)
    print(f"With Context: {result_context.final_output[:150]}...")

def conversation_debugging_tips():
    """Provide debugging tips for conversation management."""
    
    print("\n🔍 CONVERSATION DEBUGGING TIPS")
    print("="*50)
    
    tips = [
        "1. Always check conversation_history length before sending to avoid token limits",
        "2. Use result.to_input_list() instead of manually building message arrays",
        "3. Store customer/user info separately from conversation history",
        "4. Monitor token usage per turn to predict when to truncate",
        "5. Test conversation branching and merging in development",
        "6. Implement conversation summaries for long interactions",
        "7. Use structured logging to track conversation state changes"
    ]
    
    for tip in tips:
        print(f"   {tip}")
    
    print(f"\n💡 Pro Tip: In production, implement conversation persistence")
    print(f"   to resume conversations across sessions using database storage.")

if __name__ == "__main__":
    async def main():
        await customer_service_demo()
        await advanced_conversation_patterns()
        conversation_debugging_tips()
    
    asyncio.run(main())
