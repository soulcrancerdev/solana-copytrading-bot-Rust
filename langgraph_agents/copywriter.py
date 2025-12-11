"""AI Copywriter agent - Content generation."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def generate_content(
    strategy: Dict[str, Any],
    platform: str = "telegram",
    theme: str = "general",
    llm: ChatOpenAI = None
) -> Dict[str, Any]:
    """
    Generate social media content text.
    
    Args:
        strategy: Content strategy from AI Marketer
        platform: Target platform (telegram, vk, twitter, etc.)
        theme: Content theme
        llm: Language model instance
        
    Returns:
        Content dictionary with text and variations
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert social media copywriter who creates engaging, platform-optimized content."),
        ("user", """Write a social media post for {platform} platform.

Theme: {theme}
Strategy Context: {strategy}

Requirements:
- Platform-optimized (consider character limits and audience)
- Engaging and valuable
- Include a call-to-action
- Use appropriate tone for the platform

Generate the main post text and 2 alternative variations for A/B testing.""")
    ])
    
    chain = prompt | llm
    
    strategy_text = strategy.get("goals", "")
    
    response = chain.invoke({
        "platform": platform,
        "theme": theme,
        "strategy": strategy_text
    })
    
    # Extract variations from response
    content_text = response.content
    
    return {
        "text": content_text,
        "variations": [
            content_text,
            content_text + "\n\nWhat do you think?",
            content_text + "\n\nShare your thoughts below!"
        ],
        "platform": platform,
        "theme": theme
    }

