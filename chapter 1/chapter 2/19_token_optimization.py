"""Token Optimization Example

This example demonstrates cost and performance optimization techniques:
- Creating use-case specific agents with optimized model settings
- Implementing response caching to reduce API calls and costs
- Batch processing for improved efficiency
- Performance monitoring and cache hit rate analysis

Critical pattern for building cost-effective, high-performance agent applications.

Usage:
    python 19_token_optimization.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from typing import Dict, Any
import asyncio

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

class OptimizedAgentManager:
    """Manager for optimized agent performance."""
    
    def __init__(self):
        self.model_cache = {}
        self.response_cache = {}
    
    def create_optimized_agent(self, use_case: str) -> Agent:
        """Create agents optimized for specific use cases."""
        
        optimizations = {
            "quick_responses": {
                "model": "gpt-4o-mini",
                "settings": ModelSettings(
                    temperature=0.1,
                    max_tokens=150,
                    top_p=0.5
                ),
                "instructions": "Provide concise, direct responses. Be brief and accurate."
            },
            "detailed_analysis": {
                "model": "gpt-4o",
                "settings": ModelSettings(
                    temperature=0.3,
                    max_tokens=2000,
                    top_p=0.8
                ),
                "instructions": "Provide comprehensive analysis while being efficient with language."
            },
            "creative_tasks": {
                "model": "gpt-4o",
                "settings": ModelSettings(
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=0.9
                ),
                "instructions": "Be creative but focused. Avoid unnecessary elaboration."
            }
        }
        
        config = optimizations.get(use_case, optimizations["quick_responses"])
        
        return Agent(
            name=f"Optimized_{use_case}",
            model=config["model"],
            model_settings=config["settings"],
            instructions=config["instructions"]
        )
    
    async def execute_with_caching(self, agent: Agent, user_input: str) -> Dict[str, Any]:
        """Execute with response caching for repeated queries."""
        
        # Simple cache key (in production, use more sophisticated hashing)
        cache_key = f"{agent.name}:{hash(user_input)}"
        
        if cache_key in self.response_cache:
            return {
                "response": self.response_cache[cache_key],
                "cached": True,
                "execution_time": 0.001  # Cached response time
            }
        
        # Execute and cache result
        start_time = asyncio.get_event_loop().time()
        result = await Runner.run(agent, user_input)
        execution_time = asyncio.get_event_loop().time() - start_time
        
        # Cache the response
        self.response_cache[cache_key] = result.final_output
        
        return {
            "response": result.final_output,
            "cached": False,
            "execution_time": execution_time,
            "token_usage": result.raw_responses[0].usage.total_tokens if result.raw_responses else 0
        }
    
    async def batch_execute(self, agent: Agent, queries: list) -> Dict[str, Any]:
        """Execute multiple queries efficiently with batching."""
        
        start_time = asyncio.get_event_loop().time()
        
        # Execute all queries concurrently
        tasks = [self.execute_with_caching(agent, query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        total_time = asyncio.get_event_loop().time() - start_time
        
        # Calculate performance metrics
        cached_count = sum(1 for r in results if r["cached"])
        total_tokens = sum(r.get("token_usage", 0) for r in results)
        
        return {
            "results": results,
            "performance": {
                "total_time": total_time,
                "queries_processed": len(queries),
                "cache_hit_rate": cached_count / len(queries) * 100,
                "total_tokens": total_tokens,
                "avg_time_per_query": total_time / len(queries)
            }
        }

# Performance testing example
async def demonstrate_performance_optimization():
    """Demonstrate performance optimization techniques."""
    
    print("⚡ PERFORMANCE OPTIMIZATION DEMONSTRATION")
    print("=" * 50)
    
    manager = OptimizedAgentManager()
    
    # Create different optimized agents
    quick_agent = manager.create_optimized_agent("quick_responses")
    detailed_agent = manager.create_optimized_agent("detailed_analysis")
    
    # Test queries
    quick_queries = [
        "What is 2+2?",
        "Capital of France?",
        "Define AI",
        "What is 2+2?",  # Duplicate for cache testing
        "Capital of France?"  # Duplicate for cache testing
    ]
    
    detailed_queries = [
        "Explain machine learning algorithms",
        "Analyze the impact of renewable energy"
    ]
    
    # Test quick responses with caching
    print("\n--- Quick Response Optimization ---")
    quick_results = await manager.batch_execute(quick_agent, quick_queries)
    
    print(f"Processed {quick_results['performance']['queries_processed']} queries")
    print(f"Total time: {quick_results['performance']['total_time']:.3f}s")
    print(f"Cache hit rate: {quick_results['performance']['cache_hit_rate']:.1f}%")
    print(f"Avg time per query: {quick_results['performance']['avg_time_per_query']:.3f}s")
    print(f"Total tokens: {quick_results['performance']['total_tokens']}")
    
    # Show individual results
    for i, result in enumerate(quick_results['results']):
        status = "💾 CACHED" if result['cached'] else "🔄 EXECUTED"
        print(f"Query {i+1}: {status} - {result['execution_time']:.3f}s")
    
    # Test detailed responses
    print("\n--- Detailed Analysis Optimization ---")
    detailed_results = await manager.batch_execute(detailed_agent, detailed_queries)
    
    print(f"Processed {detailed_results['performance']['queries_processed']} queries")
    print(f"Total time: {detailed_results['performance']['total_time']:.3f}s")
    print(f"Total tokens: {detailed_results['performance']['total_tokens']}")

# Run the demonstration
if __name__ == "__main__":
    asyncio.run(demonstrate_performance_optimization())
