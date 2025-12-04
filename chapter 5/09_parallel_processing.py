"""Parallel Processing Example

This example demonstrates concurrent multi-agent execution:
- Running multiple agents simultaneously with asyncio.gather()
- Performance comparison between sequential and parallel execution
- Managing parallel agent workflows with proper error handling
- Optimizing multi-agent systems for speed and efficiency

Essential pattern for building high-performance multi-agent applications.

Usage:
    python 09_parallel_processing.py
"""

import asyncio
import time
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any
from datetime import datetime
from agents import Agent, Runner

class ParallelContext(BaseModel):
    model_config = ConfigDict(strict=True)
    
    workflow_id: str
    topic: str
    parallel_results: Dict[str, str] = {}
    execution_times: Dict[str, float] = {}
    created_at: datetime
    
    def add_result(self, agent_name: str, result: str, execution_time: float):
        """Add result from parallel execution"""
        self.parallel_results[agent_name] = result
        self.execution_times[agent_name] = execution_time

async def parallel_workflow(topic: str, context: ParallelContext) -> Dict[str, str]:
    """Parallel processing - agents work simultaneously"""
    
    print(f"⚡ PARALLEL WORKFLOW: {context.workflow_id}")
    print(f"Topic: {topic}")
    print("=" * 60)
    
    # Create specialized research agents for parallel execution
    market_researcher = Agent(
        name="Market Researcher",
        instructions="Research market trends, statistics, and business aspects of the topic."
    )
    
    tech_researcher = Agent(
        name="Tech Researcher", 
        instructions="Research technical aspects, innovations, and developments related to the topic."
    )
    
    social_researcher = Agent(
        name="Social Researcher",
        instructions="Research social impact, user behavior, and cultural aspects of the topic."
    )
    
    competitive_researcher = Agent(
        name="Competitive Researcher",
        instructions="Research competitors, market positioning, and competitive landscape."
    )
    
    # Execute all agents in parallel
    print("🚀 Starting parallel research tasks...")
    start_time = time.time()
    
    # Create tasks for concurrent execution
    tasks = [
        Runner.run(market_researcher, f"Research market aspects of: {topic}"),
        Runner.run(tech_researcher, f"Research technical aspects of: {topic}"),
        Runner.run(social_researcher, f"Research social aspects of: {topic}"),
        Runner.run(competitive_researcher, f"Research competitive landscape of: {topic}")
    ]
    
    # Wait for all tasks to complete simultaneously
    results = await asyncio.gather(*tasks)
    
    total_time = time.time() - start_time
    
    # Collect results with timing
    agent_names = ["Market Researcher", "Tech Researcher", "Social Researcher", "Competitive Researcher"]
    
    for i, (agent_name, result) in enumerate(zip(agent_names, results)):
        context.add_result(agent_name, result.final_output, total_time / len(agent_names))
        print(f"✅ {agent_name} completed")
    
    print(f"⚡ All parallel tasks completed in {total_time:.2f} seconds")
    return context.parallel_results

async def compare_sequential_vs_parallel(topic: str):
    """Compare sequential vs parallel execution times"""
    
    print(f"\n⚖️ PERFORMANCE COMPARISON: {topic}")
    print("=" * 60)
    
    # Sequential execution (one after another)
    print("🐌 Sequential Execution:")
    seq_start = time.time()
    
    agents = [
        Agent(name="Agent 1", instructions="Research market aspects"),
        Agent(name="Agent 2", instructions="Research technical aspects"), 
        Agent(name="Agent 3", instructions="Research social aspects"),
        Agent(name="Agent 4", instructions="Research competitive aspects")
    ]
    
    for agent in agents:
        result = await Runner.run(agent, f"Research {topic}")
        print(f"  ✅ {agent.name} completed")
    
    seq_time = time.time() - seq_start
    print(f"Sequential total time: {seq_time:.2f} seconds")
    
    # Parallel execution (simultaneous)
    print("\n⚡ Parallel Execution:")
    par_start = time.time()
    
    tasks = [Runner.run(agent, f"Research {topic}") for agent in agents]
    await asyncio.gather(*tasks)
    
    par_time = time.time() - par_start
    print(f"Parallel total time: {par_time:.2f} seconds")
    
    # Show performance improvement
    speedup = seq_time / par_time if par_time > 0 else 0
    print(f"\n📊 Performance Improvement: {speedup:.1f}x faster")
    print(f"Time saved: {seq_time - par_time:.2f} seconds")

async def demo_parallel():
    """Demonstrate parallel processing"""
    
    topics = [
        "Blockchain Technology",
        "Renewable Energy Markets"
    ]
    
    for topic in topics:
        print(f"\n{'='*80}")
        print(f"PARALLEL PROCESSING DEMO: {topic}")
        print("="*80)
        
        # Create parallel context
        context = ParallelContext(
            workflow_id=f"PAR-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            topic=topic,
            created_at=datetime.now()
        )
        
        # Run parallel workflow
        results = await parallel_workflow(topic, context)
        
        # Show results summary
        print(f"\n📋 PARALLEL EXECUTION SUMMARY:")
        print(f"Workflow ID: {context.workflow_id}")
        print(f"Concurrent Tasks: {len(results)}")
        print(f"Results:")
        for agent_name, result in results.items():
            execution_time = context.execution_times.get(agent_name, 0)
            print(f"  • {agent_name}: {result[:100]}... (Est. {execution_time:.2f}s)")
        
        # Performance comparison
        await compare_sequential_vs_parallel(topic)

if __name__ == "__main__":
    asyncio.run(demo_parallel())
