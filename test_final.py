#!/usr/bin/env python3
"""
Test script để kiểm tra hệ thống RCM_RECIPE_2
"""
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

def test_gemini_client():
    """Test Gemini client directly"""
    print("🧪 Testing Gemini Client...")
    try:
        from infrastructure.ai.gemini_client import GeminiClient
        
        client = GeminiClient()
        
        # Test 1: generate-from-trend
        print("\n" + "=" * 50)
        print("TEST 1: generate-from-trend")
        print("=" * 50)
        
        result1 = client.generate_creative_recipe(
            trend="labubu valentine matcha",
            user_segment="genz",
            occasion="valentine",
            language="vi"
        )
        
        print("✅ Success!")
        print(f"Output length: {len(result1)} characters")
        print("First 300 characters:")
        print(result1[:300] + "..." if len(result1) > 300 else result1)
        
        # Test 2: generate-from-ingredients
        print("\n" + "=" * 50)
        print("TEST 2: generate-from-ingredients")
        print("=" * 50)
        
        result2 = client.generate_recipe_from_ingredients(
            ingredients="bột mì, đường, trứng, bơ, bột matcha",
            language="vi"
        )
        
        print("✅ Success!")
        print(f"Output length: {len(result2)} characters")
        print("First 300 characters:")
        print(result2[:300] + "..." if len(result2) > 300 else result2)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_recipe_parser():
    """Test Recipe Parser"""
    print("\n🧪 Testing Recipe Parser...")
    try:
        from infrastructure.ai.recipe_parser import RecipeParser
        
        parser = RecipeParser()
        
        # Test JSON parsing
        test_json = '''
        {
          "title": "Bánh Matcha Đặc Biệt",
          "description": "Món bánh ngọt thơm ngon với hương vị matcha đậm đà",
          "ingredients": [
            {"name": "bột mì", "quantity": "200", "unit": "g"},
            {"name": "đường", "quantity": "100", "unit": "g"}
          ],
          "instructions": [
            "Bước 1: Làm nóng lò ở 175°C",
            "Bước 2: Trộn bột mì với đường"
          ],
          "prep_time": "20 phút",
          "cook_time": "30 phút",
          "servings": "8 phần",
          "difficulty": "easy"
        }
        '''
        
        result = parser.parse_gemini_output(test_json)
        print("✅ JSON parsing success!")
        print(f"Title: {result.get('title')}")
        print(f"Ingredients count: {len(result.get('ingredients', []))}")
        print(f"Instructions count: {len(result.get('instructions', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_recipe_generation_service():
    """Test Recipe Generation Service"""
    print("\n🧪 Testing Recipe Generation Service...")
    try:
        from domain.services.recipe_generation_service import RecipeGenerationService
        
        service = RecipeGenerationService()
        
        # Test generate_from_trend
        print("\n--- Testing generate_from_trend ---")
        recipe1 = service.generate_from_trend(
            trend="labubu valentine matcha",
            user_segment="genz",
            occasion="valentine",
            language="vi"
        )
        
        print("✅ Success!")
        print(f"Title: {recipe1.title}")
        print(f"Description: {recipe1.description[:100]}...")
        print(f"Ingredients: {len(recipe1.ingredients)} items")
        print(f"Instructions: {len(recipe1.instructions)} steps")
        
        # Test generate_from_ingredients
        print("\n--- Testing generate_from_ingredients ---")
        recipe2 = service.generate_from_ingredients(
            ingredients="bột mì, đường, trứng, bơ, bột matcha",
            language="vi"
        )
        
        print("✅ Success!")
        print(f"Title: {recipe2.title}")
        print(f"Description: {recipe2.description[:100]}...")
        print(f"Ingredients: {len(recipe2.ingredients)} items")
        print(f"Instructions: {len(recipe2.instructions)} steps")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 RCM_RECIPE_2 System Test")
    print("=" * 50)
    
    # Check environment
    print(f"Project root: {ROOT_DIR}")
    print(f"GEMINI_API_KEY: {'✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Not set'}")
    
    # Run tests
    tests = [
        ("Gemini Client", test_gemini_client),
        ("Recipe Parser", test_recipe_parser),
        ("Recipe Generation Service", test_recipe_generation_service),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running {test_name} Test")
        print(f"{'='*60}")
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()

