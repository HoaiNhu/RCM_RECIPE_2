# test_simple.py
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

def test_gemini_only():
    print("Testing GeminiClient only...")
    try:
        from infrastructure.ai.gemini_client import GeminiClient
        gemini = GeminiClient()
        
        # Test Gemini generation
        response = gemini.generate_creative_recipe(
            trend="labubu valentine matcha",
            user_segment="genz",
            occasion="valentine",
            language="vi"
        )
        print(f"Gemini output length: {len(response)}")
        print(f"First 300 chars: {response[:300]}")
        
    except Exception as e:
        print(f"Gemini error: {e}")

if __name__ == "__main__":
    test_gemini_only()
