"""Shared Context Pattern Example

This example demonstrates maintaining shared state across multiple agents:
- Using Pydantic models to represent shared business objects (support tickets)
- Passing context between agents while preserving state changes
- Building workflows where agents collaborate on the same data object
- Tracking escalation history and resolution notes across agent handoffs

Powerful pattern for building collaborative agent systems with persistent state.

Usage:
    python 07_shared_context_pattern.py
"""

import asyncio
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from agents import Agent, Runner

class SupportTicket(BaseModel):
    model_config = ConfigDict(strict=True)
    
    ticket_id: str
    customer_id: str
    issue_type: str
    priority: str
    status: str
    description: str
    resolution_notes: List[str] = []
    escalation_history: List[str] = []
    escalation_level: int = 0
    created_at: datetime
    updated_at: datetime
    
    def add_note(self, agent_name: str, note: str):
        """Add resolution note from agent"""
        self.resolution_notes.append(f"[{agent_name}] {note}")
        self.updated_at = datetime.now()
    
    def escalate_to(self, agent_name: str, reason: str):
        """Escalate ticket to another agent"""
        self.escalation_history.append(f"Escalated to {agent_name}: {reason}")
        self.escalation_level += 1
        self.updated_at = datetime.now()

# Create specialized agents
tier1_agent = Agent(
    name="Tier 1 Support",
    instructions="Handle basic support issues. Add notes to ticket and escalate complex issues."
)

billing_agent = Agent(
    name="Billing Specialist", 
    instructions="Handle billing, payment, and subscription issues. Update ticket with resolution."
)

technical_agent = Agent(
    name="Technical Support",
    instructions="Handle technical issues, bugs, and troubleshooting. Document solutions in ticket."
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""Categorize support tickets and route to appropriate specialists.
    
    Update ticket status and add assessment notes. Route based on issue type:
    - Basic issues → Tier 1 Support
    - Billing/payment → Billing Specialist  
    - Technical/bugs → Technical Support""",
    handoffs=[tier1_agent, billing_agent, technical_agent]
)

async def process_ticket_with_context(ticket: SupportTicket) -> SupportTicket:
    """Process ticket through agents while maintaining shared context"""
    print(f"Customer: {ticket.customer_id} | Priority: {ticket.priority}")
    print(f"Issue: {ticket.description}")
    print("-" * 60)
    
    # Step 1: Triage assessment
    print("1️⃣ Triage Assessment...")
    ticket.add_note("System", "Ticket created and assigned to triage")
    
    triage_prompt = f"""
    Analyze this support ticket:
    
    Ticket ID: {ticket.ticket_id}
    Customer: {ticket.customer_id}
    Issue Type: {ticket.issue_type}
    Priority: {ticket.priority}
    Description: {ticket.description}
    
    Provide assessment and routing recommendation.
    """
    
    triage_result = await Runner.run(triage_agent, triage_prompt)
    ticket.add_note("Triage Agent", f"Assessment: {triage_result.final_output}")
    
    # Step 2: Route to specialist based on issue type
    print("2️⃣ Routing to Specialist...")
    
    if "billing" in ticket.issue_type.lower() or "payment" in ticket.description.lower():
        specialist = billing_agent
        ticket.escalate_to("Billing Specialist", "Billing-related issue detected")
    elif "technical" in ticket.issue_type.lower() or "bug" in ticket.description.lower():
        specialist = technical_agent  
        ticket.escalate_to("Technical Support", "Technical issue detected")
    else:
        specialist = tier1_agent
        ticket.escalate_to("Tier 1 Support", "General support issue")
    
    # Step 3: Specialist handles the ticket
    print(f"3️⃣ {specialist.name} Processing...")
    
    specialist_prompt = f"""
    Handle this support ticket with full context:
    
    Ticket Details:
    - ID: {ticket.ticket_id}
    - Customer: {ticket.customer_id}  
    - Issue: {ticket.description}
    - Priority: {ticket.priority}
    
    Previous Notes:
    {chr(10).join(ticket.resolution_notes)}
    
    Escalation History:
    {chr(10).join(ticket.escalation_history)}
    
    Provide resolution and update ticket status.
    """
    
    specialist_result = await Runner.run(specialist, specialist_prompt)
    ticket.add_note(specialist.name, f"Resolution: {specialist_result.final_output}")
    ticket.status = "resolved"
    
    return ticket

async def demo_shared_context():
    """Demonstrate shared context pattern with multiple tickets"""
    
    # Create test tickets
    tickets = [
        SupportTicket(
            ticket_id="TKT-001",
            customer_id="CUST-123",
            issue_type="billing",
            priority="high", 
            status="open",
            description="My credit card was charged twice for the same subscription",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SupportTicket(
            ticket_id="TKT-002", 
            customer_id="CUST-456",
            issue_type="technical",
            priority="medium",
            status="open", 
            description="The mobile app crashes when I try to upload photos",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SupportTicket(
            ticket_id="TKT-003",
            customer_id="CUST-789", 
            issue_type="general",
            priority="low",
            status="open",
            description="How do I change my password?",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    
    # Process each ticket
    for ticket in tickets:
        print(f"\n{'='*80}")
        processed_ticket = await process_ticket_with_context(ticket)
        
        print(f"\n📋 FINAL TICKET STATE:")
        print(f"Status: {processed_ticket.status}")
        print(f"Escalation Level: {processed_ticket.escalation_level}")
        print(f"Resolution Notes:")
        for note in processed_ticket.resolution_notes:
            print(f"  • {note}")
        print(f"Escalation History:")
        for escalation in processed_ticket.escalation_history:
            print(f"  • {escalation}")

if __name__ == "__main__":
