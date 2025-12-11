"""Application settings and configuration."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7

    # Database Configuration
    database_url: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "social_media"
    db_user: str = "postgres"
    db_password: str = "postgres"

    # Platform Credentials
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    vk_access_token: Optional[str] = None
    vk_group_id: Optional[str] = None

    # n8n Configuration
    n8n_basic_auth_user: str = "admin"
    n8n_basic_auth_password: str = "admin"
    n8n_encryption_key: str = "change-this-encryption-key"
    n8n_webhook_url: str = "http://localhost:5678/"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = False


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

