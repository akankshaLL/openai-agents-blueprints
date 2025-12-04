"""Structured Output Example

This example demonstrates extracting structured data from natural language:
- Using Pydantic models to define expected output structure
- Automatic data extraction and validation from user input
- Type-safe access to extracted information
- Converting unstructured text into structured, usable data

Perfect for building data extraction and form-filling agents.

Usage:
    python 03_structured_output.py
"""

import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import Agent, Runner

# Load environment variables
load_dotenv()

# Verify API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

if not api_key.startswith("sk-"):
    raise ValueError("Invalid OpenAI API key format.")

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    location: str

async def main():
    agent = Agent(
        name="DataExtractor",
        instructions="Extract person information from user input and return structured data.",
        output_type=PersonInfo
    )
    
    result = await Runner.run(
        agent,
        "Hi, I'm Sarah, a 28-year-old software engineer living in San Francisco."        
    )
    
    # result.final_output is now a PersonInfo object, not a string
    person = result.final_output
    print(f"Name: {person.name}")        # Name: Sarah
    print(f"Age: {person.age}")          # Age: 28
    print(f"Job: {person.occupation}")   # Job: software engineer
    print(f"City: {person.location}")    # City: San Francisco
    
    # Type-safe access
    if person.age > 25:
        print("Eligible for senior discount")

if __name__ == "__main__":
    asyncio.run(main())
