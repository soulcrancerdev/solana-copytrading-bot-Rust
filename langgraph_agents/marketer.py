"""AI Marketer agent - Content strategy creation."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def create_strategy(research_data: Dict[str, Any], llm: ChatOpenAI) -> Dict[str, Any]:
    """
    Create content strategy based on research data.
    
    Args:
        research_data: Research data from AI Researcher
        llm: Language model instance
        
    Returns:
        Strategy dictionary
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert social media marketing strategist."),
        ("user", """Based on this market research:

{research_data}

Create a comprehensive social media content strategy including:
1. SMM goals and objectives
2. Content themes (5-7 themes)
3. Posting schedule (optimal times and frequency)
4. Target metrics and KPIs
5. Content mix recommendations

Format as structured strategy with actionable recommendations.""")
    ])
    
    chain = prompt | llm
    
    research_text = research_data.get("market_trends", "")
    
    response = chain.invoke({
        "research_data": research_text
    })
    
    return {
        "goals": response.content,
        "themes": ["business_tips", "industry_news", "product_updates", "behind_scenes", "user_stories"],
        "posting_schedule": {
            "frequency": "3-5 posts per week",
            "optimal_times": ["09:00", "13:00", "18:00"]
        },
        "target_metrics": {
            "engagement_rate": 0.05,
            "reach": 10000,
            "conversions": 100
        }
    }

