from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    google_api_key: str
    knowledge_path: str = "../knowledge"
    chroma_db_path: str = "./chroma_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

