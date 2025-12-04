"""Code Interpreter Tool Example

Shows how to use CodeInterpreterTool for data analysis:
- CodeInterpreterTool for Python code execution
- Data analysis and visualization capabilities
- Statistical calculations and insights
- Secure code execution environment

Usage:
    python 03_code_interpreter.py
"""

import asyncio
from agents import Agent, Runner, CodeInterpreterTool

# Create data analyst with code interpreter
data_analyst = Agent(
    name="Data Analyst",
    instructions="""You are a data analyst who can perform complex calculations 
    and create visualizations. Use Python code to analyze data and generate 
    insights. Always explain your methodology and findings clearly.""",
    tools=[
        CodeInterpreterTool(
            tool_config={
                "type": "code_interpreter",
                "container": {"type": "auto"}
            }
        )
    ],
)

# Create math tutor with code capabilities
math_tutor = Agent(
    name="Math Tutor",
    instructions="""You are a math tutor who can solve complex problems step by step.
    Use Python code to demonstrate calculations, create graphs, and verify solutions.
    Always show your work and explain each step.""",
    tools=[
        CodeInterpreterTool(
            tool_config={
                "type": "code_interpreter",
                "container": {"type": "auto"}
            }
        )
    ],
)

async def demo_code_interpreter():
    """Demonstrate code interpreter for data analysis and math"""
    
    tasks = [
        ("data_analyst", "Analyze this sales data and create a visualization: Q1: $50000, Q2: $65000, Q3: $45000, Q4: $80000. Show trends and calculate growth rates."),
        ("math_tutor", "Solve the quadratic equation x² - 5x + 6 = 0 and plot the function"),
        ("data_analyst", "Calculate statistics for this dataset: [23, 45, 67, 34, 56, 78, 23, 45, 67, 89]. Find mean, median, mode, and standard deviation."),
        ("math_tutor", "Create a visualization showing the relationship between sine and cosine functions from 0 to 2π"),
        ("data_analyst", "Generate a random dataset of 100 points and perform linear regression analysis")
    ]
    
    print("🐍 CODE INTERPRETER DEMONSTRATION")
    print("Using CodeInterpreterTool for data analysis and calculations")
    print("=" * 70)
    
    for i, (agent_type, task) in enumerate(tasks, 1):
        agent = data_analyst if agent_type == "data_analyst" else math_tutor
        
        print(f"\n{i}️⃣ Agent: {agent.name}")
        print(f"Task: {task}")
        print("-" * 50)
        
        try:
            result = await Runner.run(agent, task)
            print(f"Response: {result.final_output}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_code_interpreter())
