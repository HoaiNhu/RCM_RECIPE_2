# domain/entities/recipe.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .ingredient import Ingredient

class Recipe(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    prep_time: Optional[int] = None  # minutes
    cook_time: Optional[int] = None  # minutes
    servings: Optional[int] = None
    difficulty: Optional[str] = "medium"
    tags: List[str] = []
    created_at: datetime = datetime.now()
    language: str = "vi"