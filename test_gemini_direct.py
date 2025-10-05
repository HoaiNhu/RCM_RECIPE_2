import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[0]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

async def test_gemini_direct():
    print("Testing Gemini directly with improved prompts...")
    try:
        from infrastructure.ai.gemini_client import GeminiClient
        
        client = GeminiClient()
        
        print("\n" + "=" * 50)
        print("🧪 TEST 1: generate-from-trend")
        print("=" * 50)
        
        result1 = client.generate_creative_recipe(
            trend="labubu valentine matcha",
            user_segment="genz",
            occasion="valentine",
            language="vi"
        )
        
        print("Result:")
        print(result1[:500] + "..." if len(result1) > 500 else result1)
        
        print("\n" + "=" * 50)
        print("🧪 TEST 2: generate-from-ingredients")
        print("=" * 50)
        
        result2 = client.generate_recipe_from_ingredients(
            ingredients="bột mì, đường, trứng, bơ, bột matcha",
            language="vi"
        )
        
        print("Result:")
        print(result2[:500] + "..." if len(result2) > 500 else result2)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_direct())

