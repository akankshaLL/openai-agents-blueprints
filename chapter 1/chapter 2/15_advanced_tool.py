"""Advanced Tool Integration Example

This example demonstrates sophisticated tool patterns:
- Async tools with error handling and validation
- Tools that return structured data (Dict, complex objects)
- Multi-step tool workflows and tool chaining
- Production-ready tool patterns with logging and error recovery

Advanced patterns for building robust, production-ready agent tools.

Usage:
    python 15_advanced_tool.py
"""

import os
from dotenv import load_dotenv
from agents import function_tool, Agent, Runner
import asyncio
from typing import Optional, Dict, Any
import logging

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

# Advanced tool with error handling
@function_tool
async def fetch_user_data(user_id: str) -> Dict[str, Any]:
    """Fetch user data from external service with error handling."""
    try:
        # Simulate database/API call
        await asyncio.sleep(0.1)  # Simulate async operation
        
        # Mock user database
        users = {
            "12345": {"name": "John Doe", "tier": "premium", "last_login": "2025-01-15"},
            "67890": {"name": "Jane Smith", "tier": "basic", "last_login": "2025-01-10"}
        }
        
        if user_id not in users:
            return {"error": "User not found", "user_id": user_id}
        
        return {"success": True, "user": users[user_id]}
        
    except Exception as e:
        logging.error(f"Error fetching user {user_id}: {e}")
        return {"error": f"Service unavailable: {str(e)}"}

@function_tool
def validate_email(email: str) -> Dict[str, bool]:
    """Validate email format and domain."""
    import re
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid_format = bool(re.match(email_pattern, email))
    
    # Check for common domains
    common_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
    domain = email.split('@')[1] if '@' in email else ''
    is_common_domain = domain.lower() in common_domains
    
    return {
        "is_valid_format": is_valid_format,
        "domain": domain,
        "is_common_domain": is_common_domain,
        "recommended_action": "proceed" if is_valid_format else "request_correction"
    }

# Simplified tool 
@function_tool
def check_identifier_type(identifier: str) -> Dict[str, Any]:
    """Check if identifier is email or user_id and provide basic validation."""
    
    if '@' in identifier:
        return {
            "type": "email",
            "identifier": identifier,
            "message": "This appears to be an email address. Use validate_email tool for detailed validation."
        }
    else:
        return {
            "type": "user_id", 
            "identifier": identifier,
            "message": "This appears to be a user ID. Use fetch_user_data tool to look up user information."
        }

# Create agent with multiple tools
support_agent = Agent(
    name="AdvancedSupport",
    instructions="""
    You are an advanced customer support agent with access to user lookup tools.
    
    When users provide information:
    1. Use check_identifier_type to determine if it's an email or user ID
    2. Use validate_email for email addresses
    3. Use fetch_user_data for user IDs
    4. Always explain what validation steps you're taking
    5. Provide helpful error messages when validation fails
    
    Be professional and thorough in your responses.
    """,
    tools=[fetch_user_data, validate_email, check_identifier_type]
)

# Demonstrate tool usage
async def demonstrate_advanced_tools():
    print("=== Advanced Tool Integration Demo ===\n")
    
    test_cases = [
        "Please look up user 12345",
        "Can you validate this email: john.doe@gmail.com?",
        "Check user information for invalid.email@",
        "Look up user 99999"
    ]
    
    for query in test_cases:
        print(f"User: {query}")
        result = await Runner.run(support_agent, query)
        print(f"Agent: {result.final_output}\n")
        
        # Show tool usage details        
        tool_calls = [item for item in result.new_items if item.type == "tool_call_item"]
        if tool_calls:
            print(f"Tools used: {len(tool_calls)} tool call(s)")            
            print("  See RunResult.new_items for detailed tool call information")

if __name__ == "__main__":
    asyncio.run(demonstrate_advanced_tools())
