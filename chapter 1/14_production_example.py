"""
Production-Grade Agent Tutorial
==============================

This code demonstrates how to build a production-ready AI agent with:
- Memory management across sessions
- User context and tool integration  
- Error handling and retry logic
- Comprehensive monitoring and logging
- Token usage tracking
- Session management

Perfect for learning how to build enterprise-grade conversational AI.
"""

import asyncio
import os
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import logging

from agents import Agent, Runner, ModelSettings, RunContextWrapper, function_tool

# ============================================================================
# STEP 1: ENVIRONMENT SETUP AND VALIDATION
# ============================================================================
# Always validate your environment in production apps
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Check your .env file.")
if not api_key.startswith("sk-"):
    raise ValueError("❌ Invalid OpenAI API key format.")

# ============================================================================
# STEP 2: PRODUCTION LOGGING SETUP
# ============================================================================
# Production apps need structured logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        # In production, add: logging.FileHandler('agent.log')
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# STEP 3: CONTEXT MANAGEMENT - PASSING APP DATA TO TOOLS
# ============================================================================
@dataclass
class SessionContext:
    """
    Context object that gets passed to tools and callbacks.
    
    Production tip: This is where you put data that your tools need access to:
    - User information (ID, name, preferences)
    - Database connections
    - API clients
    - Configuration settings
    """
    user_id: str
    session_id: str
    user_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Serialize context for logging/storage - useful for debugging."""
            "message_count": len(self.conversations[session_id]),
            "exported_at": datetime.now().isoformat(),
            "export_version": "1.0"
        }
        
        logger.info(f"📤 Session {session_id} exported with {session_data['message_count']} messages")
        return session_data

# ============================================================================
# STEP 6: PRODUCTION DEMO AND TESTING
# ============================================================================
async def production_demo():
    """
    Comprehensive demo showing production agent capabilities.
    
    This demonstrates:
    - Multi-user session management
    - Memory persistence across interactions
    - Tool usage with context
    - Error handling and monitoring
    - Usage analytics
    """
    
    print("🚀 Production Agent Demo")
    print("=" * 50)
    
    # Initialize production agent
    agent = ProductionAgent(
        name="ProductionCustomerSupport",
        instructions="""You are a professional customer support agent.
        Be helpful, remember conversation context, and use tools when appropriate.
        Always be polite and professional.""",
        temperature=0.2  # Low temperature for consistent support responses
    )
    
    # Demo 1: Customer support session
    print("\n📞 DEMO 1: Customer Support Session")
    print("-" * 30)
    
    customer_context = SessionContext(
        user_id="customer_001",
        session_id="support_session_123", 
        user_name="Alice Johnson",
        metadata={
            "account_type": "premium", 
            "region": "US-West",
            "support_tier": "priority"
        }
    )
    
    # First interaction
    result1 = await agent.chat(
        "Hi, I'm having trouble accessing my premium features",
        customer_context
    )
    print(f"🙋 Customer: Hi, I'm having trouble accessing my premium features")
    print(f"🤖 Agent: {result1['response']}")
    print(f"📊 Tokens used: {result1.get('tokens_used', 0)}")
    
    # Follow-up with memory test
    result2 = await agent.chat(
        "What was my issue again? Can you check who I am?",
        customer_context
    )
    print(f"\n🙋 Customer: What was my issue again? Can you check who I am?")
    print(f"🤖 Agent: {result2['response']}")
    
    # Demo 2: Different customer, separate session
    print("\n\n📞 DEMO 2: Different Customer Session")
    print("-" * 30)
    
    customer2_context = SessionContext(
        user_id="customer_002",
        session_id="support_session_456",
        user_name="Bob Smith",
        metadata={"account_type": "basic", "region": "EU"}
    )
    
    result3 = await agent.chat(
        "Do you know what Alice's problem was?",
        customer2_context
    )
    print(f"🙋 Bob: Do you know what Alice's problem was?")
    print(f"🤖 Agent: {result3['response']}")
    print("✅ Notice: Agent doesn't know about Alice - sessions are isolated!")
    
    # Demo 3: Production monitoring
    print("\n\n📊 DEMO 3: Production Monitoring")
    print("-" * 30)
    
    # Show usage statistics
    stats = agent.get_usage_stats()
    print("Production Metrics:")
    print(json.dumps(stats, indent=2))
    
    # Export session for analysis
    session_export = agent.export_session("support_session_123")
    if session_export:
        print(f"\n📤 Session Export: {session_export['message_count']} messages exported")
    
    # Demo 4: Error handling
    print("\n\n⚠️ DEMO 4: Error Handling Test")
    print("-" * 30)
    
    # Test with empty message
    error_result = await agent.chat("", customer_context)
    print(f"Empty message result: {error_result}")
    
    print("\n🎯 Production Features Demonstrated:")
    print("✅ Memory management across sessions")
    print("✅ User context and tool integration")
    print("✅ Error handling and validation")
    print("✅ Token usage tracking")
    print("✅ Performance monitoring")
    print("✅ Session isolation")
    print("✅ Comprehensive logging")
    print("✅ Data export capabilities")

if __name__ == "__main__":
    asyncio.run(production_demo())
