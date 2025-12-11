# 🚀 Quick Start Guide

Get your multi-agent social media automation system running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- Python 3.9+ installed
- OpenAI API key
- Platform credentials (Telegram, VK, etc.)

## Step 1: Clone & Setup (2 minutes)

```bash
cd multi_agent_social_media_automation

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env

# Edit .env with your API keys
# At minimum, set:
# - OPENAI_API_KEY
# - DATABASE_URL (or use default)
```

## Step 2: Start Infrastructure (1 minute)

```bash
# Start PostgreSQL and n8n
docker-compose up -d

# Wait 30 seconds for services to start
```

## Step 3: Initialize Database (1 minute)

```bash
# Option 1: Using psql
psql -h localhost -U postgres -d social_media < database/schema.sql

# Option 2: Using Python script
python scripts/init_database.py
```

## Step 4: Start API (30 seconds)

```bash
# In a new terminal
uvicorn api.main:app --reload --port 8000
```

## Step 5: Configure n8n (1 minute)

1. Open http://localhost:5678
2. Login with: `admin` / `admin` (change in docker-compose.yml)
3. Go to Settings → Credentials
4. Add:
   - OpenAI API key
   - Database credentials
   - Platform credentials
5. Import workflow: `n8n_workflows/01_main_content_pipeline.json`

## Step 6: Test (30 seconds)

```bash
# Test API
python scripts/test_api.py

# Test agents
python scripts/test_agents.py --agent researcher
```

## ✅ You're Ready!

Your system is now running:
- **n8n UI**: http://localhost:5678
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Next Steps

1. **Configure Business Info**: Add your business details to the database
2. **Customize Workflows**: Modify n8n workflows for your needs
3. **Set Up Scheduling**: Configure schedule triggers in n8n
4. **Monitor**: Check logs and analytics

## Troubleshooting

**n8n not accessible?**
```bash
docker-compose logs n8n
```

**API not responding?**
```bash
# Check if running
curl http://localhost:8000/health

# Check logs
tail -f logs/app.log
```

**Database connection error?**
```bash
# Test connection
psql -h localhost -U postgres -d social_media

# Check DATABASE_URL in .env
```

## Need Help?

- Check the main [README.md](./README.md) for detailed documentation
- Review [DEVELOPMENT_APPROACHES.md](./DEVELOPMENT_APPROACHES.md) for architecture details
- Open an issue for support

---

**Happy Automating! 🎉**

