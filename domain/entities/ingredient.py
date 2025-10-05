# domain/entities/ingredient.py
from pydantic import BaseModel
from typing import Optional

class Ingredient(BaseModel):
    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    
    class Config:
        frozen = True