"""Settings - Application settings using Pydantic."""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "Joe-Agent-Platform"
    debug: bool = False
    log_level: str = "INFO"
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    database_url: str = "postgresql://joe:joe@localhost:5432/joe_db"
    redis_url: str = "redis://localhost:6379"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    
    openrouter_api_key: str = ""
    llm_model: str = "openrouter-free"  # FREE coding model
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096
    
    secret_key: str = "change-this-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 10
    
    max_crawl_depth: int = 3
    crawl_timeout: int = 30
    browser_headless: bool = True
    
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_dimension: int = 384
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False