-- Multi-Agent Social Media Automation Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Business Information Table
CREATE TABLE IF NOT EXISTS business_info (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    target_audience TEXT,
    brand_guidelines TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Research Data Table
CREATE TABLE IF NOT EXISTS research_data (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES business_info(id) ON DELETE CASCADE,
    market_trends TEXT,
    competitor_analysis TEXT,
    insights TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Content Strategy Table
CREATE TABLE IF NOT EXISTS content_strategy (
    id SERIAL PRIMARY KEY,
    research_id INTEGER REFERENCES research_data(id) ON DELETE CASCADE,
    goals TEXT,
    themes JSONB,
    posting_schedule JSONB,
    target_metrics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Generated Content Table
CREATE TABLE IF NOT EXISTS generated_content (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES content_strategy(id) ON DELETE SET NULL,
    platform VARCHAR(50) NOT NULL,
    theme VARCHAR(100),
    text_content TEXT NOT NULL,
    image_url VARCHAR(500),
    variations JSONB,
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'approved', 'rejected', 'published'
    moderation_notes TEXT,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Published Posts Table
CREATE TABLE IF NOT EXISTS published_posts (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES generated_content(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    post_id VARCHAR(255), -- Platform-specific post ID
    published_at TIMESTAMP NOT NULL,
    scheduled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics Table
CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES published_posts(id) ON DELETE CASCADE,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(post_id, collected_at)
);

-- Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    analysis_data JSONB,
    recommendations TEXT,
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high'
    applied BOOLEAN DEFAULT FALSE,
    applied_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent Execution Logs Table
CREATE TABLE IF NOT EXISTS agent_executions (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    status VARCHAR(20) DEFAULT 'success', -- 'success', 'error', 'pending'
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_research_data_business_id ON research_data(business_id);
CREATE INDEX IF NOT EXISTS idx_content_strategy_research_id ON content_strategy(research_id);
CREATE INDEX IF NOT EXISTS idx_generated_content_strategy_id ON generated_content(strategy_id);
CREATE INDEX IF NOT EXISTS idx_generated_content_status ON generated_content(status);
CREATE INDEX IF NOT EXISTS idx_published_posts_content_id ON published_posts(content_id);
CREATE INDEX IF NOT EXISTS idx_published_posts_platform ON published_posts(platform);
CREATE INDEX IF NOT EXISTS idx_analytics_post_id ON analytics(post_id);
CREATE INDEX IF NOT EXISTS idx_analytics_collected_at ON analytics(collected_at);
CREATE INDEX IF NOT EXISTS idx_agent_executions_agent_name ON agent_executions(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_executions_created_at ON agent_executions(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_business_info_updated_at BEFORE UPDATE ON business_info
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_strategy_updated_at BEFORE UPDATE ON content_strategy
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_generated_content_updated_at BEFORE UPDATE ON generated_content
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample business info (for testing)
INSERT INTO business_info (company_name, industry, target_audience, brand_guidelines)
VALUES (
    'Tech Startup Inc',
    'Technology',
    'Tech enthusiasts, developers, entrepreneurs',
    'Professional, innovative, friendly tone. No profanity. Focus on value and solutions.'
) ON CONFLICT DO NOTHING;

