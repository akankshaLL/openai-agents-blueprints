# src/agents/base.py
from typing import List, Optional, Type, TypeVar, Generic
from pydantic import BaseModel

from agents import Agent, ModelSettings
from agents.run import RunConfig

from src.config.settings import settings

T = TypeVar('T')

class BaseAgent(Generic[T]):
    """Base class for all agents in the application."""
    
    def __init__(
        self,
        name: str,
        instructions: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        tools: Optional[List] = None,
        output_type: Optional[Type[BaseModel]] = None,
        handoffs: Optional[List] = None,
    ):
        self.name = name
        self.instructions = instructions
        self.model = model or settings.default_model
        self.temperature = temperature or settings.default_temperature
        self.tools = tools or []
        self.output_type = output_type
        self.handoffs = handoffs or []
        
        # Create the agent instance - handoffs are passed separately, not combined with tools
        self.agent = Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model,
            model_settings=ModelSettings(temperature=self.temperature),
            tools=self.tools,
            handoffs=self.handoffs,  # Pass handoffs separately
            output_type=self.output_type,
        )
    
    def get_run_config(self) -> RunConfig:
        """Get the run configuration for this agent."""
        return RunConfig(
            workflow_name=settings.trace_workflow_name,
            tracing_disabled=not settings.enable_tracing,
        )
