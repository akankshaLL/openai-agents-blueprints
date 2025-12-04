# test_setup.py
import os
from dotenv import load_dotenv
from agents import Agent, Runner

def test_environment():
    """Test that the development environment is properly configured."""
    
    # Load environment variables
    load_dotenv()
    
    # Verify API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Check your .env file.")
    
    if not api_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI API key format.")
    
    print("✅ Environment setup verified")
    print(f"✅ API key loaded: {api_key[:8]}...")
    
    # Test basic agent functionality
    test_agent = Agent(
        name="TestAgent",
        instructions="You are a test agent. Respond with 'Hello from the OpenAI Agents SDK!'"
    )
    
    print("✅ Agent created successfully")
    
    try:
        result = Runner.run_sync(test_agent, "Say hello")
        print(f"✅ Agent execution successful: {result.final_output}")
        return True
    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        return False

if __name__ == "__main__":
    test_environment()
