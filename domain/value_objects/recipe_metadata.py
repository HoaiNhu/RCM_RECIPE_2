# domain/value_objects/recipe_metadata.py
from pydantic import BaseModel
from typing import List, Optional

class RecipeMetadata(BaseModel):
    trend_alignment_score: float = 0.0
    user_segment_match: List[str] = []
    occasion: Optional[str] = None
    season: Optional[str] = None
    
    class Config:
        frozen = True