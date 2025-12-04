"""Live Edge Case Handling Example

This example demonstrates handling real-world problematic inputs:
- Building LiveEdgeCaseHandler for detecting and managing edge cases
- Testing actual agent responses to empty, vague, and malformed inputs
- Pattern detection for different types of problematic user behavior
- Measuring agent resilience and response quality under stress

Practical pattern for building robust agents that handle any user input gracefully.

Usage:
    python 07_edge_case_live.py
"""

import os
import asyncio
import re
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

class LiveEdgeCaseHandler:
    """Handle actual edge cases with real agent responses"""
    
    def __init__(self):
        self.edge_cases_handled = []
        self.patterns = {
            'empty': r'^\s*$',
            'vague': r'^(help|fix|broken|issue|problem)\.?$',
            'ambiguous': r'\b(it|that|this|they)\s*$',
            'excessive': r'(.)\1{10,}|[.!?]{5,}',
            'injection': r'[<>{}[\]\\]|script|alert',
            'stress_test': r'test.*(?:limit|boundary|edge)',
        }
        
        self.agent = Agent(
            name="RobustAssistant",
            instructions="""You are a resilient assistant that handles any input gracefully.
            
            For unclear inputs: Ask specific clarifying questions
            For vague requests: Provide helpful options
            For problematic inputs: Respond professionally
            For edge cases: Be adaptive and helpful
            
            Always maintain a helpful, professional tone."""
        )
    
    def detect_edge_case(self, input_text: str) -> str:
        """Detect what type of edge case this is"""
        for case_type, pattern in self.patterns.items():
            if re.search(pattern, input_text, re.IGNORECASE):
                return case_type
        return "normal"
    
    async def handle_edge_case(self, input_text: str) -> dict:
        """Handle edge case with actual agent response"""
        edge_type = self.detect_edge_case(input_text)
        
        print(f"🔍 Input: '{input_text[:80]}{'...' if len(input_text) > 80 else ''}'")
        print(f"📊 Edge Case Type: {edge_type}")
        
        try:
            # Get actual agent response
            result = await Runner.run(self.agent, input_text)
            response = result.final_output
            
            case_data = {
                "input": input_text,
                "edge_type": edge_type,
                "response": response,
                "handled": True,
                "response_length": len(response)
            }
            
            self.edge_cases_handled.append(case_data)
            
            print(f"✅ Agent Response: {response}")
            print(f"📏 Response Length: {len(response)} chars")
            
            return case_data
            
        except Exception as e:
            print(f"❌ Failed to handle: {str(e)}")
            return {
                "input": input_text,
                "edge_type": edge_type,
                "response": None,
                "handled": False,
                "error": str(e)
            }
    
    def get_handling_stats(self):
        """Get statistics on edge case handling"""
        total = len(self.edge_cases_handled)
        handled = sum(1 for case in self.edge_cases_handled if case["handled"])
        
        edge_types = {}
        for case in self.edge_cases_handled:
            edge_type = case["edge_type"]
            edge_types[edge_type] = edge_types.get(edge_type, 0) + 1
        
        avg_response_length = sum(case.get("response_length", 0) for case in self.edge_cases_handled if case["handled"]) / max(1, handled)
        
        return {
            "total_cases": total,
            "successfully_handled": handled,
            "success_rate": handled / max(1, total),
            "edge_types": edge_types,
            "avg_response_length": avg_response_length
        }

async def demo_live_edge_cases():
    """Demonstrate live edge case handling with real agent responses"""
    
    handler = LiveEdgeCaseHandler()
    
    # Real problematic inputs that agents encounter
    edge_cases = [
        "",  # Empty input
        "help",  # Extremely vague
        "it doesn't work",  # Ambiguous reference
        "AAAAAAAAAAAAAAAAAAA",  # Repetitive
        "???!!!???!!!???",  # Excessive punctuation
        "<script>alert('test')</script>",  # Injection attempt
        "test boundary limits maximum edge case",  # Stress testing
        "I need help with the thing from yesterday",  # Vague temporal reference
        "Can you fix my broken stuff please?",  # Multiple vague terms
        "Why won't this stupid thing work properly?",  # Frustrated + vague
        "Hello" * 100,  # Extremely repetitive
        "What is the meaning of life, universe, and everything, and also can you help me with my computer problem and also what's the weather?",  # Multiple unrelated requests
    ]
    
    print("🔧 LIVE EDGE CASE HANDLING DEMO")
    print("Testing actual agent responses to problematic inputs\n")
    
    for i, edge_case in enumerate(edge_cases, 1):
        print(f"--- Test Case {i} ---")
        await handler.handle_edge_case(edge_case)
        print("-" * 60)
        await asyncio.sleep(0.5)  # Rate limiting
    
    # Show comprehensive results
    stats = handler.get_handling_stats()
    print(f"\n📊 EDGE CASE HANDLING RESULTS:")
    print(f"Total Cases Tested: {stats['total_cases']}")
    print(f"Successfully Handled: {stats['successfully_handled']}")
    print(f"Success Rate: {stats['success_rate']:.1%}")
    print(f"Average Response Length: {stats['avg_response_length']:.0f} characters")
    print(f"\nEdge Case Types Encountered:")
    for edge_type, count in stats['edge_types'].items():
        print(f"  {edge_type}: {count} cases")
    
    # Show examples of good handling
    print(f"\n🎯 SUCCESSFUL HANDLING EXAMPLES:")
    successful_cases = [case for case in handler.edge_cases_handled if case["handled"] and case["response"]][:3]
    
    for case in successful_cases:
        print(f"\nInput: '{case['input'][:50]}{'...' if len(case['input']) > 50 else ''}'")
        print(f"Type: {case['edge_type']}")
        print(f"Response: {case['response'][:100]}{'...' if len(case['response']) > 100 else ''}")

if __name__ == "__main__":
    asyncio.run(demo_live_edge_cases())
