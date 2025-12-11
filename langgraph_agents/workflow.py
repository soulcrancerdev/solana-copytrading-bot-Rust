"""LangGraph workflow orchestration for multi-agent system."""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from config import get_settings

settings = get_settings()

# Initialize LLM
llm = ChatOpenAI(
    model=settings.openai_model,
    temperature=settings.openai_temperature,
    api_key=settings.openai_api_key,
)


class AgentState(TypedDict):
    """State shared across all agents."""
    business_id: int
    business_info: dict
    research_data: dict
    strategy: dict
    content: dict
    images: list
    moderation_result: dict
    approved: bool
    published: bool
    analytics: dict
    error: str


def researcher_node(state: AgentState) -> AgentState:
    """AI Researcher agent - Market research and analysis."""
    from .researcher import research_market

    try:
        research_result = research_market(
            business_info=state.get("business_info", {}),
            llm=llm
        )
        state["research_data"] = research_result
    except Exception as e:
        state["error"] = f"Researcher error: {str(e)}"
    
    return state


def marketer_node(state: AgentState) -> AgentState:
    """AI Marketer agent - Content strategy creation."""
    from .marketer import create_strategy

    try:
        strategy_result = create_strategy(
            research_data=state.get("research_data", {}),
            llm=llm
        )
        state["strategy"] = strategy_result
    except Exception as e:
        state["error"] = f"Marketer error: {str(e)}"
    
    return state


def copywriter_node(state: AgentState) -> AgentState:
    """AI Copywriter agent - Content generation."""
    from .copywriter import generate_content

    try:
        content_result = generate_content(
            strategy=state.get("strategy", {}),
            platform=state.get("platform", "telegram"),
            theme=state.get("theme", "general"),
            llm=llm
        )
        state["content"] = content_result
    except Exception as e:
        state["error"] = f"Copywriter error: {str(e)}"
    
    return state


def designer_node(state: AgentState) -> AgentState:
    """AI Designer agent - Image generation."""
    from .designer import generate_image

    try:
        image_result = generate_image(
            content_text=state.get("content", {}).get("text", ""),
            style=state.get("style", "modern"),
            llm=llm
        )
        state["images"] = [image_result] if image_result else []
    except Exception as e:
        state["error"] = f"Designer error: {str(e)}"
    
    return state


def moderator_node(state: AgentState) -> AgentState:
    """AI Moderator agent - Content review and approval."""
    from .moderator import moderate_content

    try:
        moderation_result = moderate_content(
            content=state.get("content", {}),
            brand_guidelines=state.get("business_info", {}).get("brand_guidelines", ""),
            llm=llm
        )
        state["moderation_result"] = moderation_result
        state["approved"] = moderation_result.get("approved", False)
    except Exception as e:
        state["error"] = f"Moderator error: {str(e)}"
        state["approved"] = False
    
    return state


def scheduler_node(state: AgentState) -> AgentState:
    """AI Scheduler agent - Content publishing."""
    from .scheduler import schedule_post

    try:
        if state.get("approved", False):
            publish_result = schedule_post(
                content=state.get("content", {}),
                images=state.get("images", []),
                platform=state.get("platform", "telegram"),
                scheduled_time=state.get("scheduled_time")
            )
            state["published"] = publish_result.get("success", False)
        else:
            state["published"] = False
    except Exception as e:
        state["error"] = f"Scheduler error: {str(e)}"
        state["published"] = False
    
    return state


def analytical_node(state: AgentState) -> AgentState:
    """AI Analytical agent - Performance analysis."""
    from .analytical import analyze_performance

    try:
        analytics_result = analyze_performance(
            post_id=state.get("post_id"),
            platform=state.get("platform", "telegram"),
            llm=llm
        )
        state["analytics"] = analytics_result
    except Exception as e:
        state["error"] = f"Analytical error: {str(e)}"
    
    return state


def should_approve(state: AgentState) -> str:
    """Conditional edge function for moderation approval."""
    if state.get("approved", False):
        return "approved"
    return "rejected"


def create_agent_workflow() -> StateGraph:
    """Create the LangGraph workflow for multi-agent system."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("marketer", marketer_node)
    workflow.add_node("copywriter", copywriter_node)
    workflow.add_node("designer", designer_node)
    workflow.add_node("moderator", moderator_node)
    workflow.add_node("scheduler", scheduler_node)
    workflow.add_node("analytical", analytical_node)

    # Define edges
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "marketer")
    workflow.add_edge("marketer", "copywriter")
    workflow.add_edge("copywriter", "designer")
    workflow.add_edge("designer", "moderator")
    
    # Conditional edge for moderation
    workflow.add_conditional_edges(
        "moderator",
        should_approve,
        {
            "approved": "scheduler",
            "rejected": "copywriter"  # Loop back for retry
        }
    )
    
    workflow.add_edge("scheduler", END)
    workflow.add_edge("analytical", END)

    return workflow.compile()

