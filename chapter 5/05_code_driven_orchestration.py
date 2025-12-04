"""Code-Driven Orchestration Example

This example demonstrates deterministic multi-agent workflows:
- Using structured outputs to control workflow routing
- Building deterministic agent pipelines with explicit control flow
- Error handling and validation at each workflow step
- Sequential processing with structured data passing between agents

Powerful pattern for building reliable, predictable multi-agent systems.

Usage:
    python 05_code_driven_orchestration.py
"""

import asyncio
import json
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from agents import Agent, Runner

class ProcessingResult(BaseModel):
    model_config = ConfigDict(strict=True)
    
    success: bool
    data: Dict[str, Any]
    next_agent: str
    error_message: Optional[str] = None

# Create workflow agents
data_collector_agent = Agent(
    name="Data Collector",
    instructions="""You collect and validate input data. 
    
    Return:
    - success: true if data is valid
    - data: processed/cleaned data
    - next_agent: "analyzer" if data is complete, "error" if invalid
    - error_message: if validation fails""",
    output_type=ProcessingResult    
)

analyzer_agent = Agent(
    name="Data Analyzer", 
    instructions="""You analyze collected data and generate insights.
    
    Return:
    - success: true if analysis completes
    - data: analysis results and insights
    - next_agent: "reporter" if analysis successful, "error" if failed
    - error_message: if analysis fails""",
    output_type=ProcessingResult
)

reporter_agent = Agent(
    name="Report Generator",
    instructions="""You generate final reports from analyzed data.
    
    Return:
    - success: true if report generated
    - data: final report content
    - next_agent: "complete" when finished
    - error_message: if report generation fails""",
    output_type=ProcessingResult
)

async def orchestrate_workflow(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Orchestrate deterministic workflow through multiple agents"""
    
    current_agent = data_collector_agent
    context = input_data.copy()
    step = 1
    
    print("🔄 STARTING CODE-DRIVEN ORCHESTRATION")
    print("=" * 50)
    
    while current_agent:
        agent_name = current_agent.name
        print(f"\nStep {step}: {agent_name}")
        print(f"Input context: {json.dumps(context, indent=2)}")
        
        # Run current agent with structured output
        result = await Runner.run(
            current_agent,
            f"Process this data: {json.dumps(context)}"
        )
        
        processing_result = result.final_output
        print(f"Agent result: {processing_result}")
        
        # Check for errors
        if not processing_result.success:
            print(f"❌ Workflow failed at {agent_name}: {processing_result.error_message}")
            raise Exception(f"Processing failed: {processing_result.error_message}")
        
        # Update context with new data
        context.update(processing_result.data)
        
        # Determine next agent based on structured output
        next_agent_name = processing_result.next_agent
        
        if next_agent_name == "analyzer":
            current_agent = analyzer_agent
        elif next_agent_name == "reporter":
            current_agent = reporter_agent
        elif next_agent_name == "complete":
            current_agent = None  # End workflow
        elif next_agent_name == "error":
            raise Exception(f"Agent {agent_name} indicated error: {processing_result.error_message}")
        else:
            raise Exception(f"Unknown next agent: {next_agent_name}")
        
        step += 1
        print("-" * 30)
    
    print("\n✅ WORKFLOW COMPLETED SUCCESSFULLY")
    return context

async def demo_orchestration():
    """Demonstrate code-driven orchestration"""
    
    test_scenarios = [
        {
            "name": "Valid Customer Data",
            "input": {
                "customer_id": "12345",
                "purchase_amount": 299.99,
                "product": "Premium Software License",
                "date": "2024-01-15"
            }
        },
        {
            "name": "Invalid Data (Missing Fields)",
            "input": {
                "customer_id": "67890",
                "product": "Basic License"
                # Missing amount and date
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'='*60}")
        print(f"Testing Scenario: {scenario['name']}")
        print(f"Input: {scenario['input']}")
        print("=" * 60)
        
        try:
            final_result = await orchestrate_workflow(scenario["input"])
            print(f"\n🎉 Final Result:")
            print(json.dumps(final_result, indent=2))
            
        except Exception as e:
            print(f"\n💥 Workflow Error: {str(e)}")

# Alternative: Simple Sequential Processing
async def simple_sequential_workflow(data: Dict[str, Any]) -> str:
    """Simple sequential processing without complex orchestration"""
    
    print("\n🔗 SIMPLE SEQUENTIAL WORKFLOW")
    
    # Step 1: Collect
    step1 = await Runner.run(data_collector_agent, f"Validate: {json.dumps(data)}")
    if not step1.final_output.success:
        return f"Failed at collection: {step1.final_output.error_message}"
    
    # Step 2: Analyze  
    step2 = await Runner.run(analyzer_agent, f"Analyze: {json.dumps(step1.final_output.data)}")
    if not step2.final_output.success:
        return f"Failed at analysis: {step2.final_output.error_message}"
    
    # Step 3: Report
    step3 = await Runner.run(reporter_agent, f"Report: {json.dumps(step2.final_output.data)}")
    if not step3.final_output.success:
        return f"Failed at reporting: {step3.final_output.error_message}"
    
    return f"Sequential workflow completed: {step3.final_output.data}"

if __name__ == "__main__":
    asyncio.run(demo_orchestration())
