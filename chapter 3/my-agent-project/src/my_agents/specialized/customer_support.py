# src/agents/specialized/customer_support.py
from typing import Optional
from pydantic import BaseModel

from agents import function_tool
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from src.my_agents.base import BaseAgent
from src.utils.logging import setup_logger
from src.my_agents.specialized.guardrails import content_safety_guardrail

logger = setup_logger(__name__)

class CustomerQuery(BaseModel):
    """Structure for customer support query responses."""
    response: str
    sentiment: str
    follow_up_needed: bool

def _get_product_info_impl(product_id: str) -> str:
    """Internal implementation for getting product information."""
    # In a real application, this would query a database or API
    logger.info(f"Getting product info for {product_id}")
    return f"Product {product_id}: This is a sample product description with detailed specifications and features."

@function_tool
def get_product_info(product_id: str) -> str:
    """Get information about a product."""
    return _get_product_info_impl(product_id)

class CustomerSupportAgent(BaseAgent[CustomerQuery]):
    """An agent specialized for customer support tasks."""
    
    def __init__(
        self,
        name: str = "Customer Support",
        instructions: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        default_instructions = f"""
        {RECOMMENDED_PROMPT_PREFIX}
        
        You are a helpful customer support agent. Your goal is to assist customers
        with their questions and concerns in a friendly and professional manner.
        
        When responding to customers:
        1. Be empathetic and understanding
        2. Provide clear and concise information
        3. Use the tools available to look up product information when needed
        4. Handle general inquiries, billing questions, order status, and account issues
        5. Indicate whether follow-up is needed for complex issues
        
        Focus on:
        - Order management and tracking
        - Billing and payment issues
        - Account management
        - General product information
        - Returns and refunds
        """
        
        super().__init__(
            name=name,
            instructions=instructions or default_instructions,
            model=model,
            temperature=temperature,
            tools=[get_product_info],
            output_type=CustomerQuery,
        )
        # Add the content safety guardrail
        self.agent.input_guardrails = [content_safety_guardrail]
