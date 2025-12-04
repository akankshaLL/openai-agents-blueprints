"""Hybrid Orchestration Example

This example demonstrates combining AI intelligence with business rules:
- Building smart_routing_system that uses LLM decisions + programmatic overrides
- Creating router_agent for intelligent request categorization
- Implementing business rule overrides for critical priorities and escalations
- Balancing AI flexibility with deterministic business logic

Sophisticated pattern for building enterprise-grade agent orchestration systems.

Usage:
    python 06_hybrid_orchestration.py
"""

import asyncio
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional, List
from agents import Agent, Runner

class TaskContext(BaseModel):
    model_config = ConfigDict(strict=True)
    
    user_id: str
    priority: str
    category: str
    escalation_level: int = 0
    conversation_history: List[Dict[str, str]] = []

class RoutingDecision(BaseModel):
    model_config = ConfigDict(strict=True)
    
    agent_category: str
    confidence: float
    reasoning: str
    requires_escalation: bool = False

# Create specialized agents
support_agent = Agent(
    name="Support Agent",
    instructions="Handle general customer support inquiries with helpful responses."
)

technical_agent = Agent(
    name="Technical Agent", 
    instructions="Handle technical issues, bugs, and troubleshooting requests."
)

manager_agent = Agent(
    name="Manager Agent",
    instructions="Handle critical issues and complex customer problems requiring management attention."
)

escalation_agent = Agent(
    name="Escalation Agent",
    instructions="Handle escalated cases that have failed multiple resolution attempts."
)

# Smart router that makes LLM-based decisions
router_agent = Agent(
    name="Smart Router",
    instructions="""Analyze customer requests and route to appropriate agent category.
    
    Categories:
    - "support": General questions, account issues, basic help
    - "technical": Bugs, errors, installation problems
    - "manager": Complaints, refunds, complex issues
    - "escalation": Previously failed cases needing special attention
    
    Consider the user's tone, issue complexity, and urgency.""",
    output_type=RoutingDecision
)

def get_agent_by_category(category: str) -> Agent:
    """Map category to actual agent"""
    agent_map = {
        "support": support_agent,
        "technical": technical_agent, 
        "manager": manager_agent,
        "escalation": escalation_agent
    }
    return agent_map.get(category, support_agent)

async def smart_routing_system(user_input: str, context: TaskContext) -> str:
    """Hybrid orchestration: LLM intelligence + business rules"""
    
    print(f"🧠 HYBRID ORCHESTRATION")
    print(f"User: {context.user_id} | Priority: {context.priority} | Escalation: {context.escalation_level}")
    print(f"Input: {user_input}")
    
    # Step 1: Use LLM to categorize and route initially
    print("\n1️⃣ LLM-Based Routing Decision...")
    router_result = await Runner.run(
        router_agent,
        f"Route this request: {user_input}"
    )
    
    llm_decision = router_result.final_output
    print(f"LLM suggests: {llm_decision.agent_category} (confidence: {llm_decision.confidence:.2f})")
    print(f"Reasoning: {llm_decision.reasoning}")
    
    # Step 2: Apply business rules (programmatic override)
    print("\n2️⃣ Applying Business Rules...")
    
    if context.priority == "critical" and llm_decision.agent_category != "manager":
        # Override LLM decision for critical issues
        target_agent = manager_agent
        print("🚨 OVERRIDE: Critical priority → Manager Agent")
        
    elif context.escalation_level > 2:
        # Automatic escalation after multiple attempts
        target_agent = escalation_agent
        print("⬆️ OVERRIDE: High escalation level → Escalation Agent")
        
    elif llm_decision.requires_escalation:
        # LLM detected need for escalation
        target_agent = escalation_agent
        print("🤖 LLM ESCALATION: Detected escalation need → Escalation Agent")
        
    else:
        # Trust the LLM's routing decision
        target_agent = get_agent_by_category(llm_decision.agent_category)
        print(f"✅ FOLLOWING LLM: Using {llm_decision.agent_category} agent")
    
    # Step 3: Execute with the selected agent
    print(f"\n3️⃣ Executing with {target_agent.name}...")
    result = await Runner.run(target_agent, user_input)
    
    return result.final_output

async def demo_hybrid_orchestration():
    """Demonstrate hybrid orchestration scenarios"""
    
    test_scenarios = [
        {
            "input": "I can't log into my account",
            "context": TaskContext(
                user_id="user123",
                priority="normal", 
                category="support",
                escalation_level=0
            ),
            "description": "Normal support request - should follow LLM routing"
        },
        {
            "input": "The app crashed and I lost all my data!",
            "context": TaskContext(
                user_id="user456",
                priority="critical",
                category="technical", 
                escalation_level=0
            ),
            "description": "Critical issue - business rule should override to manager"
        },
        {
            "input": "This is my third time asking for help with the same problem",
            "context": TaskContext(
                user_id="user789",
                priority="normal",
                category="support",
                escalation_level=3
            ),
            "description": "High escalation level - should route to escalation agent"
        },
        {
            "input": "I want to cancel my subscription and get a full refund immediately",
            "context": TaskContext(
                user_id="user101",
                priority="normal",
                category="billing",
                escalation_level=0
            ),
            "description": "Complex request - LLM should detect need for manager"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*80}")
        print(f"SCENARIO {i}: {scenario['description']}")
        print("=" * 80)
        
        response = await smart_routing_system(scenario["input"], scenario["context"])
        
        print(f"\n🎯 Final Response: {response}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(demo_hybrid_orchestration())
