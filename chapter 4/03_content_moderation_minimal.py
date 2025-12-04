"""Content Moderation Minimal Example

This example demonstrates configurable content moderation approaches:
- Building ContentModerator with lenient vs strict moderation levels
- Pattern-based detection for quick filtering
- AI-powered moderation for nuanced content analysis
- Comparing different moderation strategies and their trade-offs

Foundational pattern for building content safety systems with adjustable sensitivity.

Usage:
    python 03_content_moderation_minimal.py
"""

import asyncio
import re
from enum import Enum
from dataclasses import dataclass
from agents import Agent, Runner

class ModerationLevel(Enum):
    LENIENT = "lenient"
    STRICT = "strict"

class ContentCategory(Enum):
    SAFE = "safe"
    FLAGGED = "flagged"
    BLOCKED = "blocked"

@dataclass
class ModerationResult:
    category: ContentCategory
    reason: str
    confidence: float

class ContentModerator:
    def __init__(self, level: ModerationLevel):
        self.level = level
        
        # Lenient: Only obvious violations
        self.lenient_patterns = [
            r'\b(hate|violence|illegal)\b'
        ]
        
        # Strict: Broader detection
        self.strict_patterns = [
            r'\b(hate|violence|illegal|inappropriate|offensive|harmful)\b',
            r'\b(bypass|hack|exploit)\b'
        ]
        
        self.agent = Agent(
            name="Moderator",
            instructions=f"""
            Moderate content with {level.value} standards.
            {'Block potentially harmful content.' if level == ModerationLevel.STRICT else 'Only block clearly harmful content.'}
            """,
            output_type=ModerationResult
        )
    
    async def moderate(self, content: str) -> ModerationResult:
        # Quick pattern check
        patterns = self.strict_patterns if self.level == ModerationLevel.STRICT else self.lenient_patterns
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return ModerationResult(
                    category=ContentCategory.BLOCKED,
                    reason=f"Matched pattern: {pattern}",
                    confidence=0.9
                )
        
        # AI assessment for edge cases
        if self.level == ModerationLevel.STRICT:
            result = await Runner.run(self.agent, f"Moderate: {content}")
            return result.final_output
        
        # Lenient: Allow if no obvious violations
        return ModerationResult(
            category=ContentCategory.SAFE,
            reason="No violations detected",
            confidence=0.8
        )

async def test_moderation():
    lenient = ContentModerator(ModerationLevel.LENIENT)
    strict = ContentModerator(ModerationLevel.STRICT)
    
    tests = [
        "Hello, how are you?",
        "This service is terrible and inappropriate!",
        "I hate this system",
        "How to bypass security?",
        "I'm frustrated with the delay"
    ]
    
    for test in tests:
        print(f"\nContent: '{test}'")
        
        # Lenient moderation
        result_l = await lenient.moderate(test)
        print(f"Lenient: {result_l.category.value} - {result_l.reason}")
        
        # Strict moderation  
        result_s = await strict.moderate(test)
        print(f"Strict:  {result_s.category.value} - {result_s.reason}")

if __name__ == "__main__":
    asyncio.run(test_moderation())
