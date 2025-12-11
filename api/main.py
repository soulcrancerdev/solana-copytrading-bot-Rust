"""FastAPI main application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from config import get_settings

from langgraph_agents.workflow import create_agent_workflow, AgentState

settings = get_settings()

app = FastAPI(
    title="Multi-Agent Social Media Automation API",
    description="API for LangGraph agents integrated with n8n workflows",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow
workflow = create_agent_workflow()


# Request Models
class ResearcherRequest(BaseModel):
    business_id: int


class MarketerRequest(BaseModel):
    research_id: int


class CopywriterRequest(BaseModel):
    strategy_id: int
    platform: str = "telegram"
    theme: str = "general"


class DesignerRequest(BaseModel):
    content_text: str
    style: str = "modern"


class ModeratorRequest(BaseModel):
    content_id: int
    brand_guidelines: Optional[str] = None


class SchedulerRequest(BaseModel):
    content_id: int
    platform: str
    scheduled_time: Optional[str] = None


class AnalyticalRequest(BaseModel):
    post_id: int


# Health Check
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "multi-agent-api"}


@app.get("/api/v1/status")
async def status():
    """Get API status."""
    return {
        "status": "running",
        "version": "1.0.0",
        "agents": [
            "researcher",
            "marketer",
            "copywriter",
            "designer",
            "moderator",
            "scheduler",
            "analytical"
        ]
    }


# Agent Endpoints
@app.post("/api/v1/agents/researcher")
async def trigger_researcher(request: ResearcherRequest):
    """Trigger AI Researcher agent."""
    try:
        initial_state: AgentState = {
            "business_id": request.business_id,
            "business_info": {},
            "research_data": {},
            "strategy": {},
            "content": {},
            "images": [],
            "moderation_result": {},
            "approved": False,
            "published": False,
            "analytics": {},
            "error": ""
        }
        
        result = workflow.invoke(initial_state)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/marketer")
async def trigger_marketer(request: MarketerRequest):
    """Trigger AI Marketer agent."""
    try:
        # In production, fetch research_data from database
        initial_state: AgentState = {
            "business_id": 0,
            "business_info": {},
            "research_data": {"research_id": request.research_id},
            "strategy": {},
            "content": {},
            "images": [],
            "moderation_result": {},
            "approved": False,
            "published": False,
            "analytics": {},
            "error": ""
        }
        
        # Run from marketer node
        result = workflow.invoke(initial_state)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/copywriter")
async def trigger_copywriter(request: CopywriterRequest):
    """Trigger AI Copywriter agent."""
    try:
        initial_state: AgentState = {
            "business_id": 0,
            "business_info": {},
            "research_data": {},
            "strategy": {"strategy_id": request.strategy_id},
            "content": {},
            "images": [],
            "moderation_result": {},
            "approved": False,
            "published": False,
            "analytics": {},
            "error": "",
            "platform": request.platform,
            "theme": request.theme
        }
        
        result = workflow.invoke(initial_state)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/designer")
async def trigger_designer(request: DesignerRequest):
    """Trigger AI Designer agent."""
    try:
        from langgraph_agents.designer import generate_image
        
        image_url = generate_image(
            content_text=request.content_text,
            style=request.style
        )
        
        return {
            "success": image_url is not None,
            "image_url": image_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/moderator")
async def trigger_moderator(request: ModeratorRequest):
    """Trigger AI Moderator agent."""
    try:
        from langgraph_agents.moderator import moderate_content
        
        # In production, fetch content from database
        content = {"text": "Sample content", "content_id": request.content_id}
        
        result = moderate_content(
            content=content,
            brand_guidelines=request.brand_guidelines or ""
        )
        
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/scheduler")
async def trigger_scheduler(request: SchedulerRequest):
    """Trigger AI Scheduler agent."""
    try:
        from langgraph_agents.scheduler import schedule_post
        from datetime import datetime
        
        scheduled_time = None
        if request.scheduled_time:
            scheduled_time = datetime.fromisoformat(request.scheduled_time)
        
        # In production, fetch content from database
        content = {"text": "Sample content", "content_id": request.content_id}
        
        result = schedule_post(
            content=content,
            images=[],
            platform=request.platform,
            scheduled_time=scheduled_time
        )
        
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/analytical")
async def trigger_analytical(request: AnalyticalRequest):
    """Trigger AI Analytical agent."""
    try:
        from langgraph_agents.analytical import analyze_performance
        
        result = analyze_performance(
            post_id=request.post_id,
            platform="telegram"
        )
        
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Webhook Endpoints (for n8n)
@app.post("/webhook/content-approved")
async def webhook_content_approved(data: Dict[str, Any]):
    """Webhook for approved content from n8n."""
    # Trigger scheduler
    return {"success": True, "message": "Content approved, scheduling..."}


@app.post("/webhook/content-rejected")
async def webhook_content_rejected(data: Dict[str, Any]):
    """Webhook for rejected content from n8n."""
    # Trigger copywriter retry
    return {"success": True, "message": "Content rejected, regenerating..."}


@app.post("/webhook/post-published")
async def webhook_post_published(data: Dict[str, Any]):
    """Webhook for published post from n8n."""
    # Trigger analytics
    return {"success": True, "message": "Post published, analytics scheduled..."}


@app.post("/webhook/analytics-ready")
async def webhook_analytics_ready(data: Dict[str, Any]):
    """Webhook for analytics ready from n8n."""
    return {"success": True, "message": "Analytics processed"}


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )

