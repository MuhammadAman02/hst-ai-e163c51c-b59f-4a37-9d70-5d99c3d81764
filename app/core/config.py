"""Application configuration using pydantic-settings V2."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = Field(default="Apple Store")
    app_description: str = Field(default="Premium Apple Products Store")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    api_prefix: str = Field(default="/api")
    
    # Security
    secret_key: str = Field(default="apple-store-secret-key-change-in-production")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    
    # Database
    database_url: str = Field(default="sqlite:///./data/apple_store.db")
    
    # File uploads
    max_file_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    upload_directory: str = Field(default="./app/static/uploads")

settings = Settings()

__all__ = ["settings", "Settings"]