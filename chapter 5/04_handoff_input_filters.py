"""Handoff Input Filters Example

This example demonstrates secure data filtering during agent handoffs:
- Building filter_sensitive_data function to remove PII and sensitive information
- Creating filter_remove_tools to clean conversation history of tool calls
- Implementing secure handoff patterns that protect customer privacy
- Demonstrating different filtering strategies for different agent types

Critical pattern for building secure, privacy-compliant multi-agent systems.

Usage:
    python 04_handoff_input_filters.py
"""

import asyncio
import re
from agents import Agent, Runner, function_tool
from typing import Dict, Any, List

# Create secure customer service agent
customer_service_agent = Agent(
    name="Customer Service",
    instructions="You are a customer service agent. Help customers while maintaining data privacy."
)

# Create financial advisor (needs filtered data)
financial_agent = Agent(
    name="Financial Advisor", 
    instructions="You are a financial advisor. Provide advice without seeing sensitive payment details."
)

def filter_sensitive_data(conversation_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter sensitive information from conversation history"""
    
    filtered_history = []
    
    for message in conversation_history:
        if message.get("role") == "user":
            content = message["content"]
            
            # Remove credit card numbers
            content = re.sub(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", 
                           "[CARD-REDACTED]", content)
            
            # Remove SSN patterns
            content = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN-REDACTED]", content)
            
            # Remove phone numbers
            content = re.sub(r"\b\d{3}-\d{3}-\d{4}\b", "[PHONE-REDACTED]", content)
            
            # Remove email addresses
            content = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", 
                           "[EMAIL-REDACTED]", content)
            
            filtered_message = {**message, "content": content}
            filtered_history.append(filtered_message)
        else:
            # Keep assistant messages as-is
            filtered_history.append(message)
    
    return filtered_history

def filter_remove_tools(conversation_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove tool calls from conversation history"""
    
    filtered_history = []
    
    for message in conversation_history:
        # Skip messages with tool calls
        if message.get("tool_calls") or message.get("role") == "tool":
            continue
        filtered_history.append(message)
    
    return filtered_history

@function_tool
def secure_handoff_to_financial(query: str) -> str:
    """Securely hand off to financial advisor with filtered context"""
    
    # Simulate conversation history
    conversation = [
        {"role": "user", "content": "My credit card 4532-1234-5678-9012 was charged twice"},
        {"role": "assistant", "content": "I see there's a billing issue. Let me help you."},
        {"role": "user", "content": query}
    ]
    
    # Filter sensitive data
    filtered_conv = filter_sensitive_data(conversation)
    
    print("🔒 FILTERING DEMONSTRATION:")
    print("Original conversation:")
    for msg in conversation:
        print(f"  {msg['role']}: {msg['content']}")
    
    print("\nFiltered conversation:")
    for msg in filtered_conv:
        print(f"  {msg['role']}: {msg['content']}")
    
    return "Handoff to financial advisor with filtered context"

@function_tool  
def secure_handoff_to_service(query: str) -> str:
    """Hand off to customer service with tool calls removed"""
    
    # Simulate conversation with tool calls
    conversation = [
        {"role": "user", "content": "I need help with my account"},
        {"role": "assistant", "content": "Let me check your account", "tool_calls": [{"function": "get_account_info"}]},
        {"role": "tool", "content": "Account details: Premium user since 2020"},
        {"role": "assistant", "content": "I can see your account details."},
        {"role": "user", "content": query}
    ]
    
    # Remove tool calls
    filtered_conv = filter_remove_tools(conversation)
    
    print("🛠️ TOOL FILTERING DEMONSTRATION:")
    print("Original conversation:")
    for msg in conversation:
        role = msg['role']
        content = msg.get('content', '')
        tools = ' [TOOL_CALLS]' if msg.get('tool_calls') else ''
        print(f"  {role}: {content}{tools}")
    
    print("\nFiltered conversation (tools removed):")
    for msg in filtered_conv:
        print(f"  {msg['role']}: {msg['content']}")
    
    return "Handoff to customer service with tools removed"

# Create main agent with filtering capabilities
main_agent = Agent(
    name="Main Agent",
    instructions="""You are a main agent that handles initial customer requests.
    
    For financial questions: Use secure_handoff_to_financial (filters sensitive data)
    For general service: Use secure_handoff_to_service (removes tool calls)
    
    Always prioritize customer privacy and data security.""",
    tools=[secure_handoff_to_financial, secure_handoff_to_service],
    handoffs=[financial_agent, customer_service_agent]
)

async def demo_input_filters():
    """Demonstrate handoff input filtering"""
    
    test_scenarios = [
        {
            "query": "I need financial advice about my investments",
            "description": "Financial query - should filter sensitive data"
        },
        {
            "query": "I need general help with my account settings", 
            "description": "Service query - should remove tool calls"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario['description']}")
        print(f"Query: {scenario['query']}")
        print("-" * 60)
        
        result = await Runner.run(main_agent, scenario["query"])
        print(f"\nFinal Response: {result.final_output}")

if __name__ == "__main__":
