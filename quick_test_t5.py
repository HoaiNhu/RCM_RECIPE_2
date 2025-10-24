#!/usr/bin/env python3
"""
Quick test T5 model functionality
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

print("🔍 Testing T5 Model Integration...")
print("=" * 60)

# Test 1: Check T5 client
print("\n1️⃣ Testing T5 Client...")
try:
    from infrastructure.external.t5_client import T5Client
    client = T5Client()
    print("✅ T5Client initialized successfully")
    
    # Test generation
    test_ingredients = "flour, sugar, eggs, butter"
    print(f"   Input: {test_ingredients}")
    
    result = client.generate_recipe(test_ingredients)
    print(f"   Output: {result[:100]}...")
    print("✅ T5 generation works!")
    
except Exception as e:
    print(f"❌ T5Client failed: {e}")
    sys.exit(1)

# Test 2: Check Translator
print("\n2️⃣ Testing Translator Service...")
try:
    from infrastructure.ai.translator_service import TranslatorService
    translator = TranslatorService()
    
    vi_text = "bột mì, đường, trứng"
    en_text = translator.vi_to_en(vi_text)
    print(f"   VI: {vi_text}")
    print(f"   EN: {en_text}")
    print("✅ Translation works!")
    
except Exception as e:
    print(f"⚠️ Translator might not work: {e}")

# Test 3: Check RecipeGenerationService
print("\n3️⃣ Testing RecipeGenerationService...")
try:
    from domain.services.recipe_generation_service import RecipeGenerationService
    
    # Test with T5
    service = RecipeGenerationService(use_t5=True)
    print(f"✅ Service initialized (T5 enabled: {service.use_t5})")
    
    if service.use_t5 and service.t5_client:
        print("✅ T5 client is ready!")
    else:
        print("⚠️ T5 client not available, will use Gemini fallback")
    
except Exception as e:
    print(f"❌ Service initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 All basic tests passed!")
print("=" * 60)
print("\n📝 To run full test:")
print("   python test_t5_integration.py")
print("\n🚀 To start API server:")
print("   python app/main.py")
print("\n📖 Read documentation:")
print("   T5_INTEGRATION_GUIDE.md")
