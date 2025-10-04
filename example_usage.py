# =============================================================================
# EXAMPLE USAGE CHO HỆ THỐNG AI RECIPE GENERATION
# =============================================================================

import asyncio
import json
from datetime import datetime
from application.use_cases.recipe_generation_use_case import RecipeGenerationUseCase
from domain.entities.recipe import UserSegment
from configs.settings import settings

async def example_basic_usage():
    """
    Example cơ bản: Tạo recipe từ trend keywords
    """
    print("🍰 EXAMPLE 1: BASIC USAGE")
    print("=" * 50)
    
    # Initialize use case
    use_case = RecipeGenerationUseCase(
        gemini_api_key=settings.GEMINI_API_KEY,
        news_api_key=settings.NEWS_API_KEY,
        youtube_api_key=settings.YOUTUBE_API_KEY
    )
    
    # Input data
    trend_keywords = ['labubu', 'valentine', 'matcha']
    user_segment = UserSegment.GEN_Z
    available_ingredients = [
        'flour', 'sugar', 'eggs', 'butter', 'matcha_powder',
        'strawberry', 'cream_cheese', 'vanilla', 'pink_food_coloring'
    ]
    
    # Run pipeline
    result = await use_case.generate_trend_recipe(
        trend_keywords=trend_keywords,
        user_segment=user_segment,
        available_ingredients=available_ingredients,
        target_language='Vietnamese'
    )
    
    # Display results
    print(f"📝 Recipe: {result['final_output']['recipe_title']}")
    print(f"🥘 Ingredients: {', '.join(result['final_output']['ingredients'])}")
    print(f"📊 Trend Analysis: {result['final_output']['trend_context']}")
    
    return result

async def example_korean_trend():
    """
    Example: Korean trend với K-pop
    """
    print("\n🍰 EXAMPLE 2: KOREAN TREND")
    print("=" * 50)
    
    use_case = RecipeGenerationUseCase(
        gemini_api_key=settings.GEMINI_API_KEY,
        news_api_key=settings.NEWS_API_KEY,
        youtube_api_key=settings.YOUTUBE_API_KEY
    )
    
    # Korean trend keywords
    trend_keywords = ['newjeans', 'korean_dessert', 'aesthetic', 'minimalist']
    user_segment = UserSegment.GEN_Z
    available_ingredients = [
        'flour', 'sugar', 'eggs', 'butter', 'matcha_powder',
        'strawberry', 'cream_cheese', 'vanilla', 'almond_flour',
        'coconut_sugar', 'dark_chocolate', 'sesame'
    ]
    
    result = await use_case.generate_trend_recipe(
        trend_keywords=trend_keywords,
        user_segment=user_segment,
        available_ingredients=available_ingredients,
        target_language='Korean'
    )
    
    print(f"📝 Recipe: {result['final_output']['recipe_title']}")
    print(f"🥘 Ingredients: {', '.join(result['final_output']['ingredients'])}")
    
    return result

async def example_health_conscious():
    """
    Example: Health conscious segment
    """
    print("\n🍰 EXAMPLE 3: HEALTH CONSCIOUS")
    print("=" * 50)
    
    use_case = RecipeGenerationUseCase(
        gemini_api_key=settings.GEMINI_API_KEY,
        news_api_key=settings.NEWS_API_KEY,
        youtube_api_key=settings.YOUTUBE_API_KEY
    )
    
    # Health trend keywords
    trend_keywords = ['keto', 'vegan', 'gluten_free', 'organic']
    user_segment = UserSegment.HEALTH_CONSCIOUS
    available_ingredients = [
        'almond_flour', 'coconut_sugar', 'stevia', 'coconut_oil',
        'almond_milk', 'chia_seeds', 'flax_seeds', 'cocoa_powder',
        'vanilla_extract', 'baking_powder', 'salt'
    ]
    
    result = await use_case.generate_trend_recipe(
        trend_keywords=trend_keywords,
        user_segment=user_segment,
        available_ingredients=available_ingredients,
        target_language='English'
    )
    
    print(f"📝 Recipe: {result['final_output']['recipe_title']}")
    print(f"🥘 Ingredients: {', '.join(result['final_output']['ingredients'])}")
    
    return result

