import os
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

# Create an agent
agent = Agent(name="TestAgent", instructions="You are a helpful assistant.")

# For more control, you can manage conversation history explicitly
messages = [
    {"role": "user", "content": "My favorite color is blue."},
]

result1 = Runner.run_sync(agent, messages)

# Add the first interaction to the message history
messages.extend([
    {"role": "user", "content": "My favorite color is blue."},
    {"role": "assistant", "content": result1.final_output}
])

# Continue the conversation with explicit history
messages.append({"role": "user", "content": "What color do I like?"})
result2 = Runner.run_sync(agent, messages)

print("First response:", result1.final_output)
print("Second response:", result2.final_output)
