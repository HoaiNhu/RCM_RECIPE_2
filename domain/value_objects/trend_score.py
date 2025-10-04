# domain/value_objects/trend_score.py
from pydantic import BaseModel

class TrendScore(BaseModel):
    relevance: float  # 0-1
    popularity: float  # 0-1
    longevity: float  # 0-1
    
    @property
    def total_score(self) -> float:
        return (self.relevance * 0.4 + 
                self.popularity * 0.4 + 
                self.longevity * 0.2)
    
    class Config:
        frozen = True