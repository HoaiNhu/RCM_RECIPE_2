# configs/settings.py
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv()


class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str
    
    # Paths
    MODEL_CACHE_DIR: str = ".cache/models"
    DATA_DIR: Path = ROOT_DIR / "data"
    OUTPUT_DIR: Path = ROOT_DIR / "output"
    LOG_DIR: Path = ROOT_DIR / "logs"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/recipes.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "RCM_RECIPE"
    VERSION: str = "2.0.0"
    
    # Model Settings
    DEFAULT_GEMINI_MODEL: str = "gemini-1.5-pro"
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_OUTPUT_TOKENS: int = 2048

settings = Settings()