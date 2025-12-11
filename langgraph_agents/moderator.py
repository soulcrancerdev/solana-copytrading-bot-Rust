"""AI Moderator agent - Content review and approval."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def moderate_content(
    content: Dict[str, Any],
    brand_guidelines: str = "",
    llm: ChatOpenAI = None
) -> Dict[str, Any]:
    """
    Review content for brand consistency, accuracy, and compliance.
    
    Args:
        content: Content dictionary from AI Copywriter
        brand_guidelines: Brand guidelines text
        llm: Language model instance
        
    Returns:
        Moderation result with approval status
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a content moderator ensuring brand consistency, factual accuracy, and compliance."),
        ("user", """Review this social media content:

Content: {content_text}

Brand Guidelines: {brand_guidelines}

Check for:
1. Brand consistency (tone, style, messaging)
2. Factual accuracy
3. Stop words or inappropriate content
4. Platform guidelines compliance
5. Overall quality

Respond in this format:
STATUS: APPROVED or REJECTED
REASON: [detailed explanation]
SUGGESTIONS: [if rejected, provide improvement suggestions]""")
    ])
    
    chain = prompt | llm
    
    content_text = content.get("text", "")
    
    response = chain.invoke({
        "content_text": content_text,
        "brand_guidelines": brand_guidelines or "Professional, friendly, value-focused."
    })
    
    response_text = response.content
    approved = "APPROVED" in response_text.upper()
    
    return {
        "approved": approved,
        "reason": response_text,
        "suggestions": "" if approved else response_text
    }

