import sys
import os
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[0]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

print("🧪 Testing RCM_RECIPE_2 System")
print("=" * 50)

# Test 1: Check environment
print("1. Checking environment...")
print(f"   GEMINI_API_KEY: {'✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Not set'}")
print(f"   Project root: {ROOT_DIR}")

# Test 2: Test Gemini Client
print("\n2. Testing Gemini Client...")
try:
    from infrastructure.ai.gemini_client import GeminiClient
    client = GeminiClient()
    print("   ✅ GeminiClient imported successfully")
    
    # Test a simple generation
    result = client.generate_creative_recipe(
        trend="labubu",
        user_segment="genz", 
        occasion="valentine",
        language="vi"
    )
    print(f"   ✅ Generated output: {len(result)} characters")
    print(f"   Preview: {result[:200]}...")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n🎉 Test completed!")