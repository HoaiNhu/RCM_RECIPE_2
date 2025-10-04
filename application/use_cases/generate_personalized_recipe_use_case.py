# application/use_cases/generate_personalized_recipe_use_case.py
from typing import Dict, Optional
from domain.services.recipe_generation_service import RecipeGenerationService
from domain.entities.recipe import Recipe

class GeneratePersonalizedRecipeUseCase:
    def __init__(self):
        self.recipe_service = RecipeGenerationService()
    
    def execute_from_ingredients(self, ingredients: str, language: str = "vi") -> Dict:
        """Generate recipe from ingredients"""
        recipe = self.recipe_service.generate_from_ingredients(ingredients, language)
        
        return {
            "status": "success",
            "data": recipe.dict()
        }
    
    def execute_from_trend(self, 
                          trend: str,
                          user_segment: str,
                          occasion: Optional[str] = None,
                          language: str = "vi") -> Dict:
        """Generate recipe from trend and user segment"""
        recipe = self.recipe_service.generate_from_trend(
            trend=trend,
            user_segment=user_segment,
            occasion=occasion,
            language=language
        )
        
        return {
            "status": "success",
            "data": recipe.dict()
        }