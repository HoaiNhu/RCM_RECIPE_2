# Quick test simple JSON response
import os
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

os.environ["GEMINI_API_KEY"] = "AIzaSyAkGgbqhI-1frAudws0C7r-T50g1QFusXM"

from infrastructure.ai.gemini_client import GeminiClient

client = GeminiClient()

# Test simple JSON response
print("🧪 Testing Simple Prompt...")
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

simple_prompt = """Tạo JSON công thức bánh matcha đơn giản:

{"title": "Bánh Matcha", "description": "Bánh ngon", "ingredients": [{"name": "bột mì", "quantity": "2", "unit": "cup"}], "instructions": ["Mix"], "prep_time": "30 phút", "cook_time": "25 phút", "servings": "8 phần", "difficulty": "medium", "tags": ["matcha"]}

Chỉ trả về JSON tương tự:"""

response = model.generate_content(simple_prompt, generation_config={"temperature": 0.3})
print(f"Raw Response:\n{response.text}\n")

# Test JSON parsing
import json
import re

def clean_json(text):
    # Remove markdown
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Find JSON object
    start = text.find('{')
    end = text.rfind('}') + 1
    
    if start != -1 and end != -1:
        json_text = text[start:end]
        try:
            return json.loads(json_text)
        except:
            return None
    return None

parsed = clean_json(response.text)
print(f"Parsed JSON: {parsed}")