from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    GEMINI_API_KEY: str
    
    model_config = {
        "env_file": ".env", 
        "env_file_encoding": "utf-8"
    }

try:
    settings = TestSettings()
    print("✅ Success:", settings.GEMINI_API_KEY[:10] + "...")
except Exception as e:
    print("❌ Error:", e)