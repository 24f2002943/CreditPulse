from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CreditPulse"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "creditpulse_super_secret_jwt_key_2026_dev")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./creditpulse.db")
    
    # Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE_MB: int = 25
    
    # ML & Risk Engine Parameters
    WEIGHT_FINANCIAL_SCORE: float = 0.60
    WEIGHT_RELATIONSHIP_SCORE: float = 0.25
    WEIGHT_MACRO_ADJUSTMENT: float = 0.15
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
