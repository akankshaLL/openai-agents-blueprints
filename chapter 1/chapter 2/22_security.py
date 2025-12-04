"""Security and Compliance Example

This example demonstrates enterprise security patterns for agent deployments:
- Building SecureAgentWrapper with input validation and output sanitization
- Implementing audit logging and compliance tracking
- Blocking sensitive data patterns and enforcing security policies
- Creating comprehensive audit reports for regulatory compliance

Critical pattern for deploying agents in regulated industries and enterprise environments.

Usage:
    python 22_security.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner
from typing import Dict, List, Any
import hashlib
import logging
from datetime import datetime
import asyncio

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

class SecureAgentWrapper:
    """Security wrapper for enterprise agent deployments."""
    
    def __init__(self, agent: Agent, security_policies: Dict[str, Any]):
        self.agent = agent
        self.security_policies = security_policies
        self.audit_log = []
        self.logger = logging.getLogger(__name__)
    
    def validate_input(self, user_input: str) -> tuple[bool, str]:
        """Validate user input against security policies."""
        
        # Check for sensitive data patterns
        sensitive_patterns = self.security_policies.get("blocked_patterns", [])
        for pattern in sensitive_patterns:
            if pattern.lower() in user_input.lower():
                return False, f"Input contains blocked pattern: {pattern}"
        
        # Check input length
        max_length = self.security_policies.get("max_input_length", 1000)
        if len(user_input) > max_length:
            return False, f"Input exceeds maximum length of {max_length} characters"
        
        return True, "Input validated"
    
    def sanitize_output(self, output: str) -> str:
        """Sanitize output to remove sensitive information."""
        
        # Remove potential sensitive data
        sensitive_data = self.security_policies.get("redact_patterns", [])
        sanitized = output
        
        for pattern in sensitive_data:
            # In production, use more sophisticated redaction
            sanitized = sanitized.replace(pattern, "[REDACTED]")
        
        return sanitized
    
    def log_interaction(self, user_input: str, output: str, metadata: Dict):
        """Log interaction for audit purposes."""
        
            "success": metadata.get("success", True)
        }
        
        self.audit_log.append(log_entry)
        
        # Log to external audit system in production
        self.logger.info(f"Agent interaction logged: {log_entry}")
    
    async def secure_execute(self, user_input: str, metadata: Dict = None) -> Dict:
        """Execute agent with full security controls."""
        
        metadata = metadata or {}
        
        # Validate input
        is_valid, validation_message = self.validate_input(user_input)
        if not is_valid:
            error_response = {
                "success": False,
                "error": validation_message,
                "blocked": True
            }
            self.log_interaction(user_input, "", {**metadata, "success": False})
            return error_response
        
        try:
            # Execute agent
            result = await Runner.run(self.agent, user_input)
            
            # Sanitize output
            sanitized_output = self.sanitize_output(result.final_output)
            
            # Log interaction
            self.log_interaction(user_input, sanitized_output, {**metadata, "success": True})
            
            return {
                "success": True,
                "response": sanitized_output,
                "agent_name": self.agent.name
            }
            
        except Exception as e:
            error_msg = f"Execution failed: {str(e)}"
            self.log_interaction(user_input, "", {**metadata, "success": False})
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def get_audit_report(self) -> Dict:
        """Generate audit report for compliance."""
        
        total_interactions = len(self.audit_log)
        successful_interactions = sum(1 for log in self.audit_log if log["success"])
        
        return {
            "total_interactions": total_interactions,
            "successful_interactions": successful_interactions,
            "failure_rate": (total_interactions - successful_interactions) / total_interactions * 100 if total_interactions > 0 else 0,
            "unique_users": len(set(log["user_id"] for log in self.audit_log)),
            "date_range": {
                "start": self.audit_log[0]["timestamp"] if self.audit_log else None,
                "end": self.audit_log[-1]["timestamp"] if self.audit_log else None
            }
        }

# Security demonstration
async def demonstrate_security_patterns():
    """Demonstrate enterprise security patterns."""
    
    print("🔒 SECURITY AND COMPLIANCE DEMONSTRATION")
    print("=" * 50)
    
    # Define security policies
    security_policies = {
        "blocked_patterns": ["password", "ssn", "credit card"],
        "redact_patterns": ["admin@company.com", "secret"],
        "max_input_length": 500
    }
    
    # Create secure agent
    base_agent = Agent(
        name="SecureAgent",
        instructions="You are a helpful assistant for customer inquiries.",
        model="gpt-4o-mini"
    )
    
    secure_agent = SecureAgentWrapper(base_agent, security_policies)
    
    # Test cases
    test_cases = [
        {
            "input": "What is your email?",
            "metadata": {"user_id": "user123", "session_id": "sess456"}
        },
        {
            "input": "My password is 123456, can you help?",
            "metadata": {"user_id": "user124", "session_id": "sess457"}
        },
        {
            "input": "How do I contact support?",
            "metadata": {"user_id": "user125", "session_id": "sess458"}
        }
    ]
    
    print("\n--- Security Test Results ---")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['input']}")
        result = await secure_agent.secure_execute(test_case['input'], test_case['metadata'])
        print(f"Result: {result}")
    
    # Show audit capabilities
    print(f"\n--- Audit Report ---")
    audit_report = secure_agent.get_audit_report()
    print(audit_report)

if __name__ == "__main__":
    asyncio.run(demonstrate_security_patterns())
