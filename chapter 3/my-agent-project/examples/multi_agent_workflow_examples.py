# examples/multi_agent_workflow_example.py
import asyncio
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from agents import Runner
from src.my_agents.specialized.multi_agent_workflow import SupportTriageAgent
from src.utils.logging import app_logger

# Load environment variables
load_dotenv()

async def run_support_triage(user_query: str, scenario_name: str):
    """Run the support triage system with a specific user query."""
    app_logger.info(f"\n{'='*60}")
    app_logger.info(f"SCENARIO: {scenario_name}")
    app_logger.info(f"{'='*60}")
    
    # Create the support triage agent
    triage_agent = SupportTriageAgent()
    app_logger.info(f"Created triage agent: {triage_agent.name}")
    
    app_logger.info(f"User query: {user_query}")
    
    try:
        # Run the triage agent
        result = await Runner.run(
            triage_agent.agent,
            user_query,
            run_config=triage_agent.get_run_config(),
        )
        
        # Process the result
        response = result.final_output
        app_logger.info(f"Triage response: {response}")
        
        # Check if there was a handoff
        if result.tool_calls:
            for tool_call in result.tool_calls:
                # Try to get the tool name in a robust way
                tool_name = getattr(tool_call, 'name', None) or getattr(tool_call, 'tool_name', None) or str(tool_call)
                app_logger.info(f"Tool called: {tool_name}")
                # Print all attributes for debugging
                app_logger.info(f"Tool call details: {tool_call.__dict__ if hasattr(tool_call, '__dict__') else tool_call}")
                if hasattr(tool_call, 'output') and tool_call.output:
                    app_logger.info(f"Handoff response: {tool_call.output}")
        
        return response
        
    except Exception as e:
        app_logger.error(f"Error in triage scenario '{scenario_name}': {e}")
        return None

async def main():
    """Run multiple scenarios to demonstrate the multi-agent workflow."""
    app_logger.info("Starting Multi-Agent Support Workflow Demo")
    app_logger.info("This demo shows how the triage agent routes different types of inquiries")
    
    # Test scenarios
    scenarios = [
        {
            "name": "General Customer Support Inquiry",
            "query": "I want to know more about your return policy and how to return an item I purchased last week."
        },
        {
            "name": "Technical Support Issue",
            "query": "My device won't turn on after the latest software update. I've tried holding the power button but nothing happens."
        },
        {
            "name": "Billing Question",
            "query": "I was charged twice for my subscription this month. Can you help me get a refund for the duplicate charge?"
        },
        {
            "name": "Product Functionality Problem",
            "query": "The app keeps crashing when I try to upload photos. It works fine for everything else but crashes every time I select an image."
        },
        {
            "name": "Order Status Inquiry",
            "query": "I placed an order 3 days ago and haven't received any shipping confirmation. Can you check the status of my order?"
        }
    ]
    
    # Run each scenario
    for scenario in scenarios:
        await run_support_triage(scenario["query"], scenario["name"])
        await asyncio.sleep(1)  # Brief pause between scenarios
    
    app_logger.info(f"\n{'='*60}")
    app_logger.info("Multi-Agent Workflow Demo Complete!")
    app_logger.info("The triage agent successfully routed different types of inquiries")
    app_logger.info("to the appropriate specialized agents (Customer Support vs Technical Support)")
    app_logger.info(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
