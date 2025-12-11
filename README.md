# 🤖 Multi-Agent Social Media Automation System

> **Hybrid n8n + LangGraph Approach** - Production-ready AI-powered social media automation

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange.svg)](https://github.com/langchain-ai/langgraph)
[![n8n](https://img.shields.io/badge/n8n-Self--hosted-purple.svg)](https://n8n.io/)

## 🎯 Overview

A sophisticated multi-agent system that automates social media content creation, scheduling, and publishing using **7 specialized AI agents** working in harmony. Built with the recommended **Hybrid n8n + LangGraph** architecture for maximum flexibility and speed.

### Why This Architecture?

- ✅ **Fast Development**: 3-4 weeks vs 2-3 months for pure code
- ✅ **Visual Workflows**: n8n provides intuitive workflow management
- ✅ **Powerful AI**: LangGraph handles complex agent reasoning
- ✅ **Cost-Effective**: ~$80-375/month vs $19,900 RUB/month alternatives
- ✅ **Production-Ready**: Scalable, maintainable, and extensible

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      n8n Workflows                           │
│  (Orchestration, Scheduling, API Integrations, Triggers)     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/Webhooks
┌──────────────────────▼──────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         LangGraph Agent Orchestration                  │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │Researcher│→ │ Marketer │→ │Copywriter│→ ...        │ │
│  │  └──────────┘  └──────────┘  └──────────┘            │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              PostgreSQL Database                             │
│  (Business Info, Research, Content, Analytics)               │
└─────────────────────────────────────────────────────────────┘
```

### The 7 AI Agents

1. **🔍 AI Researcher** - Market research, trend analysis, competitor audit
2. **📊 AI Marketer** - Content strategy, SMM goals, content planning
3. **✍️ AI Copywriter** - Text generation, variations, A/B testing ideas
4. **🎨 AI Designer** - Visual content, layouts, image generation (DALL-E)
5. **✅ AI Moderator** - Fact-checking, brand consistency, approval workflow
6. **📅 AI Scheduler** - Automatic publication via platform APIs
7. **📈 AI Analytical** - Metrics collection, pattern analysis, ROI/KPI

---

## 🚀 Quick Start

> **For a faster setup, see [QUICKSTART.md](./QUICKSTART.md) - Get running in 5 minutes!**

### Prerequisites

- Python 3.9+
- Docker & Docker Compose (for n8n and PostgreSQL)
- OpenAI API key
- Platform API credentials (Telegram, VK, etc.)

### 1. Clone & Setup

```bash
cd multi_agent_social_media_automation

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start Infrastructure

```bash
# Start PostgreSQL and n8n
docker-compose up -d

# Wait for services to be ready (30 seconds)
```

### 3. Initialize Database

```bash
# Run database migrations
psql -h localhost -U postgres -d social_media < database/schema.sql

# Or use Python script
python scripts/init_database.py
```

### 4. Start LangGraph API

```bash
# Start FastAPI backend
uvicorn api.main:app --reload --port 8000
```

### 5. Configure n8n

1. Open http://localhost:5678
2. Import workflows from `n8n_workflows/` directory
3. Configure environment variables in n8n settings
4. Test each workflow individually

### 6. Run Your First Workflow

```bash
# Trigger via API
curl -X POST http://localhost:8000/api/v1/trigger/researcher

# Or use n8n's manual trigger
```

---

## 📁 Project Structure

```
multi_agent_social_media_automation/
├── README.md                 # This file
├── docker-compose.yml         # Docker services (n8n, PostgreSQL)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
│
├── langgraph_agents/         # LangGraph agent implementations
│   ├── __init__.py
│   ├── researcher.py         # AI Researcher agent
│   ├── marketer.py           # AI Marketer agent
│   ├── copywriter.py         # AI Copywriter agent
│   ├── designer.py           # AI Designer agent
│   ├── moderator.py          # AI Moderator agent
│   ├── scheduler.py          # AI Scheduler agent
│   ├── analytical.py        # AI Analytical agent
│   └── workflow.py           # LangGraph state graph orchestration
│
├── api/                      # FastAPI backend
│   ├── __init__.py
│   ├── main.py              # FastAPI app & routes
│   └── webhooks.py           # Webhook endpoints for n8n
│
├── n8n_workflows/            # n8n workflow JSON files
│   ├── 01_ai_researcher.json
│   ├── 02_ai_marketer.json
│   ├── 03_ai_copywriter.json
│   ├── 04_ai_designer.json
│   ├── 05_ai_moderator.json
│   ├── 06_ai_scheduler.json
│   └── 07_ai_analytical.json
│
├── database/                 # Database schema & migrations
│   ├── schema.sql            # PostgreSQL schema
│   └── migrations/           # Database migration scripts
│
├── config/                   # Configuration files
│   ├── __init__.py
│   └── settings.py           # App settings & constants
│
└── scripts/                  # Utility scripts
    ├── init_database.py      # Database initialization
    └── test_agents.py        # Test individual agents
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```bash
# OpenAI API
OPENAI_API_KEY=sk-...

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/social_media

# Platform Credentials
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
VK_ACCESS_TOKEN=...
VK_GROUP_ID=...

# n8n
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=yourpassword
N8N_ENCRYPTION_KEY=your-encryption-key

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### n8n Configuration

1. **Access n8n**: http://localhost:5678
2. **Set Credentials**: Go to Settings → Credentials
3. **Import Workflows**: Use the JSON files in `n8n_workflows/`
4. **Configure Webhooks**: Update webhook URLs to point to your API

---

## 🔄 Workflow Flow

### Content Generation Pipeline

```
1. Schedule Trigger (n8n)
   ↓
2. AI Researcher (LangGraph via API)
   → Research market trends & competitors
   → Save to database
   ↓
3. AI Marketer (LangGraph via API)
   → Create content strategy
   → Define themes & goals
   ↓
4. AI Copywriter (LangGraph via API)
   → Generate text content
   → Create variations for A/B testing
   ↓
5. AI Designer (n8n OpenAI node)
   → Generate images with DALL-E
   → Process & optimize images
   ↓
6. AI Moderator (LangGraph via API)
   → Review content quality
   → Check brand guidelines
   → Decision: Approve/Reject
   ↓
7a. If Approved → AI Scheduler (n8n)
    → Publish to platforms
    → Save published post
    ↓
7b. If Rejected → Loop back to Copywriter
   ↓
8. AI Analytical (LangGraph via API)
   → Collect metrics after 24h
   → Analyze performance
   → Generate recommendations
   → Update strategy (feedback loop)
```

---

## 📡 API Endpoints

### LangGraph Agent Endpoints

```bash
# Trigger AI Researcher
POST /api/v1/agents/researcher
Body: { "business_id": 1 }

# Trigger AI Marketer
POST /api/v1/agents/marketer
Body: { "research_id": 123 }

# Trigger AI Copywriter
POST /api/v1/agents/copywriter
Body: { "strategy_id": 456, "platform": "telegram", "theme": "business_tips" }

# Trigger AI Designer
POST /api/v1/agents/designer
Body: { "content_text": "...", "style": "modern" }

# Trigger AI Moderator
POST /api/v1/agents/moderator
Body: { "content_id": 789, "brand_guidelines": "..." }

# Trigger AI Scheduler
POST /api/v1/agents/scheduler
Body: { "content_id": 789, "platform": "telegram", "scheduled_time": "2024-01-01T10:00:00" }

# Trigger AI Analytical
POST /api/v1/agents/analytical
Body: { "post_id": 101112 }
```

### Webhook Endpoints (for n8n)

```bash
# Receive webhook from n8n
POST /webhook/content-approved
POST /webhook/content-rejected
POST /webhook/post-published
POST /webhook/analytics-ready
```

### Health & Status

```bash
GET /health
GET /api/v1/status
GET /api/v1/agents/status
```

---

## 🧪 Testing

### Test Individual Agents

```bash
# Test Researcher
python scripts/test_agents.py --agent researcher

# Test Full Workflow
python scripts/test_agents.py --workflow full
```

### Test API Endpoints

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/agents/researcher \
  -H "Content-Type: application/json" \
  -d '{"business_id": 1}'

# Using Python
python scripts/test_api.py
```

### Test n8n Workflows

1. Open n8n UI
2. Click "Execute Workflow" on any workflow
3. Check execution logs
4. Verify database entries

---

## 📊 Database Schema

Key tables:

- `business_info` - Company/business information
- `research_data` - Market research results
- `content_strategy` - Marketing strategies
- `generated_content` - Generated posts (draft/approved/rejected)
- `published_posts` - Published content
- `analytics` - Performance metrics
- `recommendations` - AI-generated recommendations

See `database/schema.sql` for full schema.

---

## 🔧 Development

### Adding a New Agent

1. **Create agent file** in `langgraph_agents/`:

```python
# langgraph_agents/new_agent.py
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    input_data: str
    output_data: str

def new_agent_node(state: AgentState) -> AgentState:
    # Your agent logic here
    return state
```

2. **Add to workflow** in `langgraph_agents/workflow.py`
3. **Create API endpoint** in `api/main.py`
4. **Create n8n workflow** in `n8n_workflows/`

### Adding a New Platform

1. **Create adapter** (reuse from `social_media_automation/platform_adapters/`)
2. **Add to scheduler** in `langgraph_agents/scheduler.py`
3. **Update n8n workflow** `06_ai_scheduler.json`

---

## 🚢 Deployment

### Production Setup

1. **Use managed PostgreSQL** (AWS RDS, DigitalOcean, etc.)
2. **Deploy FastAPI** (Gunicorn + Nginx, or Docker)
3. **Deploy n8n** (Docker, or n8n Cloud)
4. **Set up monitoring** (Prometheus, Grafana)
5. **Configure backups** (Database + n8n workflows)

### Docker Production

```bash
# Build and run
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f
```

### Environment-Specific Configs

- `.env.development` - Local development
- `.env.staging` - Staging environment
- `.env.production` - Production environment

---

## 📈 Monitoring & Analytics

### Built-in Analytics

- **Performance Reports**: `/api/v1/analytics/report`
- **Agent Metrics**: Track execution times, success rates
- **Content Performance**: Engagement rates, top posts
- **Cost Tracking**: API usage, costs per post

### Logging

- **Application Logs**: `logs/app.log`
- **Agent Logs**: `logs/agents.log`
- **API Logs**: FastAPI automatic logging

### Alerts

Configure alerts for:
- Failed agent executions
- High API costs
- Low engagement rates
- Database connection issues

---

## 💰 Cost Breakdown

**Monthly Costs (Estimated):**

- n8n: **$0** (self-hosted) or **$20** (cloud)
- OpenAI API: **$50-200** (depending on volume)
- DALL-E: **$20-100** (image generation)
- PostgreSQL: **$0-25** (self-hosted or managed)
- Server/Hosting: **$10-50** (VPS)

**Total: ~$80-375/month**

**Cost per Post:**
- Text only: ~$0.03-0.06 (GPT-4)
- With image: ~$0.07-0.14 (GPT-4 + DALL-E)

---

## 🐛 Troubleshooting

### Common Issues

**n8n not starting:**
```bash
# Check Docker logs
docker-compose logs n8n

# Verify port 5678 is available
netstat -an | grep 5678
```

**Database connection errors:**
```bash
# Test connection
psql -h localhost -U postgres -d social_media

# Check DATABASE_URL in .env
```

**API not responding:**
```bash
# Check if FastAPI is running
curl http://localhost:8000/health

# Check logs
tail -f logs/app.log
```

**Agent execution failures:**
- Check OpenAI API key
- Verify database has required data
- Check agent logs in `logs/agents.log`

---

## 📚 Documentation

- [Development Approaches](./DEVELOPMENT_APPROACHES.md) - Detailed comparison
- [n8n Implementation Guide](../n8n_implementation_guide.md) - n8n setup
- [API Reference](./docs/API_REFERENCE.md) - Full API docs
- [Agent Details](./docs/AGENTS.md) - Agent specifications

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

This project is provided as-is for educational and commercial use.

---

## 🆘 Support

- **Issues**: Open a GitHub issue
- **Questions**: Check documentation or open a discussion
- **Commercial Support**: Contact for enterprise support

---

## 🎉 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Workflow automation by [n8n](https://n8n.io/)
- AI powered by [OpenAI](https://openai.com/)

---

**Ready to automate your social media? Start with the Quick Start guide above! 🚀**

