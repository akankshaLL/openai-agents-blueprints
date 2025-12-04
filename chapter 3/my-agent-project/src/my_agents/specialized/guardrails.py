# src/agents/specialized/guardrails.py
from pydantic import BaseModel
from typing import Optional

from agents import (
    Agent, 
    GuardrailFunctionOutput, 
    RunContextWrapper, 
    Runner,
    input_guardrail,
)

from src.utils.logging import setup_logger

logger = setup_logger(__name__)

class ContentSafetyOutput(BaseModel):
    """Output from the content safety guardrail."""
    is_safe: bool
    reasoning: str

# Create a guardrail agent to check content safety
content_safety_agent = Agent(
    name="Content Safety",
    instructions="""
    You are a content safety checker. Your job is to determine if the user's input
    contains any harmful, offensive, or inappropriate content. This includes:
    
    1. Hate speech or discriminatory language
    2. Explicit sexual content
    3. Violence or threats
    4. Personal attacks or harassment
    5. Requests for illegal activities
    
    Analyze the input carefully and determine if it's safe.
    """,
    output_type=ContentSafetyOutput,
)

@input_guardrail
async def content_safety_guardrail(
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    input_data: str
) -> GuardrailFunctionOutput:
    """Guardrail to check if user input is safe and appropriate."""
    logger.info("Running content safety guardrail")
    
    result = await Runner.run(content_safety_agent, input_data, context=ctx.context)
    safety_result = result.final_output
    
    return GuardrailFunctionOutput(
        output_info=safety_result,
        tripwire_triggered=not safety_result.is_safe,
    )
