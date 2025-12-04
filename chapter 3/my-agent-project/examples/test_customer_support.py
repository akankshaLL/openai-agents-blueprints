#!/usr/bin/env python3
"""Test customer support handoff workflow."""

import asyncio
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add src to path for development
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from agents import Runner
from my_agents.specialized.multi_agent_workflow import SupportTriageAgent
from utils.logging import app_logger

# Load environment variables
load_dotenv()

async def main():
    """Test customer support workflow."""
    app_logger.info("Testing Customer Support Workflow")
    
    # Create the support triage agent
    triage_agent = SupportTriageAgent()
    
    # Test with a customer support query (billing/order)
    user_query = "I was charged twice for my order last month and need a refund. My order number is #12345."
    app_logger.info(f"User query: {user_query}")
    
    try:
        # Run the triage agent
        result = await Runner.run(
            triage_agent.agent,
            user_query,
            run_config=triage_agent.get_run_config(),
        )
        
        # Process the result
        app_logger.info(f"Final result: {result.final_output}")
        app_logger.info(f"Last agent: {result.last_agent.name}")
        
        app_logger.info("Customer support workflow completed successfully!")
        
    except Exception as e:
        app_logger.error(f"Error in customer support workflow: {e}")
        import traceback
        app_logger.error(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(main())
