# list_models.py
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

def list_models():
    try:
        import google.generativeai as genai
        from configs.settings import settings
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # List available models
        models = genai.list_models()
        print("Available models:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
