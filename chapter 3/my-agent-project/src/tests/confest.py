# tests/conftest.py
import pytest
from src.config.settings import Settings

@pytest.fixture
def test_settings():
    """Fixture for test settings."""
    return Settings(
        openai_api_key="test-api-key",
        default_model="gpt-3.5-turbo",
        default_temperature=0.5,
        enable_tracing=False,
        trace_workflow_name="test-workflow",
        log_level="DEBUG",
        environment="test",
    )
