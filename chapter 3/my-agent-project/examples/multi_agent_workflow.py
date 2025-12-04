# examples/customer_support_example.py
import asyncio
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from agents import Runner
from src.my_agents.specialized.customer_support import CustomerSupportAgent
from src.utils.logging import app_logger

# Load environment variables
load_dotenv()

async def main():
    # Create the customer support agent
    agent = CustomerSupportAgent()
    app_logger.info(f"Created agent: {agent.name}")
    
    # Run the agent with a user query
    user_query = "I'm having trouble with my recent purchase of product XYZ789. Can you help me?"
    app_logger.info(f"User query: {user_query}")
    
    result = await Runner.run(
        agent.agent,
        user_query,
        run_config=agent.get_run_config(),
    )
    
    # Process the result
    response = result.final_output
    app_logger.info(f"Agent response: {response.response}")
    app_logger.info(f"Sentiment: {response.sentiment}")
    app_logger.info(f"Follow-up needed: {response.follow_up_needed}")
    
    return response

if __name__ == "__main__":
    asyncio.run(main())
