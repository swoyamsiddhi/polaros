"""Application configuration via environment variables."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Polar Ops Commander"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database - SQLite by default, PostgreSQL optional
    DATABASE_URL: str = "sqlite:///./polarops.db"

    # JWT Auth
    SECRET_KEY: str = "polar-ops-commander-sih26062-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours for demo

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Optional LLM API key for enhanced NL assistant
    LLM_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
