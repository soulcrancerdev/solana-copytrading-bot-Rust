"""AI Designer agent - Image generation."""

from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from openai import OpenAI
from config import get_settings

settings = get_settings()


def generate_image(
    content_text: str,
    style: str = "modern",
    llm: Optional[ChatOpenAI] = None
) -> Optional[str]:
    """
    Generate image using DALL-E based on content.
    
    Args:
        content_text: Text content to create image for
        style: Image style preference
        llm: Language model instance (optional, for prompt enhancement)
        
    Returns:
        Image URL or None if generation fails
    """
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        
        # Create image prompt
        image_prompt = f"Create a professional social media image for: {content_text[:200]}. Style: {style}, modern, clean design suitable for social media."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

