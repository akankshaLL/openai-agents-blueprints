"""
Correct way to use Vision with OpenAI Agents SDK
Based on GitHub issue #159 - proper input format required
"""

import asyncio
import base64
import requests
from agents import Agent, Runner, ModelSettings

def encode_image_from_url(image_url: str) -> str:
    """Download and encode image from URL to base64"""
    response = requests.get(image_url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode('utf-8')

def encode_image_from_file(image_path: str) -> str:
    """Encode local image file to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def analyze_image_correct(image_url: str, question: str):
    """CORRECT way to analyze images with Agents SDK"""
    
    # Create vision-enabled agent
    agent = Agent(
        name="Vision Agent",
        model="gpt-4o",  # Vision-capable model
        model_settings=ModelSettings(temperature=0.1, max_tokens=1024),
        instructions="You can see and analyze images. Describe what you observe accurately and answer questions about the image."
    )
    
    # Get base64 image
    if image_url.startswith('http'):
        base64_image = encode_image_from_url(image_url)
        image_data_url = f"data:image/jpeg;base64,{base64_image}"
    else:
        # Assume it's a file path
        base64_image = encode_image_from_file(image_url)
        image_data_url = f"data:image/jpeg;base64,{base64_image}"
    
    # CORRECT format - use structured input with separate text and image components
    result = await Runner.run(agent, input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": question},
                {"type": "input_image", "image_url": image_data_url}
            ]
        }
    ])
    
    return result.final_output

async def main():    
    print("Using proper input format for OpenAI Agents SDK\n")    
    test_image = "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600"
    
    result = await analyze_image_correct(
        image_url=test_image,
        question="What do you see in this image? What color is it and what text is visible?"
    )
    
    print("="*50)
    print("🖼️ VISION ANALYSIS RESULT:")
    print("="*50)
    print(result)
    print("="*50)
    
    # Test with a real photo amd tricky prompt
    print("\n" + "─"*50 + "\n")
    
    real_image = "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400"
    
    result2 = await analyze_image_correct(
        image_url=real_image,
        question="Describe this vehicle - what type, color, and any notable features you can see."
    )
    
    print("🚗 REAL IMAGE ANALYSIS:")
    print("="*50)
    print(result2)
    print("="*50)



if __name__ == "__main__":
    print("✅ Correct Vision Setup:")
    print("1. Set OPENAI_API_KEY environment variable")
    print("2. pip install openai-agents requests")
    print("3. Use proper input format with input_text and input_image types\n")
    
    asyncio.run(main())
