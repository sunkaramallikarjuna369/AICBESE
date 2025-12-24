from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Cost Optimization Notes:
    - Use AI_PROVIDER=mock for development/testing (free)
    - Use AI_PROVIDER=replicate for low-cost production (~$0.05/million tokens)
    - Use AI_PROVIDER=vertex only if you have GCP credits or higher budget
    """
    APP_NAME: str = "CBSE Learning Platform (Low-Cost Edition)"
    APP_VERSION: str = "1.1.0"
    DEBUG: bool = True
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # AI Provider Configuration
    # Options: mock (free), replicate (low-cost), vertex (higher cost)
    AI_PROVIDER: str = "mock"
    
    # Replicate Configuration (recommended for low-budget deployments)
    # Get your API token from https://replicate.com/account/api-tokens
    REPLICATE_API_TOKEN: Optional[str] = None
    REPLICATE_MODEL: str = "meta/meta-llama-3.1-8b-instruct"
    
    # Vertex AI Configuration (higher cost, requires GCP project)
    VERTEX_AI_PROJECT: Optional[str] = None
    VERTEX_AI_LOCATION: str = "us-central1"
    
    # Firebase Configuration (free tier: 50K reads/day, 20K writes/day)
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    
    # Optional: Redis for caching (skip for low-budget, use in-memory instead)
    REDIS_URL: Optional[str] = None
    
    # Optional: Pub/Sub for async processing (skip for low-budget)
    PUBSUB_PROJECT: Optional[str] = None
    
    # GCP Configuration
    GCP_PROJECT_ID: Optional[str] = None
    GCP_REGION: str = "asia-south1"  # Mumbai region for Indian users
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
