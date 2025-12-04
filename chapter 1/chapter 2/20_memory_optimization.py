"""Memory Optimization Example

This example demonstrates conversation memory optimization techniques:
- Building ContextOptimizer for managing conversation history length
- Token-based trimming to stay within model context limits
- Preserving important context while removing redundant information
- Performance optimization for long-running conversations

Essential pattern for building scalable conversational agents with long sessions.

Usage:
    python 20_memory_optimization.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

class ContextOptimizer:
    """Optimize conversation context for performance."""
    
    def __init__(self, max_context_length: int = 10):
        self.max_context_length = max_context_length
    
    def optimize_conversation_history(self, history: list) -> list:
        """Optimize conversation history to maintain performance."""
        
        if len(history) <= self.max_context_length:
            return history
        
        # Keep system message and recent interactions
        system_messages = [msg for msg in history if msg.get("role") == "system"]
        other_messages = [msg for msg in history if msg.get("role") != "system"]
        
        # Keep most recent messages
        recent_messages = other_messages[-(self.max_context_length - len(system_messages)):]
        
        return system_messages + recent_messages
    
    def estimate_token_count(self, text: str) -> int:
        """Rough estimation of token count."""
        # Simple approximation: ~4 characters per token
        return len(text) // 4
    
    def trim_by_token_limit(self, history: list, max_tokens: int = 4000) -> list:
        """Trim conversation history by estimated token count."""
        
        total_tokens = 0
        trimmed_history = []
        
        # Process in reverse order to keep most recent messages
        for message in reversed(history):
            content = str(message.get("content", ""))
            message_tokens = self.estimate_token_count(content)
            
            if total_tokens + message_tokens <= max_tokens:
                trimmed_history.insert(0, message)
                total_tokens += message_tokens
            else:
                break
        
        return trimmed_history

# Usage example
def demonstrate_context_optimization():
    optimizer = ContextOptimizer(max_context_length=5)
    
    # Simulate a conversation history
    history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": "Hello! How can I help you today?"},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": "Why did the chicken cross the road? To get to the other side!"},
        {"role": "user", "content": "Another one, please."},
        {"role": "assistant", "content": "Why don't scientists trust atoms? Because they make up everything!"},
        {"role": "user", "content": "Thanks!"},
    ]
    
    print("Original conversation length:", len(history))
    optimized = optimizer.optimize_conversation_history(history)
    print("Optimized by context length:", len(optimized))
    trimmed = optimizer.trim_by_token_limit(history, max_tokens=30)
    print("Trimmed by token limit:", len(trimmed))
    print("Trimmed conversation:")
    for msg in trimmed:
        print(f"{msg['role']}: {msg['content']}")

if __name__ == "__main__":
    demonstrate_context_optimization()
