# domain/entities/trend.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Trend(BaseModel):
    keyword: str
    score: float = 0.0
    platform: Optional[str] = None
    region: str = "VN"
    collected_at: datetime = datetime.now()