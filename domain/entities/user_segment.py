# domain/entities/user_segment.py
from pydantic import BaseModel
from typing import List, Dict

class UserSegment(BaseModel):
    code: str  # genz, kids, gym, elderly
    name: str
    description: str
    age_range: Optional[str] = None
    preferences: Dict[str, List[str]] = {}
    
    class Config:
        frozen = True