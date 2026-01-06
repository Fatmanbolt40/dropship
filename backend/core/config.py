import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore', env_file='.env', case_sensitive=True)
    
    # Application
    APP_NAME: str = "DropShip AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./dropship.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # E-commerce
    SHOPIFY_API_KEY: str = ""
    SHOPIFY_API_SECRET: str = ""
    SHOPIFY_STORE_URL: str = ""
    
    # AliExpress
    ALIEXPRESS_API_KEY: str = ""
    ALIEXPRESS_API_SECRET: str = ""
    
    # Stripe
    STRIPE_API_KEY: str = ""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

settings = Settings()

settings = Settings()
