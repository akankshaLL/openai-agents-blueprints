"""Custom Handoff Functions Example

This example demonstrates building custom routing logic for agent handoffs:
- Creating analyze_query function for intelligent request categorization
- Building custom routing tools that agents can use for decision making
- Implementing priority-based routing with urgent escalation paths
- Combining programmatic logic with agent intelligence for routing decisions

Advanced pattern for building sophisticated agent routing systems.

Usage:
    python 03_custom_handoff_functions.py
"""

import asyncio
from agents import Agent, Runner, function_tool
from typing import Dict, Any

# Create specialized support agents
billing_agent = Agent(
    name="Billing Specialist",
    instructions="You are a billing specialist. Handle payment, invoice, and subscription questions."
)

technical_agent = Agent(
    name="Technical Support",
    instructions="You are technical support. Handle software bugs, installation, and technical issues."
)

sales_agent = Agent(
    name="Sales Representative", 
    instructions="You are a sales rep. Handle product inquiries, demos, and purchase questions."
)

def analyze_query(query: str, priority: str = "normal") -> str:
    """Analyze query and return routing decision"""
    
    query_lower = query.lower()
    
    # Billing keywords
    billing_keywords = ["payment", "invoice", "bill", "charge", "subscription", "refund", "price"]
    
    # Technical keywords  
    tech_keywords = ["bug", "error", "install", "crash", "not working", "broken", "technical"]
    
    # Sales keywords
    sales_keywords = ["buy", "purchase", "demo", "trial", "features", "pricing", "upgrade"]
    
    # Priority routing for urgent issues
    if priority == "urgent":
        if any(keyword in query_lower for keyword in tech_keywords):
            return "technical_urgent"
        elif any(keyword in query_lower for keyword in billing_keywords):
            return "billing_urgent"
    
    # Standard routing
    if any(keyword in query_lower for keyword in billing_keywords):
        return "billing"
    elif any(keyword in query_lower for keyword in tech_keywords):
        return "technical"
    elif any(keyword in query_lower for keyword in sales_keywords):
        return "sales"
    else:
        return "general"

@function_tool
def route_customer_query(query: str, priority: str = "normal") -> str:
    """Custom routing logic for customer support queries"""
    return analyze_query(query, priority)

# Create main router agent with custom routing tool
router_agent = Agent(
    name="Customer Support Router",
    instructions="""You are a customer support router. Use the route_customer_query tool 
    to analyze customer requests and determine the best specialist to handle them.
    
    Based on the routing result:
    - "billing" or "billing_urgent" → Hand off to Billing Specialist
    - "technical" or "technical_urgent" → Hand off to Technical Support  
    - "sales" → Hand off to Sales Representative
    - "general" → Handle the query yourself
    
    For urgent issues, mention the priority when handing off.""",
    tools=[route_customer_query],
    handoffs=[billing_agent, technical_agent, sales_agent]
)

async def demo_custom_routing():
    """Demonstrate custom handoff routing logic"""
    
    test_queries = [
        ("My payment failed and I need help", "urgent"),
        ("I want to see a product demo", "normal"),
        ("The app keeps crashing on startup", "urgent"), 
        ("What are your business hours?", "normal"),
        ("I need a refund for my subscription", "normal"),
        ("How do I install the software?", "normal"),
        ("Can I upgrade my plan?", "normal")
    ]
    
    for query, priority in test_queries:
        print(f"\nQuery: {query} (Priority: {priority})")
        
        # First show what the routing tool would return
        route_result = analyze_query(query, priority)
        print(f"Routing Decision: {route_result}")
        
        # Then show the actual agent response
        result = await Runner.run(router_agent, f"Priority: {priority}. Customer query: {query}")
        print(f"Response: {result.final_output}")
        print("-" * 70)

if __name__ == "__main__":
    asyncio.run(demo_custom_routing())
