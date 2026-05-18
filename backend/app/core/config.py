import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Masion Feride Shop"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-for-jwt-masion-feride")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./masion_feride.db")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
