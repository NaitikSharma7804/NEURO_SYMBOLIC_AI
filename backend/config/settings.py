from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Neuro-Symbolic AI Framework"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # LLM Settings
    LLM_PROVIDER: str = "mock"  # "mock" | "openai"
    LLM_MODEL: str = "mock-model"
    OPENAI_API_KEY: Optional[str] = None
    MAX_FORMALIZATION_RETRIES: int = 2
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./neurosymbolic.db"
    
    # Symbolic Reasoning Settings
    PROLOG_PATH: Optional[str] = None
    REASONING_BACKEND: str = "pure"  # "pure" | "swi_prolog"
    DEFAULT_TIMEOUT_SECONDS: float = 10.0
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
