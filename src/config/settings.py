"""Configuration settings for the AI Code Review Agent."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # OpenAI Configuration
    openai_api_key: str
    default_model: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_tokens: int = 4096
    
    # LangSmith Configuration
    langchain_tracing_v2: bool = True
    langchain_api_key: str | None = None
    langchain_project: str = "ai-code-review-agent"
    langchain_endpoint: str = "https://api.smith.langchain.com"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Vector Store Configuration
    vector_store_type: Literal["faiss", "chromadb"] = "faiss"
    embedding_model: str = "text-embedding-3-small"
    
    # MLflow Configuration
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "code-review-agent"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # Review Configuration
    max_code_length: int = 10000
    review_timeout_seconds: int = 120
    enable_parallel_agents: bool = True
    
    # GitHub Integration (optional)
    github_token: str | None = None
    github_webhook_secret: str | None = None


# Singleton instance
settings = Settings()
