# domain/services/recipe_generation_service.py
from typing import Dict, List, Optional, Tuple
import re
from domain.entities.recipe import Recipe, DifficultyLevel
from domain.entities.ingredient import Ingredient
from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ai.translator_service import TranslatorService
from infrastructure.ai.recipe_parser import RecipeParser


QUANTITY_UNIT_PATTERN = re.compile(
    r"^(?:[-\s]*)?(?P<qty>(?:\d+[\/,\.]?\d*|\d*\.?\d+))\s*(?P<unit>(?:g|kg|mg|ml|l|tsp|tbsp|teaspoon|tablespoon|cup|cups|gram|grams|kilogram|liter|liters|ounce|oz|lb|lbs|muỗng|thìa|muong|ml|lít|gr|chén|cốc)\b)?\s*(?P<name>.*)$",
    re.IGNORECASE,
)


def parse_ingredient_line(line: str) -> Ingredient:
    """Parse one ingredient line to Ingredient(name, quantity, unit).
    Fallback gracefully if cannot parse quantity/unit.
    """
    cleaned = line.lstrip("- •\t ")
    match = QUANTITY_UNIT_PATTERN.match(cleaned)
    if match:
        name = match.group("name").strip() or cleaned
        qty = match.group("qty")
        unit = match.group("unit")
        # normalize decimal comma to dot
        if qty and "," in qty and "/" not in qty:
            qty = qty.replace(",", ".")
        quantity_str = qty if qty else None
        unit_str = unit.lower() if unit else None
        return Ingredient(name=name, quantity=quantity_str, unit=unit_str)
    return Ingredient(name=cleaned)


class RecipeGenerationService:
    def __init__(self):
        self.gemini = GeminiClient()
        self.translator = TranslatorService()
        self.parser = RecipeParser()
    
    def generate_from_ingredients(self, ingredients: str, language: str = "vi") -> Recipe:
        """Generate recipe from ingredients list using Gemini (T5 disabled for now)"""
        # Use Gemini directly for now (T5 has issues)
        recipe_text = self.gemini.generate_recipe_from_ingredients(ingredients, language)
        
        # Parse and create Recipe object
        return self._parse_recipe_response(recipe_text, language)
    
    def generate_from_trend(self, 
                          trend: str, 
                          user_segment: str,
                          occasion: Optional[str] = None,
                          language: str = "vi") -> Recipe:
        """Generate creative recipe based on trend and user segment"""
        recipe_data = self.gemini.generate_creative_recipe(
            trend=trend,
            user_segment=user_segment,
            occasion=occasion,
            language=language
        )
        # Parse, có fallback nếu thiếu dữ liệu
        return self._parse_recipe_response(
            recipe_data, language, trend=trend, user_segment=user_segment, occasion=occasion
        )
    
    def _parse_recipe_response(self, response: str, language: str, *, trend: Optional[str] = None, user_segment: Optional[str] = None, occasion: Optional[str] = None) -> Recipe:
        """Parse model response into Recipe entity using improved parser.
        Nếu dữ liệu thiếu (title/ingredients/instructions), fallback sinh công thức chi tiết rồi parse lại.
        """
        # Parse lần 1
        parsed_data = self.parser.parse_gemini_output(response)

        def _is_incomplete(d: dict) -> bool:
            return not d.get('ingredients') or not d.get('instructions') or (d.get('title') in [None, '', 'Untitled Recipe'])

        # Fallback: generate simple detailed recipe theo ngôn ngữ yêu cầu
        if _is_incomplete(parsed_data):
            fallback_text = self.gemini._generate_simple_recipe(
                trend=trend or 'bánh ngọt',
                user_segment=user_segment or 'khách hàng',
                occasion=occasion or 'hàng ngày',
                language=language
            )
            parsed_data = self.parser.parse_gemini_output(fallback_text)

        # Convert ingredients to Ingredient objects
        recipe_ingredients = []
        for ing_data in parsed_data.get('ingredients', []):
            recipe_ingredients.append(Ingredient(
                name=ing_data.get('name', ''),
                quantity=ing_data.get('quantity', '1'),
                unit=ing_data.get('unit'),
                category=self._categorize_ingredient(ing_data.get('name', ''))
            ))

        # Convert difficulty
        difficulty_map = {
            'easy': DifficultyLevel.EASY,
            'medium': DifficultyLevel.MEDIUM,
            'hard': DifficultyLevel.HARD
        }
        difficulty = difficulty_map.get(parsed_data.get('difficulty', 'medium'), DifficultyLevel.MEDIUM)

        return Recipe(
            title=parsed_data.get('title', 'Generated Recipe'),
            description=parsed_data.get('description', ''),
            ingredients=recipe_ingredients,
            instructions=parsed_data.get('instructions', []),
            prep_time=parsed_data.get('prep_time', '30 phút'),
            cook_time=parsed_data.get('cook_time', '25 phút'),
            servings=parsed_data.get('servings', '8 phần'),
            difficulty=difficulty,
            tags=parsed_data.get('tags', []),
            trend_context=(f"{trend} | {occasion}" if trend else "Generated from trend"),
            user_segment=user_segment or 'general',
            language=language
        )
    
    def _categorize_ingredient(self, ingredient_name: str) -> str:
        """Categorize ingredient based on name"""
        ingredient_lower = ingredient_name.lower()
        
        if any(word in ingredient_lower for word in ['flour', 'bột', 'sugar', 'đường', 'salt', 'muối', 'baking']):
            return 'dry_ingredients'
        elif any(word in ingredient_lower for word in ['egg', 'trứng', 'milk', 'sữa', 'butter', 'bơ', 'cream']):
            return 'dairy_eggs'
        elif any(word in ingredient_lower for word in ['fruit', 'trái cây', 'berry', 'strawberry', 'dâu']):
            return 'fruits'
        elif any(word in ingredient_lower for word in ['chocolate', 'socola', 'cocoa', 'vanilla', 'vanilla']):
            return 'flavorings'
        else:
            return 'other'