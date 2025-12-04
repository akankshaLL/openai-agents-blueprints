"""Model Settings Configuration Example

This example demonstrates fine-tuning agent behavior with ModelSettings:
- Configuring temperature, top_p, and token limits for different use cases
- Creative vs analytical vs conversational agent configurations
- Understanding how model parameters affect agent responses
- Optimizing for cost, speed, and quality based on application needs

Essential for building production agents with predictable, optimized behavior.

Usage:
    python 02_model_settings.py
"""

from agents import Agent, ModelSettings

# Configuration for creative tasks
creative_agent = Agent(
    name="CreativeWriter",
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.8,        # Higher creativity and variation
        top_p=0.9,             # Consider top 90% of probability mass
        max_tokens=1500,       # Allow longer responses
        frequency_penalty=0.1,  # Slight penalty for repetition
        presence_penalty=0.1    # Encourage diverse vocabulary
    ),
    instructions="You are a creative writer specializing in engaging narratives."
)

# Configuration for analytical tasks
analytical_agent = Agent(
    name="DataAnalyst", 
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.1,        # Low creativity, high consistency
        top_p=0.5,             # More focused probability distribution
        max_tokens=800,        # Concise responses
        frequency_penalty=0.0,  # No repetition penalty
        presence_penalty=0.0    # No vocabulary diversity pressure
    ),
    instructions="You are a data analyst providing accurate, objective analysis."
)

# Configuration for conversational agents
conversational_agent = Agent(
    name="ChatAgent",
    model="gpt-4o-mini",      # Faster, more cost-effective for chat
    model_settings=ModelSettings(
        temperature=0.5,        # Balanced creativity and consistency
        top_p=0.8,             # Good balance of variety and focus
        max_tokens=300         # Shorter responses for chat
    ),
    instructions="You are a friendly, conversational assistant."
)
