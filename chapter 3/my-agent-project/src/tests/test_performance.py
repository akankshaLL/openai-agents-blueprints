# tests/test_performance.py
import pytest
import asyncio
import time
from src.my_agents.specialized.customer_support import CustomerSupportAgent
from agents import Runner

class TestAgentPerformance:
    """Performance tests for agent applications."""
    
    @pytest.mark.performance
    def test_response_time_under_load(self):
        """Test agent response time under concurrent load."""
        agent = CustomerSupportAgent()
        
        async def single_request():
            start_time = time.time()
            result = await Runner.run(agent.agent, "What are your business hours?")
            end_time = time.time()
            return end_time - start_time, result
        
        async def load_test():
            tasks = [single_request() for _ in range(10)]
            results = await asyncio.gather(*tasks)
            
            response_times = [r[0] for r in results]
            responses = [r[1] for r in results]
            
            assert len(responses) == 10
            assert all(r.final_output is not None for r in responses)
            
            avg_response_time = sum(response_times) / len(response_times)
            assert avg_response_time < 5.0  # Average under 5 seconds
            
            return {"avg_response_time": avg_response_time}
        
        result = asyncio.run(load_test())
        print(f"Performance results: {result}")
