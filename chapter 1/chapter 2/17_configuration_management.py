"""Configuration Management Example

This example demonstrates environment-specific agent configuration:
- Building AgentConfig dataclasses for different deployment environments
- Creating factory patterns for environment-specific agent creation
- Managing model settings, timeouts, and cost limits per environment
- Production-ready configuration management patterns

Critical pattern for deploying agents across development, staging, and production.

Usage:
    python 17_configuration_management.py
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

@dataclass
class AgentConfig:
    """Configuration for agent deployment environments."""
    model: str
    temperature: float
    max_tokens: int
    timeout: float
    enable_tracing: bool
    cost_limit_per_request: float

class ConfiguredAgentFactory:
    """Factory for creating environment-specific agents."""
    
    @staticmethod
    def get_config(environment: str = "production") -> AgentConfig:
        """Get configuration for specific environment."""
        
        configs = {
            "development": AgentConfig(
                model="gpt-4o-mini",      # Faster/cheaper for dev
                temperature=0.7,
                max_tokens=1000,
                timeout=30.0,
                enable_tracing=True,      # Detailed tracing in dev
                cost_limit_per_request=0.01
            ),
            "staging": AgentConfig(
                model="gpt-4o",
                temperature=0.5,
                max_tokens=1500,
                timeout=45.0,
                enable_tracing=True,
                cost_limit_per_request=0.05
            ),
            "production": AgentConfig(
                model="gpt-4o",
                temperature=0.3,          # More consistent in prod
                max_tokens=2000,
                timeout=60.0,
                enable_tracing=False,     # Reduced overhead in prod
                cost_limit_per_request=0.10
            )
        }
        
        return configs.get(environment, configs["production"])
    
    @staticmethod
    def create_agent(name: str, instructions: str, environment: str = None) -> Agent:
        """Create an agent configured for the specified environment."""
        
        env = environment or os.getenv("ENVIRONMENT", "production")
        config = ConfiguredAgentFactory.get_config(env)
        
        return Agent(
            name=name,
            instructions=instructions,
            model=config.model,
            model_settings=ModelSettings(
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
        )

# Usage
agent = ConfiguredAgentFactory.create_agent(
    name="ProductionAgent",
    instructions="You are a professional customer service agent.",
    environment=os.getenv("ENVIRONMENT", "production")
)

# Run the agent with a sample prompt
if __name__ == "__main__":
    prompt = "How can I update my account information?"
    result = Runner.run_sync(agent, prompt)
    print(f"Agent response: {result.final_output}")
