# domain/entities/recipe.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .ingredient import Ingredient

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Recipe(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    servings: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = DifficultyLevel.MEDIUM
    tags: List[str] = []
    created_at: datetime = datetime.now()
    language: str = "vi"
    trend_context: Optional[str] = None
    user_segment: Optional[str] = None