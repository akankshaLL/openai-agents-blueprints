# tests/test_agents.py
import pytest
from unittest.mock import patch, MagicMock

from src.my_agents.specialized.customer_support import CustomerSupportAgent, CustomerQuery

@pytest.mark.asyncio
async def test_customer_support_agent_creation():
    """Test that the customer support agent can be created."""
    agent = CustomerSupportAgent()
    assert agent.name == "Customer Support"
    assert agent.model == "gpt-4o-mini"  # Default from settings
    assert len(agent.tools) == 1  # Should have the get_product_info tool

@pytest.mark.asyncio
@patch("agents.Runner.run_sync")
async def test_customer_support_agent_response(mock_run_sync):
    """Test that the customer support agent can generate responses."""
    # Mock the RunResult
    mock_result = MagicMock()
    mock_result.final_output = CustomerQuery(
        response="Thank you for your question about product ABC123.",
        sentiment="positive",
        follow_up_needed=False,
    )
    mock_run_sync.return_value = mock_result
    
    agent = CustomerSupportAgent()
    
    # Run the agent
    from agents import Runner
    result = Runner.run_sync(agent.agent, "Tell me about product ABC123")
    
    # Verify the result
    assert mock_run_sync.called
    assert isinstance(result.final_output, CustomerQuery)
    assert "product ABC123" in result.final_output.response
    assert result.final_output.sentiment == "positive"
    assert result.final_output.follow_up_needed is False