async def example_seasonal_trend():
    """
    Example: Seasonal trend (Valentine)
    """
    print("\n🍰 EXAMPLE 4: SEASONAL TREND")
    print("=" * 50)
    
    use_case = RecipeGenerationUseCase(
        gemini_api_key=settings.GEMINI_API_KEY,
        news_api_key=settings.NEWS_API_KEY,
        youtube_api_key=settings.YOUTUBE_API_KEY
    )
    
    # Valentine trend keywords
    trend_keywords = ['valentine', 'romantic', 'pink', 'heart', 'chocolate']
    user_segment = UserSegment.MILLENNIALS
    available_ingredients = [
        'flour', 'sugar', 'eggs', 'butter', 'dark_chocolate',
        'strawberry', 'cream_cheese', 'vanilla', 'pink_food_coloring',
        'raspberry', 'white_chocolate', 'cocoa_powder'
    ]
    
    result = await use_case.generate_trend_recipe(
        trend_keywords=trend_keywords,
        user_segment=user_segment,
        available_ingredients=available_ingredients,
        target_language='Vietnamese'
    )
    
    print(f"📝 Recipe: {result['final_output']['recipe_title']}")
    print(f"🥘 Ingredients: {', '.join(result['final_output']['ingredients'])}")
    
    return result

async def example_character_trend():
    """
    Example: Character trend (Labubu)
    """
    print("\n🍰 EXAMPLE 5: CHARACTER TREND")
    print("=" * 50)
    
    use_case = RecipeGenerationUseCase(
        gemini_api_key=settings.GEMINI_API_KEY,
        news_api_key=settings.NEWS_API_KEY,
        youtube_api_key=settings.YOUTUBE_API_KEY
    )
    
    # Labubu character trend
    trend_keywords = ['labubu', 'cute', 'kawaii', 'pastel', 'character']
    user_segment = UserSegment.GEN_Z
    available_ingredients = [
        'flour', 'sugar', 'eggs', 'butter', 'vanilla',
        'strawberry', 'cream_cheese', 'food_coloring',
        'sprinkles', 'fondant', 'chocolate_chips'
    ]
    
    result = await use_case.generate_trend_recipe(
        trend_keywords=trend_keywords,
        user_segment=user_segment,
        available_ingredients=available_ingredients,
        target_language='Vietnamese'
    )
    
    print(f"📝 Recipe: {result['final_output']['recipe_title']}")
    print(f"🥘 Ingredients: {', '.join(result['final_output']['ingredients'])}")
    
    return result

async def batch_generation_example():
    """
    Example: Batch generation cho multiple scenarios
    """
    print("\n🍰 EXAMPLE 6: BATCH GENERATION")
    print("=" * 50)
    
    use_case = RecipeGenerationUseCase(
        gemini_api_key=settings.GEMINI_API_KEY,
        news_api_key=settings.NEWS_API_KEY,
        youtube_api_key=settings.YOUTUBE_API_KEY
    )
    
    # Multiple scenarios
    scenarios = [
        {
            'trend_keywords': ['newjeans', 'korean_style', 'aesthetic'],
            'user_segment': UserSegment.GEN_Z,
            'available_ingredients': ['flour', 'sugar', 'eggs', 'butter', 'matcha_powder', 'strawberry'],
            'target_language': 'Korean'
        },
        {
            'trend_keywords': ['keto', 'vegan', 'gluten_free'],
            'user_segment': UserSegment.HEALTH_CONSCIOUS,
            'available_ingredients': ['almond_flour', 'coconut_sugar', 'coconut_oil', 'almond_milk'],
            'target_language': 'English'
        },
        {
            'trend_keywords': ['valentine', 'romantic', 'chocolate'],
            'user_segment': UserSegment.MILLENNIALS,
            'available_ingredients': ['flour', 'sugar', 'eggs', 'butter', 'dark_chocolate', 'strawberry'],
            'target_language': 'Vietnamese'
        }
    ]
    
    results = await use_case.batch_generate_recipes(scenarios)
    
    # Save batch results
    with open('batch_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Saved {len(results)} recipes to 'batch_results.json'")
    
    return results

async def main():
    """
    Main function để chạy tất cả examples
    """
    print("🚀 AI RECIPE GENERATION EXAMPLES")
    print("=" * 60)
    
    try:
        # Example 1: Basic usage
        await example_basic_usage()
        
        # Example 2: Korean trend
        await example_korean_trend()
        
        # Example 3: Health conscious
        await example_health_conscious()
        
        # Example 4: Seasonal trend
        await example_seasonal_trend()
        
        # Example 5: Character trend
        await example_character_trend()
        
        # Example 6: Batch generation
        await batch_generation_example()
        
        print("\n✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
