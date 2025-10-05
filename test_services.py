# test_services.py
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

def test_translator():
    print("Testing TranslatorService...")
    try:
        from infrastructure.ai.translator_service import TranslatorService
        translator = TranslatorService()
        
        # Test translation
        vi_text = "bột mì, đường, trứng, bơ, bột matcha"
        en_text = translator.vi_to_en(vi_text)
        print(f"VI: {vi_text}")
        print(f"EN: {en_text}")
        
        # Test reverse translation
        back_to_vi = translator.en_to_vi(en_text)
        print(f"Back to VI: {back_to_vi}")
        
    except Exception as e:
        print(f"Translator error: {e}")

def test_t5():
    print("\nTesting T5Client...")
    try:
        from infrastructure.external.t5_client import T5Client
        t5 = T5Client()
        
        # Test T5 generation
        ingredients = "flour, sugar, eggs, butter, matcha powder"
        recipe = t5.generate_recipe(ingredients)
        print(f"T5 output: {recipe[:200]}...")
        
    except Exception as e:
        print(f"T5 error: {e}")

def test_gemini():
    print("\nTesting GeminiClient...")
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
        print(f"Gemini output: {response[:200]}...")
        
    except Exception as e:
        print(f"Gemini error: {e}")

def test_parser():
    print("\nTesting RecipeParser...")
    try:
        from infrastructure.ai.recipe_parser import RecipeParser
        parser = RecipeParser()
        
        # Test with sample output
        sample_output = '''```json
{
  "title": "Banh Labubu Valentine Matcha",
  "description": "Banh bong lan mem min voi huong vi matcha thom ngon",
  "ingredients": [
    {"name": "bot mi", "quantity": "200", "unit": "g"},
    {"name": "duong", "quantity": "100", "unit": "g"}
  ],
  "instructions": [
    "Buoc 1: Tron bot mi voi duong",
    "Buoc 2: Them trung vao"
  ]
}
```'''
        
        result = parser.parse_gemini_output(sample_output)
        print(f"Parsed title: {result.get('title')}")
        print(f"Parsed ingredients: {len(result.get('ingredients', []))} items")
        
    except Exception as e:
        print(f"Parser error: {e}")

if __name__ == "__main__":
    test_translator()
    test_t5()
    test_gemini()
    test_parser()
