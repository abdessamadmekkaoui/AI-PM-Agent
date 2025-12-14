# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./ai_pm_agent.db"
    
    # Google Gemini API
    GEMINI_API_KEY: str
    
    # Google Calendar API (optionnel)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    # App (optionnel)
    PROJECT_NAME: str = "AI PM Agent"
    VERSION: str = "1.0.0"
    APP_ENV: Optional[str] = "development"
    APP_HOST: Optional[str] = "0.0.0.0"
    APP_PORT: Optional[str] = "8000"
    CORS_ORIGINS: Optional[str] = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permettre les champs supplémentaires

settings = Settings()