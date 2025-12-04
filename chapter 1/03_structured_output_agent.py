"""Structured Output Agent Example

This example demonstrates how to get structured data from agents using Pydantic models:
- Defining response schemas with Pydantic BaseModel classes
- Using output_type parameter to enforce structured responses
- Accessing typed data instead of raw text responses
- Field validation and documentation with Pydantic Field
- Converting structured data to JSON for storage/APIs

Essential for building agents that integrate with databases, APIs, and structured workflows.

Usage:
    python 03_structured_output_agent.py
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from agents import Agent, Runner, ModelSettings

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path)

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(f"OPENAI_API_KEY not found in environment variables. Checked .env at {dotenv_path}")

class TaskBreakdown(BaseModel):
    """Structure for task breakdown responses."""
    main_task: str = Field(description="The primary task to accomplish")
    subtasks: List[str] = Field(description="List of smaller tasks needed to complete the main task")
    estimated_time: str = Field(description="Estimated time to complete all tasks")
    difficulty_level: str = Field(description="Easy, Medium, Hard, or Expert")
    required_skills: List[str] = Field(description="Skills needed to complete the task")

def main():
    print("=== Structured Output Agent Demo ===")
    print("This agent returns structured data using Pydantic models.\n")
    
    # Create an agent that outputs structured data
    planning_agent = Agent(
        name="TaskPlanner",
        model="gpt-4o",
        model_settings=ModelSettings(temperature=0.2),  # Lower temperature for more consistent structure
        instructions="""
        You are an expert project planner. When given a task or project,
        break it down into manageable subtasks with time estimates.
        
        Analyze the complexity and provide a realistic assessment of
        the skills and time required to complete the work.
        """,
        output_type=TaskBreakdown  # This tells the agent to return structured data
    )
    
    # Example task to break down
    user_task = "Build a personal website portfolio to showcase my programming projects"
    
    print(f"Task to analyze: {user_task}\n")
    print("Running planning agent...")
    
    # Execute the agent
    result = Runner.run_sync(planning_agent, user_task)
    
    # The result.final_output is now a TaskBreakdown object, not a string
    task_plan: TaskBreakdown = result.final_output
    
    # Display the structured results
    print("\n=== TASK BREAKDOWN ===")
    print(f"Main Task: {task_plan.main_task}")
    print(f"Difficulty: {task_plan.difficulty_level}")
    print(f"Estimated Time: {task_plan.estimated_time}")
    
    print("\nSubtasks:")
    for i, subtask in enumerate(task_plan.subtasks, 1):
        print(f"  {i}. {subtask}")
    
    print("\nRequired Skills:")
    for skill in task_plan.required_skills:
        print(f"  • {skill}")
    
    print("\n=== TECHNICAL DETAILS ===")
    print(f"Response Type: {type(task_plan)}")
    print(f"Is Pydantic Model: {isinstance(task_plan, BaseModel)}")
    print(f"Raw JSON: {task_plan.model_dump_json(indent=2)}")

if __name__ == "__main__":
    main()
