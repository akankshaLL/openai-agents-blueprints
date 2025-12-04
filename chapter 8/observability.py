"""
Minimal OpenAI Agent with Observability and Monitoring
Demonstrates the built-in tracing and performance metrics capabilities
mentioned in Chapter 8: Observability & Monitoring
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from agents import Agent, Runner, function_tool

# Performance metrics class from the document
@dataclass
class AgentPerformanceMetrics:
    operation_name: str
    start_time: float
    end_time: float = 0.0
    token_usage: Dict[str, int] = field(default_factory=dict)
    tool_calls: List[str] = field(default_factory=list)
    reasoning_depth: int = 0
    
    @property
    def duration(self) -> float:
        if self.end_time > 0:
            return self.end_time - self.start_time
        return time.time() - self.start_time

# Custom tools to demonstrate observability
@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    # Simulate API call delay
    time.sleep(0.5)
    return f"The weather in {city} is sunny with 22°C temperature."

@function_tool
def get_time() -> str:
    """Get current time"""
    return f"Current time is {time.strftime('%Y-%m-%d %H:%M:%S')}"

@function_tool
def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> str:
    """Calculate tip amount for a given bill"""
    tip = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip
    return f"Bill: ${bill_amount:.2f}, Tip ({tip_percentage}%): ${tip:.2f}, Total: ${total:.2f}"

class ObservableAgent:
    """Wrapper class to add observability to OpenAI Agents"""
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.metrics: List[AgentPerformanceMetrics] = []
    
    async def run_with_observability(self, input_message: str) -> Dict:
        """Run agent with built-in performance tracking"""
        
        # Start performance tracking
        metrics = AgentPerformanceMetrics(
            operation_name=f"agent_run_{self.agent.name}",
            start_time=time.time()
        )
        
        try:
            print(f"🤖 Starting agent run: {input_message}")
            print(f"📊 Agent: {self.agent.name}")
            print(f"⏱️  Start time: {time.strftime('%H:%M:%S', time.localtime(metrics.start_time))}")
            
            # Run the agent (built-in tracing automatically handles this)
            result = await Runner.run(self.agent, input_message)
            
            # Complete performance tracking
            metrics.end_time = time.time()
            
            self.metrics.append(metrics)
            print(f"❌ Error during agent run: {e}")
            raise
    
    def _display_metrics(self, metrics: AgentPerformanceMetrics, result):
        """Display comprehensive observability information"""
        print("\n" + "="*60)
        print("📈 AGENT OBSERVABILITY REPORT")
        print("="*60)
        
        # Performance Metrics
        print(f"⏱️  Duration: {metrics.duration:.2f} seconds")
        print(f"🔧 Tools Called: {len(metrics.tool_calls)}")
        if metrics.tool_calls:
            print(f"🛠️  Tools Used: {', '.join(metrics.tool_calls)}")
        
        # Token Usage (if available)
        if metrics.token_usage:
            print(f"🎯 Token Usage: {metrics.token_usage}")
        
        # Built-in Tracing Information
        if hasattr(result, 'trace') and result.trace:
            print(f"🔍 Trace ID: {result.trace.trace_id}")
            print(f"📋 Total Events: {len(result.trace.events)}")
            
            # Display trace events
            print("\n📊 EXECUTION TRACE:")
            for i, event in enumerate(result.trace.events, 1):
                timestamp = time.strftime('%H:%M:%S', time.localtime(event.timestamp))
                print(f"  {i}. [{timestamp}] {event.type}: {getattr(event, 'name', 'N/A')}")
        
        print(f"\n💬 Final Output: {result.final_output}")
        print("="*60)
    
    def get_performance_summary(self) -> Dict:
        """Get summary of all agent runs"""
        if not self.metrics:
            return {"message": "No metrics available"}
        
        total_runs = len(self.metrics)
        avg_duration = sum(m.duration for m in self.metrics) / total_runs
        total_tool_calls = sum(len(m.tool_calls) for m in self.metrics)
        
        return {
            "total_runs": total_runs,
            "average_duration": round(avg_duration, 2),
            "total_tool_calls": total_tool_calls,
            "most_used_tools": self._get_most_used_tools()
        }
    
    def _get_most_used_tools(self) -> Dict[str, int]:
        """Get frequency count of tool usage"""
        tool_count = {}
        for metrics in self.metrics:
            for tool in metrics.tool_calls:
                tool_count[tool] = tool_count.get(tool, 0) + 1
        return dict(sorted(tool_count.items(), key=lambda x: x[1], reverse=True))

async def main():
    """Demonstrate the observable agent with multiple interactions"""
    
    # Create an agent with tools (demonstrates the SDK's built-in capabilities)
    agent = Agent(
        name="Customer Service Assistant",
        instructions="""You are a helpful customer service assistant. 
        You can check weather, provide time information, and calculate tips.
        Always be friendly and provide detailed responses.""",
        tools=[get_weather, get_time, calculate_tip]
    )
    
    # Wrap with observability
    observable_agent = ObservableAgent(agent)
    
    # Test scenarios that will generate different observability patterns
    test_scenarios = [
        "What's the weather like in New York?",
        "What time is it now?",
        "I had dinner that cost $85.50. How much should I tip at 20%?",
        "Can you tell me the weather in London and what time it is?",
    ]
    
    print("🚀 Starting OpenAI Agent Observability Demo")
    print("This demonstrates the built-in tracing and monitoring capabilities\n")
    
    # Run each scenario
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 Scenario {i}/{len(test_scenarios)}")
        try:
            await observable_agent.run_with_observability(scenario)
        except Exception as e:
            print(f"Error in scenario {i}: {e}")
        
        # Add delay between runs for clarity
        await asyncio.sleep(1)
    
    # Display performance summary
    print("\n" + "="*60)
    print("📊 PERFORMANCE SUMMARY")
    print("="*60)
    summary = observable_agent.get_performance_summary()
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    # Note: You need to set OPENAI_API_KEY environment variable
    # export OPENAI_API_KEY="your-api-key-here"
    
    print("⚠️  Make sure to set your OPENAI_API_KEY environment variable")
    print("   export OPENAI_API_KEY='your-api-key-here'\n")
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure OPENAI_API_KEY is set")
        print("   2. Install the SDK: pip install openai-agents")
        print("   3. Check your internet connection")
