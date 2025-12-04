"""
Comprehensive OpenAI Agent with Business & Technical Observability
Demonstrates built-in tracing, performance metrics, and custom business KPIs
mentioned in Chapter 8: Observability & Monitoring
"""

import asyncio
import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from collections import defaultdict
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

@dataclass  
class BusinessMetrics:
    """Custom metrics for business-specific monitoring."""
    customer_satisfaction_score: float = 0.0
    resolution_time: float = 0.0
    escalation_required: bool = False
    cost_per_interaction: float = 0.0
    knowledge_base_hits: int = 0

class CustomMetricsCollector:
    """Collects and aggregates custom metrics for agent operations."""
    
    def __init__(self):
        self.metrics: List[BusinessMetrics] = []
        self.operation_stats = defaultdict(lambda: {
            'total_count': 0,
            'success_count': 0,
            'total_duration': 0.0,
            'total_cost': 0.0
        })
    
    def record_interaction(self, operation_type: str, metrics: BusinessMetrics):
        """Record a business interaction with custom metrics."""
        self.metrics.append(metrics)
        
        stats = self.operation_stats[operation_type]
        stats['total_count'] += 1
        stats['total_duration'] += metrics.resolution_time
        stats['total_cost'] += metrics.cost_per_interaction
        
        if not metrics.escalation_required:
            stats['success_count'] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Generate summary of collected metrics."""
        if not self.metrics:
            return {}
            
        total_interactions = len(self.metrics)
        avg_satisfaction = sum(m.customer_satisfaction_score for m in self.metrics) / total_interactions
        avg_resolution_time = sum(m.resolution_time for m in self.metrics) / total_interactions
        escalation_rate = sum(1 for m in self.metrics if m.escalation_required) / total_interactions
        
        return {
            'total_interactions': total_interactions,
            "description": "Simple weather lookup"
        },
        {
            "query": "I need help understanding our company's remote work policy. Can you search for that information?",
            "operation_type": "policy_inquiry", 
            "description": "Knowledge base search required"
        },
        {
            "query": "Our team dinner cost $340 for 8 people. What's a good tip amount at 18%?",
            "operation_type": "calculation_request",
            "description": "Financial calculation task"
        },
        {
            "query": "I'm having issues with my account billing and need urgent help. This is affecting our production system and I need to speak to a manager immediately.",
            "operation_type": "escalation_required",
            "description": "Complex issue requiring human escalation"
        },
        {
            "query": "What time is it now, and can you also check the weather in London for our UK team meeting?",
            "operation_type": "multi_task_request",
            "description": "Multiple tool usage scenario"
        }
    ]
    
    print("🚀 Enterprise AI Agent Observability Demonstration")
    print("=" * 70)
    print("Demonstrating comprehensive monitoring with:")
    print("• OpenAI SDK built-in tracing")
    print("• Technical performance metrics") 
    print("• Business KPIs and cost analysis")
    print("• Enterprise dashboard generation")
    print("=" * 70)
    
    # Execute enterprise scenarios
    for i, scenario in enumerate(enterprise_scenarios, 1):
        print(f"\n🎯 ENTERPRISE SCENARIO {i}/{len(enterprise_scenarios)}")
        print(f"📝 Description: {scenario['description']}")
        print(f"🏷️  Operation Type: {scenario['operation_type']}")
        
        try:
            await enterprise_agent.run_with_full_observability(
                scenario['query'], 
                scenario['operation_type']
            )
        except Exception as e:
            print(f"❌ Error in scenario {i}: {e}")
        
        # Brief pause between scenarios for clarity
        await asyncio.sleep(1.5)
    
    # Generate comprehensive enterprise dashboard
    print("\n" + "="*70)
    print("📊 ENTERPRISE MONITORING DASHBOARD")
    print("="*70)
    
    dashboard = enterprise_agent.get_enterprise_dashboard()
    
    def print_dashboard_section(section_name, data, indent=0):
        """Recursively print dashboard data with proper formatting."""
        spaces = "  " * indent
        if isinstance(data, dict):
            print(f"{spaces}{section_name}:")
            for key, value in data.items():
                if isinstance(value, dict):
                    print_dashboard_section(key, value, indent + 1)
                else:
                    print(f"{spaces}  {key}: {value}")
        else:
            print(f"{spaces}{section_name}: {data}")
    
    for section, content in dashboard.items():
        print_dashboard_section(section, content)
    
    # Summary insights for stakeholders
    print("\n" + "="*70)
    print("🎯 KEY INSIGHTS FOR STAKEHOLDERS")
    print("="*70)
    
    business_summary = enterprise_agent.business_collector.get_summary()
    if business_summary:
        efficiency = 100 - business_summary.get('escalation_rate', 0)
        cost_analysis = dashboard.get("📊 ENTERPRISE DASHBOARD", {}).get("cost_analysis", {})
        
        print(f"✅ Automation Efficiency: {efficiency}% of queries resolved without escalation")
        print(f"😊 Customer Satisfaction: {business_summary.get('average_satisfaction', 0)}/5.0 average score")
        print(f"💰 Cost Performance: ${cost_analysis.get('average_cost_per_interaction', 0)} per interaction")
        print(f"⚡ Response Time: {business_summary.get('average_resolution_time', 0)} seconds average")
        
        # Performance recommendations
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        if business_summary.get('escalation_rate', 0) > 20:
            print("  • Consider expanding knowledge base to reduce escalation rate")
        if business_summary.get('average_satisfaction', 5) < 4.0:
            print("  • Review response quality and consider additional training")
        if cost_analysis.get('average_cost_per_interaction', 0) > 0.02:
            print("  • Optimize tool usage to reduce operational costs")
        if business_summary.get('average_resolution_time', 0) > 8.0:
            print("  • Investigate performance bottlenecks in tool execution")

if __name__ == "__main__":
    # Note: You need to set OPENAI_API_KEY environment variable
    # export OPENAI_API_KEY="your-api-key-here"
    
    print("⚠️  SETUP REQUIREMENTS")
    print("   1. Set OPENAI_API_KEY environment variable:")
    print("      export OPENAI_API_KEY='your-api-key-here'")
    print("   2. Install the SDK: pip install openai-agents")
    print("   3. Ensure stable internet connection\n")
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Application Error: {e}")
        print("\n🔧 TROUBLESHOOTING GUIDE:")
        print("   • Verify OPENAI_API_KEY is correctly set")
        print("   • Check OpenAI account has sufficient credits")
        print("   • Ensure network connectivity to OpenAI services")
        print("   • Validate Python environment has required dependencies")
