"""RunResult Monitoring Example

This example demonstrates production monitoring and analytics:
- Exporting conversation metrics for analytics dashboards
- Tracking token usage, tool usage, and performance metrics
- Building monitoring functions for production agent deployments
- Creating structured logs for debugging and optimization

Critical pattern for production agent monitoring and cost management.

Usage:
    python 08_runresult_monitoring.py
"""

import os
import json
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

def export_conversation_metrics(result, user_id=None):
    """Export conversation data for analytics and monitoring."""
    
    # Calculate token usage
    total_input = sum(r.usage.input_tokens for r in result.raw_responses)
    total_output = sum(r.usage.output_tokens for r in result.raw_responses)
    
    # Analyze tool usage
    tool_calls = [item for item in result.new_items if item.type == "tool_call_item"]
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "agent_name": result.last_agent.name,
        "conversation_length": len(result.to_input_list()),
        "tokens": {
            "input": total_input,
            "output": total_output,
            "total": total_input + total_output
        },
        "tool_usage": {
            "tools_called": len(tool_calls),
            "total_items": len(result.new_items)
        },
        "response_preview": result.final_output[:100] + "..." if len(result.final_output) > 100 else result.final_output
    }
    
    return metrics

# Usage example
async def monitored_conversation():
    agent = Agent(name="MonitoredAgent", instructions="Be helpful")
    result = await Runner.run(agent, "Hello!")
    
    metrics = export_conversation_metrics(result, user_id="user_123")
    print(json.dumps(metrics, indent=2))

async def main():
    print("📊 RunResult Monitoring Demo")
    print("=" * 40)
    print("This demo shows how to export conversation metrics")
    print("for analytics and monitoring purposes.\n")
    
    await monitored_conversation()
    
    print(f"\n{'='*40}")
    print("Demo completed! The metrics above show:")
    print("- Token usage breakdown")
    print("- Tool usage statistics")
    print("- Conversation metadata")
    print("- Response preview")

if __name__ == "__main__":
    asyncio.run(main())
