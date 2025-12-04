# src/config/settings.py
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # OpenAI API settings
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_org_id: Optional[str] = Field(None, alias="OPENAI_ORG_ID")
    
    # Agent settings
    default_model: str = Field("gpt-4o", alias="DEFAULT_MODEL")
    default_temperature: float = Field(0.7, alias="DEFAULT_TEMPERATURE")
    
    # Tracing settings
    enable_tracing: bool = Field(True, alias="ENABLE_TRACING")
    trace_workflow_name: str = Field("my-agent-app", alias="TRACE_WORKFLOW_NAME")
    
    # Application settings
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    environment: str = Field("development", alias="ENVIRONMENT")

# Create a global settings instance
settings = Settings()
