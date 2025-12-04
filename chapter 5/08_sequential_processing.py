"""Sequential Processing Example

This example demonstrates step-by-step agent workflows:
- Building linear workflows where each agent processes the previous agent's output
- Maintaining shared context and intermediate results across workflow stages
- Creating content pipelines (research → analysis → writing → editing)
- Tracking workflow progress and stage completion times

Perfect pattern for building content creation and document processing pipelines.

Usage:
    python 08_sequential_processing.py
"""

import asyncio
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any
from datetime import datetime
from agents import Agent, Runner

class WorkflowContext(BaseModel):
    model_config = ConfigDict(strict=True)
    
    workflow_id: str
    topic: str
    stage_results: Dict[str, str] = {}
    metadata: Dict[str, Any] = {}
    created_at: datetime
    
    def add_stage_result(self, agent_name: str, result: str):
        """Add result from a workflow stage"""
        self.stage_results[agent_name] = result
        self.metadata[f"{agent_name}_completed_at"] = datetime.now().isoformat()

# Create sequential workflow agents
research_agent = Agent(
    name="Research Agent",
    instructions="Research the given topic thoroughly. Provide key facts, statistics, and insights."
)

analysis_agent = Agent(
    name="Analysis Agent", 
    instructions="Analyze the research data. Identify patterns, trends, and key takeaways."
)

writer_agent = Agent(
    name="Writer Agent",
    instructions="Write a comprehensive article based on the research and analysis provided."
)

editor_agent = Agent(
    name="Editor Agent",
    instructions="Edit and polish the written content. Improve clarity, flow, and readability."
)

async def sequential_workflow(initial_input: str, context: WorkflowContext) -> str:
    """Sequential processing workflow - each agent waits for previous to complete"""
    
    agents = [research_agent, analysis_agent, writer_agent, editor_agent]
    current_input = initial_input
    
    print(f"🔄 SEQUENTIAL WORKFLOW: {context.workflow_id}")
    print(f"Topic: {context.topic}")
    print("=" * 60)
    
    for i, agent in enumerate(agents, 1):
        print(f"\n{i}️⃣ Processing with {agent.name}...")
        
        # Build context-aware prompt
        if i == 1:
            # First agent gets original input
            prompt = f"Research this topic: {current_input}"
        else:
            # Subsequent agents get previous results + context
            prompt = f"""
            Continue the workflow for topic: {context.topic}
            
            Previous stage results:
            {chr(10).join([f"- {name}: {result[:100]}..." for name, result in context.stage_results.items()])}
            
            Current input to process: {current_input}
            """
        
        # Execute agent (blocking - waits for completion)
        result = await Runner.run(agent, prompt)
        
        # Use this agent's output as input for the next
        current_input = result.final_output
        
        # Update shared context with intermediate results
        context.add_stage_result(agent.name, result.final_output)
        
        print(f"✅ Completed {agent.name}")
        print(f"Output preview: {current_input[:150]}...")
        print("-" * 40)
    
    print(f"\n🎉 SEQUENTIAL WORKFLOW COMPLETED")
    return current_input

async def demo_sequential():
    """Demonstrate sequential processing"""
    
    topics = [
        "Machine Learning in Finance",
        "Climate Change Solutions"
    ]
    
    for topic in topics:
        print(f"\n{'='*80}")
        print(f"SEQUENTIAL PROCESSING DEMO: {topic}")
        print("="*80)
        
        # Create workflow context
        context = WorkflowContext(
            workflow_id=f"SEQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            topic=topic,
            created_at=datetime.now()
        )
        
        # Run sequential workflow
        final_result = await sequential_workflow(topic, context)
        
        # Show workflow summary
        print(f"\n📋 WORKFLOW SUMMARY:")
        print(f"Workflow ID: {context.workflow_id}")
        print(f"Total Stages: {len(context.stage_results)}")
        print(f"Processing Order:")
        for i, (stage, _) in enumerate(context.stage_results.items(), 1):
            completion_time = context.metadata.get(f"{stage}_completed_at", "Unknown")
            print(f"  {i}. {stage} - Completed: {completion_time}")
        
        print(f"\n🎉 FINAL RESULT:")
        print(f"{final_result[:200]}...")

if __name__ == "__main__":
    asyncio.run(demo_sequential())
