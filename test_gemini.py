# test_gemini.py
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

from infrastructure.ai.gemini_client import GeminiClient

def test_gemini():
    try:
        client = GeminiClient()
        print("Testing Gemini client...")
        
        # Test basic connection
        response = client.generate_creative_recipe(
            trend="labubu valentine matcha",
            user_segment="genz",
            occasion="hallowen",
            language="vi"
        )
        
        print("Gemini response:")
        print(response[:500] + "...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini()
