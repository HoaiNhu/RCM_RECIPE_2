#!/usr/bin/env python3
"""
Test script để kiểm tra T5 Model integration

Workflow test:
1. Vietnamese ingredients → English translation
2. English ingredients → T5 recipe generation
3. English recipe → Vietnamese translation + enhancement
"""

import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

from domain.services.recipe_generation_service import RecipeGenerationService

def test_t5_integration():
    """Test T5 model với Vietnamese input"""
    
    print("=" * 80)
    print("🧪 TESTING T5 MODEL INTEGRATION")
    print("=" * 80)
    
    # Test 1: Vietnamese ingredients
    print("\n📝 Test 1: Vietnamese Ingredients → T5 → Vietnamese Recipe")
    print("-" * 80)
    
    vi_ingredients = "bột mì, đường, trứng, bơ, bột matcha, sữa tươi"
    print(f"Input (Vietnamese): {vi_ingredients}")
    
    try:
        # Initialize service with T5 enabled
        service = RecipeGenerationService(use_t5=True)
        
        # Generate recipe
        print("\n🚀 Starting recipe generation pipeline...")
        recipe = service.generate_from_ingredients(vi_ingredients, language="vi")
        
        print("\n✅ SUCCESS! Recipe generated with T5 model")
        print("=" * 80)
        print(f"📋 RECIPE DETAILS:")
        print("=" * 80)
        print(f"Title: {recipe.title}")
        print(f"Description: {recipe.description}")
        print(f"\nIngredients ({len(recipe.ingredients)}):")
        for i, ing in enumerate(recipe.ingredients, 1):
            print(f"  {i}. {ing.quantity} {ing.unit or ''} {ing.name}")
        
        print(f"\nInstructions ({len(recipe.instructions)} steps):")
        for i, step in enumerate(recipe.instructions, 1):
            print(f"  {i}. {step[:100]}...")
        
        print(f"\nTiming:")
        print(f"  Prep time: {recipe.prep_time}")
        print(f"  Cook time: {recipe.cook_time}")
        print(f"  Servings: {recipe.servings}")
        print(f"  Difficulty: {recipe.difficulty}")
        
        print(f"\nTags: {', '.join(recipe.tags)}")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: English ingredients
    print("\n" + "=" * 80)
    print("\n📝 Test 2: English Ingredients → T5 → English Recipe")
    print("-" * 80)
    
    en_ingredients = "flour, sugar, eggs, butter, matcha powder, milk"
    print(f"Input (English): {en_ingredients}")
    
    try:
        # Generate recipe in English
        print("\n🚀 Starting recipe generation pipeline...")
        recipe = service.generate_from_ingredients(en_ingredients, language="en")
        
        print("\n✅ SUCCESS! Recipe generated with T5 model")
        print("=" * 80)
        print(f"📋 RECIPE DETAILS:")
        print("=" * 80)
        print(f"Title: {recipe.title}")
        print(f"Description: {recipe.description[:150]}...")
        print(f"Ingredients: {len(recipe.ingredients)} items")
        print(f"Instructions: {len(recipe.instructions)} steps")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Fallback to Gemini
    print("\n" + "=" * 80)
    print("\n📝 Test 3: Fallback to Gemini-only mode")
    print("-" * 80)
    
    try:
        # Initialize service with T5 disabled
        service_gemini = RecipeGenerationService(use_t5=False)
        
        print("\n🚀 Generating with Gemini-only mode...")
        recipe = service_gemini.generate_from_ingredients(vi_ingredients, language="vi")
        
        print("\n✅ SUCCESS! Recipe generated with Gemini")
        print(f"Title: {recipe.title}")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 80)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    success = test_t5_integration()
    sys.exit(0 if success else 1)
