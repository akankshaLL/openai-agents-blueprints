"""Scalable Agent Example

This example demonstrates enterprise-scale agent deployment patterns:
- Building EnterpriseAgentManager with load balancing and rate limiting
- Agent pooling for high-availability and performance
- Concurrent request handling with semaphore-based rate limiting
- Health monitoring and performance metrics for production systems

Advanced pattern for building enterprise-grade, scalable agent applications.

Usage:
    python 21_scalable_agent.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging
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
class AgentPool:
    """Pool of agents for load balancing."""
    agents: List[Agent]
    current_index: int = 0
    
    def get_next_agent(self) -> Agent:
        """Get next agent using round-robin."""
        agent = self.agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.agents)
        return agent

class EnterpriseAgentManager:
    """Enterprise-grade agent management system."""
    
    def __init__(self, max_concurrent_requests: int = 50):
        self.max_concurrent_requests = max_concurrent_requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.agent_pools: Dict[str, AgentPool] = {}
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0
        }
        self.logger = logging.getLogger(__name__)
    
    def register_agent_pool(self, pool_name: str, agents: List[Agent]):
        """Register a pool of agents for load balancing."""
        self.agent_pools[pool_name] = AgentPool(agents=agents)
        self.logger.info(f"Registered agent pool '{pool_name}' with {len(agents)} agents")
    
    async def execute_request(self, pool_name: str, user_input: str, **kwargs) -> Dict:
        """Execute request with load balancing and rate limiting."""
        
        async with self.semaphore:  # Rate limiting
            start_time = datetime.now()
            
            try:
                # Get agent from pool
                if pool_name not in self.agent_pools:
                    "response": result.final_output,
                    "agent_name": agent.name,
                    "execution_time": execution_time,
                    "token_usage": tokens
                }
                
            except Exception as e:
                self.metrics["total_requests"] += 1
                self.metrics["failed_requests"] += 1
                
                self.logger.error(f"Request failed: {str(e)}")
                
                return {
                    "success": False,
                    "error": str(e),
                    "execution_time": (datetime.now() - start_time).total_seconds()
                }
    
    def get_health_status(self) -> Dict:
        """Get system health and performance metrics."""
        
        total_requests = self.metrics["total_requests"]
        success_rate = (self.metrics["successful_requests"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "status": "healthy" if success_rate > 95 else "degraded" if success_rate > 80 else "unhealthy",
            "total_requests": total_requests,
            "success_rate": round(success_rate, 2),
            "failed_requests": self.metrics["failed_requests"],
            "total_tokens_processed": self.metrics["total_tokens"],
            "active_agent_pools": len(self.agent_pools),
            "max_concurrent_requests": self.max_concurrent_requests
        }

# Enterprise deployment example
async def demonstrate_enterprise_deployment():
    """Demonstrate enterprise deployment patterns."""
    
    print("🏢 ENTERPRISE DEPLOYMENT DEMONSTRATION")
    print("=" * 50)
    
    # Create enterprise manager
    manager = EnterpriseAgentManager(max_concurrent_requests=10)
    
    # Create agent pools for different services
    customer_service_agents = [
        Agent(
            name=f"CustomerService-{i}",
            instructions="You are a professional customer service agent.",
            model="gpt-4o-mini"
        ) for i in range(3)
    ]
    
    technical_support_agents = [
        Agent(
            name=f"TechnicalSupport-{i}",
            instructions="You are a technical support specialist.",
            model="gpt-4o"
        ) for i in range(2)
    ]
    
    # Register agent pools
    manager.register_agent_pool("customer_service", customer_service_agents)
    manager.register_agent_pool("technical_support", technical_support_agents)
    
    # Simulate enterprise workload
    customer_requests = [
        "I need help with my account",
        "How do I reset my password?",
        "What are your business hours?",
        "I want to cancel my subscription",
        "Can you help me with billing?"
    ]
    
    technical_requests = [
        "My API calls are failing",
        "Help me debug this error",
        "Performance optimization needed"
    ]
    
    print("\n--- Processing Customer Service Requests ---")
    customer_tasks = [
        manager.execute_request("customer_service", request)
        for request in customer_requests
    ]
    
    customer_results = await asyncio.gather(*customer_tasks)
    
    for i, result in enumerate(customer_results):
        if result["success"]:
            print(f"✅ Request {i+1}: {result['execution_time']:.3f}s, Agent: {result['agent_name']}")
        else:
            print(f"❌ Request {i+1}: Failed - {result['error']}")
    
    print("\n--- Processing Technical Support Requests ---")
    technical_tasks = [
        manager.execute_request("technical_support", request)
        for request in technical_requests
    ]
    
    technical_results = await asyncio.gather(*technical_tasks)
    
    for i, result in enumerate(technical_results):
        if result["success"]:
            print(f"✅ Request {i+1}: {result['execution_time']:.3f}s, Agent: {result['agent_name']}")
        else:
            print(f"❌ Request {i+1}: Failed - {result['error']}")
    
    # Show health status
    print("\n--- System Health Status ---")
    health = manager.get_health_status()
    for key, value in health.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

# Run enterprise demonstration
if __name__ == "__main__":
    asyncio.run(demonstrate_enterprise_deployment())
