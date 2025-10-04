# test_improved_system.py
"""
Test script để kiểm tra hệ thống AI Recipe Generation đã được cải thiện
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.append(str(ROOT_DIR))

from domain.services.recipe_generation_service import RecipeGenerationService
from domain.services.trend_analyzer import TrendAnalyzer
from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ai.recipe_parser import RecipeParser
import json

def test_recipe_parser():
    """Test RecipeParser với các format khác nhau"""
    print("🧪 TESTING RECIPE PARSER")
    print("=" * 50)
    
    parser = RecipeParser()
    
    # Test JSON format
    json_output = """
    {
      "title": "Bánh Labubu Cute",
      "description": "Bánh bông lan mềm mịn với hương vị matcha thơm ngon",
      "ingredients": [
        {"name": "bột mì", "quantity": "200", "unit": "g"},
        {"name": "đường", "quantity": "100", "unit": "g"},
        {"name": "trứng", "quantity": "3", "unit": "quả"}
      ],
      "instructions": [
        "Bước 1: Trộn bột mì với đường",
        "Bước 2: Thêm trứng vào và khuấy đều"
      ],
      "prep_time": "20 phút",
      "cook_time": "30 phút",
      "servings": "8 phần",
      "difficulty": "easy"
    }
    """
    
    result = parser.parse_gemini_output(json_output)
    print("✅ JSON Parsing Result:")
    print(f"Title: {result['title']}")
    print(f"Ingredients: {len(result['ingredients'])} items")
    print(f"Instructions: {len(result['instructions'])} steps")
    print()

def test_gemini_client():
    """Test GeminiClient với prompt mới"""
    print("🤖 TESTING GEMINI CLIENT")
    print("=" * 50)
    
    try:
        client = GeminiClient()
        
        # Test basic connection
        print("Testing basic connection...")
        response = client.generate_recipe_from_ingredients(
            "bột mì, trứng, đường, bơ, sữa tươi",
            "vi"
        )
        print("✅ Gemini connection successful")
        print(f"Response length: {len(response)} characters")
        print(f"First 200 chars: {response[:200]}...")
        print()
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        print()

def test_recipe_generation():
    """Test RecipeGenerationService với các scenarios"""
    print("🎂 TESTING RECIPE GENERATION")
    print("=" * 50)
    
    try:
        service = RecipeGenerationService()
        
        # Test 1: Generate from ingredients
        print("Test 1: Generate from ingredients")
        recipe1 = service.generate_from_ingredients(
            "bột mì, trứng, đường, bơ, sữa tươi, vani",
            "vi"
        )
        print(f"✅ Recipe 1: {recipe1.title}")
        print(f"   Ingredients: {len(recipe1.ingredients)} items")
        print(f"   Instructions: {len(recipe1.instructions)} steps")
        print()
        
        # Test 2: Generate from trend
        print("Test 2: Generate from trend")
        recipe2 = service.generate_from_trend(
            trend="Labubu (nhân vật hot trend)",
            user_segment="GenZ (18-25 tuổi, thích màu pastel, cute)",
            occasion="Sinh nhật",
            language="vi"
        )
        print(f"✅ Recipe 2: {recipe2.title}")
        print(f"   Ingredients: {len(recipe2.ingredients)} items")
        print(f"   Instructions: {len(recipe2.instructions)} steps")
        print()
        
        # Test 3: Generate for different segment
        print("Test 3: Generate for healthy segment")
        recipe3 = service.generate_from_trend(
            trend="Minimalist, healthy",
            user_segment="Dân gym, người ăn kiêng",
            occasion="Hàng ngày",
            language="vi"
        )
        print(f"✅ Recipe 3: {recipe3.title}")
        print(f"   Ingredients: {len(recipe3.ingredients)} items")
        print(f"   Instructions: {len(recipe3.instructions)} steps")
        print()
        
    except Exception as e:
        print(f"❌ Recipe generation test failed: {e}")
        print()

def test_trend_analyzer():
    """Test TrendAnalyzer"""
    print("📈 TESTING TREND ANALYZER")
    print("=" * 50)
    
    try:
        analyzer = TrendAnalyzer()
        
        # Test trend analysis
        trends = analyzer.analyze_trends()
        print(f"✅ Found {len(trends)} trends")
        
        for i, trend in enumerate(trends[:3], 1):
            print(f"   Trend {i}: {trend.trend_name} (Score: {trend.trend_score})")
        print()
        
    except Exception as e:
        print(f"❌ Trend analyzer test failed: {e}")
        print()

def test_full_pipeline():
    """Test toàn bộ pipeline"""
    print("🚀 TESTING FULL PIPELINE")
    print("=" * 50)
    
    try:
        # Simulate full workflow
        service = RecipeGenerationService()
        
        # Step 1: Analyze trends
        print("Step 1: Analyzing trends...")
        analyzer = TrendAnalyzer()
        trends = analyzer.analyze_trends()
        print(f"   Found {len(trends)} trends")
        
        # Step 2: Generate recipe for top trend
        if trends:
            top_trend = trends[0]
            print(f"Step 2: Generating recipe for trend: {top_trend.trend_name}")
            
            recipe = service.generate_from_trend(
                trend=top_trend.trend_name,
                user_segment="GenZ (18-25 tuổi)",
                occasion="Hàng ngày",
                language="vi"
            )
            
            print(f"✅ Generated recipe: {recipe.title}")
            print(f"   Difficulty: {recipe.difficulty}")
            print(f"   Prep time: {recipe.prep_time}")
            print(f"   Cook time: {recipe.cook_time}")
            print(f"   Servings: {recipe.servings}")
            print()
            
            # Show ingredients
            print("   Ingredients:")
            for i, ingredient in enumerate(recipe.ingredients[:5], 1):
                print(f"     {i}. {ingredient.quantity} {ingredient.unit or ''} {ingredient.name}")
            print()
            
            # Show instructions
            print("   Instructions:")
            for i, instruction in enumerate(recipe.instructions[:3], 1):
                print(f"     {i}. {instruction}")
            print()
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        print()

def main():
    """Run all tests"""
    print("🎯 AI RECIPE GENERATION SYSTEM - IMPROVED TESTING")
    print("=" * 60)
    print()
    
    # Run individual tests
    test_recipe_parser()
    test_gemini_client()
    test_recipe_generation()
    test_trend_analyzer()
    test_full_pipeline()
    
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
