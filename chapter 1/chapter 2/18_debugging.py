"""Advanced Debugging Example

This example demonstrates comprehensive agent debugging and observability:
- Building an AgentDebugger class for detailed execution tracing
- Tracking performance metrics, token usage, and tool calls
- Error pattern analysis and performance optimization insights
- Exporting execution traces for external analysis and monitoring

Advanced pattern for building production monitoring and debugging systems.

Usage:
    python 18_debugging.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
import time
import traceback
from datetime import datetime

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

@dataclass
class ExecutionTrace:
    """Detailed execution trace for debugging."""
    timestamp: str
    agent_name: str
    user_input: str
    execution_time: float
    success: bool
    error_message: Optional[str]
    token_usage: Dict[str, int]
    tool_calls: List[str]
    finish_reason: str
    guardrail_triggers: int
    conversation_length: int

class AgentDebugger:
    """Advanced debugging and observability for agent execution."""
    
    def __init__(self, enable_detailed_logging: bool = True):
        self.enable_detailed_logging = enable_detailed_logging
        self.execution_traces: List[ExecutionTrace] = []
        self.error_patterns: Dict[str, int] = {}
    
    def execute_with_debugging(self, agent: Agent, user_input, **kwargs) -> tuple:
        """Execute agent with comprehensive debugging and tracing."""
        
        start_time = time.time()
        execution_trace = None
        result = None
        
        try:
            # Execute the agent
            result = Runner.run_sync(agent, user_input, **kwargs)
            
            # Calculate execution metrics
            execution_time = time.time() - start_time
            
            # Extract debugging information
            token_usage = {}
            finish_reason = "completed"  # Default since ModelResponse structure differs
        if self.enable_detailed_logging:
            print("Stack Trace:")
            print(traceback.format_exc())
        
        print("-" * 60)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance analytics."""
        
        if not self.execution_traces:
            return {"message": "No executions recorded"}
        
        successful_traces = [t for t in self.execution_traces if t.success]
        failed_traces = [t for t in self.execution_traces if not t.success]
        
        # Calculate averages for successful executions
        avg_execution_time = sum(t.execution_time for t in successful_traces) / len(successful_traces) if successful_traces else 0
        avg_tokens = sum(t.token_usage.get('total', 0) for t in successful_traces) / len(successful_traces) if successful_traces else 0
        
        # Find most used tools
        all_tools = []
        for trace in successful_traces:
            all_tools.extend(trace.tool_calls)
        
        tool_usage = {}
        for tool in all_tools:
            tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        # Most common finish reasons
        finish_reasons = {}
        for trace in successful_traces:
            reason = trace.finish_reason
            finish_reasons[reason] = finish_reasons.get(reason, 0) + 1
        
        return {
            "total_executions": len(self.execution_traces),
            "successful_executions": len(successful_traces),
            "failed_executions": len(failed_traces),
            "success_rate": len(successful_traces) / len(self.execution_traces) * 100,
            "average_execution_time": avg_execution_time,
            "average_tokens_per_execution": avg_tokens,
            "most_used_tools": dict(sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)[:5]),
            "finish_reasons": finish_reasons,
            "error_patterns": self.error_patterns,
            "total_guardrail_triggers": sum(t.guardrail_triggers for t in self.execution_traces)
        }
    
    def export_traces(self, filename: str = "agent_traces.json"):
        """Export execution traces for external analysis."""
        
        trace_data = []
        for trace in self.execution_traces:
            trace_data.append({
                "timestamp": trace.timestamp,
                "agent_name": trace.agent_name,
                "user_input": trace.user_input,
                "execution_time": trace.execution_time,
                "success": trace.success,
                "error_message": trace.error_message,
                "token_usage": trace.token_usage,
                "tool_calls": trace.tool_calls,
                "finish_reason": trace.finish_reason,
                "guardrail_triggers": trace.guardrail_triggers,
                "conversation_length": trace.conversation_length
            })
        
        with open(filename, 'w') as f:
            json.dump(trace_data, f, indent=2)
        
        print(f"Exported {len(trace_data)} execution traces to {filename}")

# Usage example
def demonstrate_debugging():
    """Demonstrate advanced debugging capabilities."""
    
    print("🔬 ADVANCED DEBUGGING DEMONSTRATION")
    print("=" * 50)
    
    # Create debugger
    debugger = AgentDebugger(enable_detailed_logging=True)
    
    # Create test agent
    test_agent = Agent(
        name="TestAgent",
        instructions="You are a helpful assistant that answers questions concisely.",
        model="gpt-4o-mini"  # Faster for testing
    )
    
    # Test various scenarios
    test_cases = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "What is 2 + 2?",
        "Tell me a short story about a robot",
    ]
    
    # Execute with debugging
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        result, trace = debugger.execute_with_debugging(test_agent, test_case)
        
        if result:
            print(f"Response: {result.final_output}")
    
    # Show performance summary
    print("\n" + "=" * 50)
    print("PERFORMANCE SUMMARY")
    print("=" * 50)
    
    summary = debugger.get_performance_summary()
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Export traces
    debugger.export_traces("chapter2_debug_traces.json")

if __name__ == "__main__":
    demonstrate_debugging()
