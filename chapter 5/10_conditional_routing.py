"""Conditional Routing Example

This example demonstrates dynamic workflow routing based on processing outcomes:
- Using agent responses to determine next workflow steps
- Building decision trees with multiple routing paths
- Handling different confidence levels and error conditions
- Creating adaptive workflows that respond to processing results

Advanced pattern for building intelligent, self-adapting agent workflows.

Usage:
    python 10_conditional_routing.py
"""

import asyncio
from typing import Dict, Any
from datetime import datetime
from agents import Agent, Runner

class ProcessingContext:
    def __init__(self, request_id: str, user_type: str, priority: str):
        self.request_id = request_id
        self.user_type = user_type
        self.priority = priority
        self.routing_history = []
        self.created_at = datetime.now()

# Create specialized agents for different routing paths
processor_agent = Agent(
    name="Processor Agent",
    instructions="""Analyze the input and provide a routing decision.
    
    Respond with one of these outcomes based on the request:
    - "SUCCESS_HIGH" for simple requests you can handle with high confidence
    - "SUCCESS_MEDIUM" for requests you can handle but with some uncertainty
    - "NEEDS_REVIEW" for ambiguous requests requiring human review
    - "REQUIRES_ESCALATION" for complex or critical issues
    - "ERROR" for malformed or invalid requests
    
    Start your response with the outcome, then explain your reasoning."""
)

finalizer_agent = Agent(
    name="Finalizer Agent",
    instructions="Finalize successful processing results. Provide polished final output."
)

reviewer_agent = Agent(
    name="Reviewer Agent", 
    instructions="Review uncertain results. Provide quality assessment and improvements."
)

human_review_agent = Agent(
    name="Human Review Agent",
    instructions="Handle cases requiring human review. Provide detailed analysis for human oversight."
)

supervisor_agent = Agent(
    name="Supervisor Agent",
    instructions="Handle escalated cases. Provide management-level resolution."
)

error_handler_agent = Agent(
    name="Error Handler Agent",
    instructions="Handle processing errors. Provide error analysis and recovery options."
)

async def conditional_workflow(input_data: str, context: ProcessingContext) -> str:
    """Conditional routing workflow based on processing outcomes"""
    
    print(f"🔀 CONDITIONAL ROUTING WORKFLOW")
    print(f"Request ID: {context.request_id}")
    print(f"Input: {input_data}")
    print("=" * 60)
    
    # Step 1: Initial processing
    print("1️⃣ Initial Processing...")
    context.routing_history.append("Started with Processor Agent")
    
    result = await Runner.run(processor_agent, f"Process this request: {input_data}")
    processor_response = result.final_output
    
    print(f"Processor response: {processor_response[:100]}...")
    
    # Extract outcome from response
    outcome = "SUCCESS_MEDIUM"  # Default
    if "SUCCESS_HIGH" in processor_response:
        outcome = "SUCCESS_HIGH"
    elif "SUCCESS_MEDIUM" in processor_response:
        outcome = "SUCCESS_MEDIUM"
    elif "NEEDS_REVIEW" in processor_response:
        outcome = "NEEDS_REVIEW"
    elif "REQUIRES_ESCALATION" in processor_response:
        outcome = "REQUIRES_ESCALATION"
    elif "ERROR" in processor_response:
        outcome = "ERROR"
    
    # Step 2: Route based on outcome
    print(f"\n2️⃣ Conditional Routing: {outcome}")
    
    if outcome == "SUCCESS_HIGH":
        # High confidence - go directly to finalization
        print("🎯 HIGH CONFIDENCE → Direct to Finalizer")
        context.routing_history.append("Routed to Finalizer (high confidence)")
        final_result = await Runner.run(finalizer_agent, f"Finalize this request: {input_data}")
        
    elif outcome == "SUCCESS_MEDIUM":
        # Medium confidence - get review first
        print("🔍 MEDIUM CONFIDENCE → Review then Finalize")
        context.routing_history.append("Routed to Reviewer (medium confidence)")
        review_result = await Runner.run(reviewer_agent, f"Review this request: {input_data}")
        
        context.routing_history.append("Reviewed, now finalizing")
        final_result = await Runner.run(finalizer_agent, f"Finalize reviewed content: {review_result.final_output}")
    
    elif outcome == "NEEDS_REVIEW":
        # Send to human review agent
        print("👤 NEEDS REVIEW → Human Review Agent")
        context.routing_history.append("Routed to Human Review Agent")
        final_result = await Runner.run(human_review_agent, f"Human review needed for: {input_data}")
    
    elif outcome == "REQUIRES_ESCALATION":
        # Escalate to supervisor
        print("⬆️ ESCALATION → Supervisor Agent")
        context.routing_history.append("Escalated to Supervisor Agent")
        final_result = await Runner.run(supervisor_agent, f"Escalated case: {input_data}")
    
    else:  # ERROR
        # Send to error handling agent
        print("❌ ERROR → Error Handler Agent")
        context.routing_history.append("Error handling triggered")
        final_result = await Runner.run(error_handler_agent, f"Handle error in request: {input_data}")
    
    return final_result.final_output

async def demo_conditional_routing():
    """Demonstrate conditional routing with different scenarios"""
    
    test_scenarios = [
        {
            "input": "Please help me reset my password",
            "context": ProcessingContext("REQ-001", "standard", "normal"),
            "description": "Simple request - should succeed with high confidence"
        },
        {
            "input": "I need help with a complex integration issue involving multiple APIs",
            "context": ProcessingContext("REQ-002", "enterprise", "high"),
            "description": "Complex request - may need review or escalation"
        },
        {
            "input": "The system crashed and I lost all my data, this is urgent!",
            "context": ProcessingContext("REQ-003", "premium", "critical"),
            "description": "Critical issue - likely requires escalation"
        },
        {
            "input": "Invalid request with malformed data @#$%^&*()",
            "context": ProcessingContext("REQ-004", "unknown", "low"),
            "description": "Malformed request - should trigger error handling"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'='*80}")
        print(f"SCENARIO: {scenario['description']}")
        print("="*80)
        
        final_response = await conditional_workflow(scenario["input"], scenario["context"])
        
        print(f"\n📋 ROUTING SUMMARY:")
        print(f"Request ID: {scenario['context'].request_id}")
        print(f"Routing Path:")
        for i, step in enumerate(scenario["context"].routing_history, 1):
            print(f"  {i}. {step}")
        
        print(f"\n🎯 FINAL RESPONSE:")
        print(f"{final_response}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(demo_conditional_routing())
