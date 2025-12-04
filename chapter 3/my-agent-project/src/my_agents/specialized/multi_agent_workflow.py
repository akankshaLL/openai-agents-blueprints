# src/agents/specialized/multi_agent_workflow.py
from typing import Optional
from agents import Agent, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from src.my_agents.base import BaseAgent
from src.my_agents.specialized.customer_support import CustomerSupportAgent
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

class TechnicalSupportAgent(BaseAgent):
    """An agent specialized for technical support."""
    
    def __init__(
        self,
        name: str = "Technical Support",
        instructions: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        default_instructions = f"""
        {RECOMMENDED_PROMPT_PREFIX}
        
        You are a technical support specialist. Your goal is to help customers
        resolve technical issues with their products. Provide detailed, step-by-step
        instructions and troubleshooting advice.
        
        Focus on:
        - Hardware troubleshooting
        - Software issues and bugs
        - Configuration problems
        - Performance optimization
        """
        
        super().__init__(
            name=name,
            instructions=instructions or default_instructions,
            model=model,
            temperature=temperature,
        )

class SupportTriageAgent(BaseAgent):
    """An agent that triages customer support requests."""
    
    def __init__(
        self,
        name: str = "Support Triage",
        instructions: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        # Create the specialized agents first
        customer_support = CustomerSupportAgent()
        technical_support = TechnicalSupportAgent()
        
        default_instructions = f"""
        {RECOMMENDED_PROMPT_PREFIX}
        
        You are a support triage agent. Your job is to determine whether a customer
        inquiry should be handled by general customer support or technical support.
        
        Classification guidelines:
        - For general inquiries, product information, orders, billing, and account issues: 
          transfer to Customer Support
        - For technical issues, troubleshooting, software problems, and product functionality: 
          transfer to Technical Support
        
        Analyze the customer's message carefully to determine the most appropriate team.
        Always transfer to the appropriate specialist rather than trying to handle the request yourself.
        """
        
        # Create handoffs using the correct pattern
        handoffs = [
            handoff(
                customer_support.agent,
                tool_name_override="transfer_to_customer_support",
                tool_description_override="Transfer this conversation to the Customer Support team for general inquiries, billing, orders, and account issues.",
            ),
            handoff(
                technical_support.agent,
                tool_name_override="transfer_to_technical_support",
                tool_description_override="Transfer this conversation to the Technical Support team for technical issues, troubleshooting, and product functionality problems.",
            )
        ]
        
        super().__init__(
            name=name,
            instructions=instructions or default_instructions,
            model=model,
            temperature=temperature,
            handoffs=handoffs,
        )
