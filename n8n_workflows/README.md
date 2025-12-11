# n8n Workflows

This directory contains n8n workflow JSON files for the multi-agent social media automation system.

## Workflow Files

1. **01_main_content_pipeline.json** - Main content generation pipeline
   - Triggers: Schedule or Webhook
   - Agents: Researcher → Marketer → Copywriter → Designer → Moderator → Scheduler

2. **02_analytics_workflow.json** - Analytics and performance tracking
   - Triggers: Post published webhook
   - Agent: Analytical

## Importing Workflows

1. Open n8n UI: http://localhost:5678
2. Click "Workflows" → "Import from File"
3. Select the JSON file you want to import
4. Configure credentials and environment variables
5. Activate the workflow

## Workflow Structure

Each workflow follows this pattern:
- **Trigger**: Schedule or Webhook
- **Agent Nodes**: HTTP Request to LangGraph API
- **Database Nodes**: PostgreSQL operations
- **Conditional Logic**: IF nodes for approval/rejection
- **Error Handling**: On Error nodes

## Configuration

Before using workflows, ensure:
- ✅ Database is initialized
- ✅ FastAPI backend is running (port 8000)
- ✅ Environment variables are set in n8n
- ✅ Credentials are configured (OpenAI, platforms)

## Customization

You can modify workflows in n8n UI or edit JSON files directly. Remember to export updated workflows for version control.

