# application/use_cases/generate_personalized_recipe_use_case.py
from typing import Dict, Optional
from domain.services.recipe_generation_service import RecipeGenerationService
from domain.entities.recipe import Recipe

class GeneratePersonalizedRecipeUseCase:
    def __init__(self, use_t5: bool = True):
        """
        Initialize use case with T5 model option.
        
        Args:
            use_t5: Enable T5 model for recipe generation (default: True)
        """
        self.recipe_service = RecipeGenerationService(use_t5=use_t5)
    
    def execute_from_ingredients(self, ingredients: str, language: str = "vi", use_t5: Optional[bool] = None) -> Dict:
        """
        Generate recipe from ingredients.
        
        Args:
            ingredients: Comma-separated ingredients
            language: Output language ('vi' or 'en')
            use_t5: Override T5 usage for this request
        """
        # Override service T5 setting if specified
        if use_t5 is not None:
            original_setting = self.recipe_service.use_t5
            self.recipe_service.use_t5 = use_t5
            
            try:
                recipe = self.recipe_service.generate_from_ingredients(ingredients, language)
            finally:
                self.recipe_service.use_t5 = original_setting
        else:
            recipe = self.recipe_service.generate_from_ingredients(ingredients, language)
        
        return {
            "status": "success",
            "model_used": "T5 + Gemini" if self.recipe_service.use_t5 else "Gemini",
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