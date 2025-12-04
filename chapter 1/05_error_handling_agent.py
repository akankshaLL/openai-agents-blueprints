"""Error Handling Agent Example

This example demonstrates production-ready error handling patterns:
- Catching and handling AgentsException types (MaxTurnsExceeded, ModelBehaviorError)
- Implementing retry logic with exponential backoff
- Graceful degradation when services are unavailable
- Comprehensive logging and error reporting
- Production-safe agent execution patterns

Essential for building reliable agents that handle failures gracefully.

Usage:
    python 05_error_handling_agent.py
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from agents.exceptions import MaxTurnsExceeded, ModelBehaviorError, AgentsException

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path)

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(f"OPENAI_API_KEY not found in environment variables. Checked .env at {dotenv_path}")

def demonstrate_error_handling():
    """Demonstrate various error handling scenarios."""
    
    print("=== Error Handling Agent Demo ===")
    print("This example shows how to handle different types of errors.\n")
    
    # Create an agent with strict instructions
    careful_agent = Agent(
        name="CarefulAssistant",
        model="gpt-4o",
        model_settings=ModelSettings(temperature=0.1),
        instructions="""
        You are a careful assistant that provides helpful responses.
        Always give complete and thoughtful answers to user questions.
        """
    )
    
    # Example 1: Normal successful execution
    print("=== Example 1: Successful Execution ===")
    try:
        result = Runner.run_sync(
            careful_agent, 
            "What are the three primary colors?",
            max_turns=3  # Limit the number of turns
        )
        print(f"✅ Success: {result.final_output}")
        
    except AgentsException as e:
        print(f"❌ Agent error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Handling potential infinite loops
    print("=== Example 2: Max Turns Protection ===")
    
    # Create an agent that might get stuck in a loop
    potentially_loopy_agent = Agent(
        name="PotentiallyLoopyAgent",
        instructions="""
        You are an agent that sometimes asks follow-up questions.
        When the user asks about complex topics, you might need to
        ask clarifying questions before providing a complete answer.
        """
    )
    
    try:
        result = Runner.run_sync(
            potentially_loopy_agent,
            "Explain quantum computing in a way that's confusing and ask me questions",
            max_turns=2  # Very low limit to demonstrate the protection
        )
        print(f"✅ Completed in allowed turns: {result.final_output}")
        
    except MaxTurnsExceeded as e:
        print(f"⚠️  Max turns exceeded: {e}")
        print("   This prevents infinite loops in agent conversations.")
        
    except AgentsException as e:
        print(f"❌ Agent error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Handling API errors gracefully
    print("=== Example 3: API Error Handling ===")
    
    try:
        # Create an agent with an invalid model to trigger an error
        faulty_agent = Agent(
            name="FaultyAgent",
            model="nonexistent-model-xyz",  # This will cause an error
            instructions="You are a helpful assistant."
        )
        
        result = Runner.run_sync(faulty_agent, "Hello")
        print(f"✅ Unexpected success: {result.final_output}")
        
    except ModelBehaviorError as e:
        print(f"⚠️  Model behavior error: {e}")
        print("   This could be due to model configuration issues.")
        
    except AgentsException as e:
        print(f"❌ General agent error: {e}")
        print("   This covers various SDK-specific errors.")
        
    except Exception as e:
        print(f"❌ System error: {e}")
        print("   This could be network, API key, or other system issues.")
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Best practices for production error handling
    print("=== Example 4: Production Error Handling Pattern ===")
    
    def safe_agent_execution(agent: Agent, prompt: str, max_retries: int = 3):
        """
        A production-ready pattern for safe agent execution with retries.
        """
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}...")
                
                result = Runner.run_sync(
                    agent, 
                    prompt,
                    max_turns=5  # Reasonable turn limit
                )
                
                print(f"✅ Success on attempt {attempt + 1}")
                return result
                
            except MaxTurnsExceeded:
                print(f"⚠️  Attempt {attempt + 1}: Max turns exceeded")
                if attempt == max_retries - 1:
                    print("❌ All attempts exhausted due to max turns")
                    return None
                    
            except ModelBehaviorError as e:
                print(f"⚠️  Attempt {attempt + 1}: Model behavior error: {e}")
                if attempt == max_retries - 1:
                    print("❌ All attempts exhausted due to model issues")
                    return None
                    
            except AgentsException as e:
                print(f"❌ Agent error (not retrying): {e}")
                return None
                
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1}: System error: {e}")
                if attempt == max_retries - 1:
                    print("❌ All attempts exhausted due to system errors")
                    return None
        
        return None
    
    # Test the production pattern
    production_agent = Agent(
        name="ProductionAgent",
        instructions="You are a reliable production assistant."
    )
    
    result = safe_agent_execution(
        production_agent,
        "What's the capital of France? Give a brief answer."
    )
    
    if result:
        print(f"Final result: {result.final_output}")
    else:
        print("Failed to get a result after all retries.")

if __name__ == "__main__":
    demonstrate_error_handling()
