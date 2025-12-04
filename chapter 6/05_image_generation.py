"""Image Generation Tool Example

Shows how to use ImageGenerationTool for creating images:
- ImageGenerationTool for AI-powered image creation
- High-quality image generation with DALL-E
- Creative visual content generation
- Customizable image parameters

Usage:
    python 05_image_generation.py
"""

import asyncio
from agents import Agent, Runner, ImageGenerationTool

# Create creative assistant with image generation
creative_agent = Agent(
    name="Creative Assistant",
    instructions="""You are a creative assistant that can generate images 
    based on descriptions. Create detailed, high-quality images that match 
    user requests and provide helpful descriptions of what was created.""",
    tools=[
        ImageGenerationTool(
            tool_config={
                "type": "image_generation",
                "quality": "hd",
                "size": "1024x1024"
            }
        )
    ],
)

# Create marketing designer
marketing_designer = Agent(
    name="Marketing Designer",
    instructions="""You are a marketing designer who creates visual content 
    for campaigns. Generate professional images for marketing materials, 
    social media, and promotional content.""",
    tools=[
        ImageGenerationTool(
            tool_config={
                "type": "image_generation",
                "quality": "hd", 
                "size": "1792x1024"  # Wide format for marketing
            }
        )
    ],
)

# Create concept artist
concept_artist = Agent(
    name="Concept Artist",
    instructions="""You are a concept artist who creates visual concepts 
    and illustrations. Generate artistic images for creative projects, 
    character designs, and conceptual artwork.""",
    tools=[
        ImageGenerationTool(
            tool_config={
                "type": "image_generation",
                "quality": "hd",
                "size": "1024x1792"  # Portrait format for art
            }
        )
    ],
)

async def demo_image_generation():
    """Demonstrate image generation for different creative purposes"""
    
    requests = [
        ("creative_agent", "Create a serene landscape with mountains, a lake, and sunset colors"),
        ("marketing_designer", "Design a modern tech startup office space for a website banner"),
        ("concept_artist", "Create a fantasy character - a wise wizard with a magical staff"),
        ("creative_agent", "Generate an abstract art piece with vibrant colors and geometric shapes"),
        ("marketing_designer", "Create a product mockup showing a smartphone with a sleek design"),
        ("concept_artist", "Design a futuristic cityscape with flying cars and neon lights")
    ]
    
    print("🎨 IMAGE GENERATION DEMONSTRATION")
    print("Using ImageGenerationTool for AI-powered visual content creation")
    print("=" * 70)
    
    for i, (agent_type, request) in enumerate(requests, 1):
        # Select appropriate agent
        if agent_type == "creative_agent":
            agent = creative_agent
        elif agent_type == "marketing_designer":
            agent = marketing_designer
        else:
            agent = concept_artist
        
        print(f"\n{i}️⃣ Agent: {agent.name}")
        print(f"Request: {request}")
        print("-" * 50)
        
        try:
            result = await Runner.run(agent, request)
            print(f"Response: {result.final_output}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(demo_image_generation())
