#!/usr/bin/env python3
"""Debug script để test Gemini responses"""

import sys
import os
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

# Load environment
from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ai.recipe_parser import RecipeParser
import json

def test_ingredients_endpoint():
    """Test case tương tự request của bạn"""
    print("="*50)
    print("TESTING INGREDIENTS ENDPOINT")
    print("="*50)
    
    client = GeminiClient()
    parser = RecipeParser()
    
    # Test data giống như request
    ingredients = "bột mì, đường, trứng, bơ, bột matcha"
    language = "vi"
    
    print(f"Input ingredients: {ingredients}")
    print(f"Language: {language}")
    print("\n" + "-"*30)
    print("RAW GEMINI RESPONSE:")
    print("-"*30)
    
    try:
        # Get raw response
        raw_response = client.generate_recipe_from_ingredients(ingredients, language)
        print(f"Response length: {len(raw_response)}")
        print(f"Response type: {type(raw_response)}")
        print(f"First 200 chars: {repr(raw_response[:200])}")
        print(f"Full response:\n{raw_response}")
        
        print("\n" + "-"*30)
        print("PARSED RESULT:")
        print("-"*30)
        
        # Parse response
        parsed = parser.parse_gemini_output(raw_response)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_trend_endpoint():
    """Test case tương tự request thứ 2"""
    print("\n" + "="*50)
    print("TESTING TREND ENDPOINT")
    print("="*50)
    
    client = GeminiClient()
    parser = RecipeParser()
    
    # Test data giống như request
    trend = "labubu valentine matcha"
    user_segment = "genz"
    occasion = "valentine"
    language = "vi"
    
    print(f"Input trend: {trend}")
    print(f"User segment: {user_segment}")
    print(f"Occasion: {occasion}")
    print(f"Language: {language}")
    print("\n" + "-"*30)
    print("RAW GEMINI RESPONSE:")
    print("-"*30)
    
    try:
        # Get raw response
        raw_response = client.generate_creative_recipe(
            trend=trend,
            user_segment=user_segment,
            occasion=occasion,
            language=language
        )
        print(f"Response length: {len(raw_response)}")
        print(f"Response type: {type(raw_response)}")
        print(f"First 200 chars: {repr(raw_response[:200])}")
        print(f"Full response:\n{raw_response}")
        
        print("\n" + "-"*30)
        print("PARSED RESULT:")
        print("-"*30)
        
        # Parse response
        parsed = parser.parse_gemini_output(raw_response)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"Gemini API Key set: {bool(os.getenv('GEMINI_API_KEY'))}")
    test_ingredients_endpoint()
    test_trend_endpoint()