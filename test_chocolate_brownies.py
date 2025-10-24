#!/usr/bin/env python3
"""
Test T5 với chocolate brownies input
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

print("🧪 Testing T5 with Chocolate Brownies Input")
print("=" * 80)

from domain.services.recipe_generation_service import RecipeGenerationService

# Test input
ingredients = "flour, cocoa powder, sugar, eggs, butter"
print(f"📝 Input: {ingredients}")
print(f"🎯 Expected: Chocolate Brownies recipe")
print()

# Initialize service
service = RecipeGenerationService(use_t5=True)

# Generate recipe
print("🚀 Generating recipe...")
recipe = service.generate_from_ingredients(ingredients, language="vi")

print("\n" + "=" * 80)
print("✅ RESULT:")
print("=" * 80)
print(f"Title: {recipe.title}")
print(f"Description: {recipe.description[:100]}...")
print(f"\nIngredients ({len(recipe.ingredients)}):")
for i, ing in enumerate(recipe.ingredients[:5], 1):
    print(f"  {i}. {ing.quantity} {ing.unit or ''} {ing.name}")

print(f"\nInstructions ({len(recipe.instructions)} steps):")
for i, step in enumerate(recipe.instructions[:3], 1):
    print(f"  {i}. {step[:80]}...")

print(f"\nTags: {', '.join(recipe.tags)}")

# Check if output matches input
print("\n" + "=" * 80)
print("🔍 VALIDATION:")
print("=" * 80)

has_cocoa = any('cocoa' in ing.name.lower() or 'ca cao' in ing.name.lower() 
                for ing in recipe.ingredients)
has_chocolate = 'chocolate' in recipe.title.lower() or 'brownies' in recipe.title.lower() or 'socola' in recipe.title.lower()

if has_cocoa or has_chocolate:
    print("✅ PASS: Output matches input (chocolate/brownies detected)")
else:
    print("❌ FAIL: Output does not match input")
    print(f"   Expected: chocolate brownies with cocoa powder")
    print(f"   Got: {recipe.title}")
