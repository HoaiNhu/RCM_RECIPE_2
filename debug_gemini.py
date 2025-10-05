import os
os.environ["GEMINI_API_KEY"] = "AIzaSyAkGgbqhI-1frAudws0C7r-T50g1QFusXM"

from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ai.recipe_parser import RecipeParser

# Test Gemini response
client = GeminiClient()
parser = RecipeParser()

print("🔥 Testing Gemini Creative Recipe...")
raw_response = client.generate_creative_recipe(
    trend="labubu valentine",
    user_segment="genz",
    language="vi"
)

print(f"\n📝 Raw Response Length: {len(raw_response)}")
print(f"📝 Raw Response:\n{raw_response}\n")

# Test parser
print("🔍 Testing Parser...")
parsed_data = parser.parse_gemini_output(raw_response)
print(f"📊 Parsed Data: {parsed_data}")