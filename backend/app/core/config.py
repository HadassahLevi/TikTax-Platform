"""
Tik-Tax API Configuration
Manages all environment variables and application settings using Pydantic
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # App Information
    PROJECT_NAME: str = "Tik-Tax API"
    PROJECT_NAME_HE: str = "טיק-טקס API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = "API לניהול קבלות חכם עבור עסקים קטנים בישראל"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Database
    DATABASE_URL: str
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_S3_REGION: str = "eu-west-1"
    
    # Google Cloud Vision
    GOOGLE_CLOUD_VISION_CREDENTIALS: str
    
    # SMS (Twilio)
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    
    # Email (SendGrid)
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_FROM_NAME: str = "Tik-Tax"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Redis (for caching and rate limiting)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Sentry (error tracking)
    SENTRY_DSN: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf"]
    
    # OCR Settings
    OCR_CONFIDENCE_THRESHOLD: float = 0.8
    
    # Israeli Business Settings
    VAT_RATE: float = 0.17  # 17% VAT in Israel
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Global settings instance
settings = Settings()
