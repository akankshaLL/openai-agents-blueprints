"""Advanced Structured Output Example

This example demonstrates complex structured data extraction:
- Using Pydantic models with enums, validation, and nested structures
- Field constraints and validation (ge, le for numeric ranges)
- Complex business objects like project plans with multiple tasks
- Type-safe data access with automatic validation

Advanced pattern for building agents that return complex, validated business data.

Usage:
    python 04_structured_output_advanced.py
"""

import os
import asyncio
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    description: str
    priority: Priority
    estimated_hours: int = Field(ge=1, le=40)  # Between 1-40 hours
    tags: List[str] = []

class ProjectPlan(BaseModel):
    project_name: str
    deadline: str
    tasks: List[Task]
    total_estimated_hours: Optional[int] = None

async def create_project_plan():
    agent = Agent(
        name="ProjectPlanner",
        instructions="""
        Create a detailed project plan based on user requirements.
        Break down the project into specific tasks with priorities and time estimates.
        """,
        output_type=ProjectPlan  # Set the output type in the agent
    )
    
    user_request = """
    I need to build a todo app. It should have user authentication, 
    task management, and be ready in 2 weeks. Make it web-based.
    """
    
    result = await Runner.run(agent, user_request)
    
    plan = result.final_output  # Access the structured data
    print(f"Project: {plan.project_name}")
    print(f"Deadline: {plan.deadline}")
    print(f"Total Tasks: {len(plan.tasks)}")
    
    for i, task in enumerate(plan.tasks, 1):
        print(f"\n{i}. {task.title}")
        print(f"   Priority: {task.priority.value}")
        print(f"   Time: {task.estimated_hours}h")
        print(f"   Tags: {', '.join(task.tags)}")

async def main():
    print("=== Advanced Structured Output Demo ===")
    print("Creating a project plan for a todo app...\n")
    
    await create_project_plan()
    
    print(f"\n{'='*50}")
    print("Demo completed! Notice how the agent returned structured data")
    print("that we can easily access and work with programmatically.")

if __name__ == "__main__":
    asyncio.run(main())
