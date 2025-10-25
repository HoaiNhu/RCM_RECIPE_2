# configs/settings.py
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


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
    DEFAULT_GEMINI_MODEL: str = "gemini-2.5-pro"  # Changed from gemini-2.5-pro - free tier has 15 RPM
    # DEFAULT_GEMINI_MODEL: str = "gemini-2.5-flash"  # Changed from gemini-2.5-pro - free tier has 15 RPM
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_OUTPUT_TOKENS: int = 4096

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

settings = Settings()