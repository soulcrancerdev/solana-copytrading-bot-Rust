"""Test individual agents."""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langgraph_agents.workflow import create_agent_workflow, AgentState
from config import get_settings

settings = get_settings()


def test_researcher():
    """Test AI Researcher agent."""
    print("🔍 Testing AI Researcher...")
    
    workflow = create_agent_workflow()
    
    initial_state: AgentState = {
        "business_id": 1,
        "business_info": {
            "company_name": "Tech Startup Inc",
            "industry": "Technology",
            "target_audience": "Tech enthusiasts and developers"
        },
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
    
    try:
        result = workflow.invoke(initial_state)
        print("✅ Researcher test completed")
        print(f"Research data keys: {list(result.get('research_data', {}).keys())}")
        return True
    except Exception as e:
        print(f"❌ Researcher test failed: {str(e)}")
        return False


def test_full_workflow():
    """Test full workflow."""
    print("🚀 Testing full workflow...")
    
    workflow = create_agent_workflow()
    
    initial_state: AgentState = {
        "business_id": 1,
        "business_info": {
            "company_name": "Test Company",
            "industry": "Technology",
            "target_audience": "Developers",
            "brand_guidelines": "Professional, friendly"
        },
        "research_data": {},
        "strategy": {},
        "content": {},
        "images": [],
        "moderation_result": {},
        "approved": False,
        "published": False,
        "analytics": {},
        "error": "",
        "platform": "telegram",
        "theme": "business_tips"
    }
    
    try:
        result = workflow.invoke(initial_state)
        print("✅ Full workflow test completed")
        print(f"Final state keys: {list(result.keys())}")
        print(f"Approved: {result.get('approved', False)}")
        print(f"Published: {result.get('published', False)}")
        return True
    except Exception as e:
        print(f"❌ Full workflow test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="Test agents")
    parser.add_argument("--agent", choices=["researcher", "marketer", "copywriter", "all"], default="all")
    parser.add_argument("--workflow", action="store_true", help="Test full workflow")
    
    args = parser.parse_args()
    
    if args.workflow:
        test_full_workflow()
    elif args.agent == "researcher":
        test_researcher()
    elif args.agent == "all":
        print("Testing all agents...")
        test_researcher()
        # Add more agent tests here
    else:
        print(f"Testing {args.agent} agent...")
        # Add specific agent tests


if __name__ == "__main__":
    main()

