# infrastructure/db/models.py
from sqlalchemy import Column, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RecipeModel(Base):
    __tablename__ = "recipes"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    tags = Column(JSON)
    language = Column(String, default="vi")
    created_at = Column(DateTime, default=datetime.utcnow)
    
class TrendModel(Base):
    __tablename__ = "trends"
    
    id = Column(String, primary_key=True)
    keyword = Column(String, nullable=False)
    score = Column(Float, default=0.0)
    platform = Column(String)
    region = Column(String, default="VN")
    collected_at = Column(DateTime, default=datetime.utcnow)