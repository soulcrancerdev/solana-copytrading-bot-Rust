"""AI Researcher agent - Market research and analysis."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def research_market(business_info: Dict[str, Any], llm: ChatOpenAI) -> Dict[str, Any]:
    """
    Research market trends, competitors, and insights.
    
    Args:
        business_info: Business information dictionary
        llm: Language model instance
        
    Returns:
        Research data dictionary
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert market researcher specializing in social media trends and competitor analysis."),
        ("user", """Research and analyze the market for the following business:

Company: {company_name}
Industry: {industry}
Target Audience: {target_audience}

Provide a comprehensive analysis including:
1. Current market trends in this industry
2. Competitor analysis (top 3-5 competitors)
3. Target audience insights and preferences
4. Content opportunities and gaps
5. Recommended content themes

Format your response as structured data with clear sections.""")
    ])
    
    chain = prompt | llm
    
    company_name = business_info.get("company_name", "Unknown")
    industry = business_info.get("industry", "General")
    target_audience = business_info.get("target_audience", "General audience")
    
    response = chain.invoke({
        "company_name": company_name,
        "industry": industry,
        "target_audience": target_audience
    })
    
    return {
        "market_trends": response.content,
        "competitor_analysis": "",
        "insights": "",
        "recommendations": ""
    }

