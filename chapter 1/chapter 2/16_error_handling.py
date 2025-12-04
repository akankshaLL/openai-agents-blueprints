"""Error Handling Example

This example demonstrates production-ready error handling patterns:
- Building a RobustAgent wrapper with retry logic
- Handling specific agent exceptions (MaxTurnsExceeded, ModelBehaviorError)
- Implementing graceful degradation and fallback responses
- Comprehensive logging and error tracking for production systems

Essential pattern for building reliable, production-grade agent applications.

Usage:
    python 16_error_handling.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded, ModelBehaviorError
import logging

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

class RobustAgent:
    """A production-ready agent wrapper with comprehensive error handling."""
    
    def __init__(self, agent: Agent, max_retries: int = 3):
        self.agent = agent
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
    
    def execute_with_retry(self, user_input, **kwargs):
        """Execute agent with retry logic and comprehensive error handling."""
        
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Executing {self.agent.name}, attempt {attempt + 1}")
                
                result = Runner.run_sync(
                    self.agent, 
                    user_input, 
                    max_turns=5,  # Prevent infinite loops
                    **kwargs
                )
                
                self.logger.info(f"Execution successful on attempt {attempt + 1}")
                return result
                
            except MaxTurnsExceeded:
                self.logger.warning(f"Attempt {attempt + 1}: Max turns exceeded")
                if attempt == self.max_retries - 1:
                    return self._create_error_response("The request was too complex to complete.")
                    
            except ModelBehaviorError as e:
                self.logger.warning(f"Attempt {attempt + 1}: Model behavior error: {e}")
                if attempt == self.max_retries - 1:
                    return self._create_error_response("Unable to process request due to response format issues.")
                    
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1}: Unexpected error: {e}")
                if attempt == self.max_retries - 1:
                    return self._create_error_response("An unexpected error occurred. Please try again.")
        
        return self._create_error_response("Service temporarily unavailable.")
    
    def _create_error_response(self, message: str):
        """Create a fallback response for error scenarios."""
        # In a real implementation, you might return a structured error object
        class ErrorResult:
            def __init__(self, message):
                self.final_output = message
                self.last_agent = self.agent
                self.new_items = []
                self.raw_responses = []
                
        return ErrorResult(message)

# Usage example
reliable_agent = RobustAgent(
    Agent(
        name="CustomerService",
        instructions="Provide helpful customer service responses."
    )
)

result = reliable_agent.execute_with_retry("Help me with my account")
print(result.final_output)
