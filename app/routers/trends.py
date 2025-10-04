# app/routers/trends.py
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/trends", tags=["trends"])

class TrendResponse(BaseModel):
    keyword: str
    score: float
    platform: str

@router.get("/current", response_model=List[TrendResponse])
async def get_current_trends():
    """Get current trending topics"""
    # Mock data for now - replace with actual trend service
    return [
        {"keyword": "Labubu", "score": 0.92, "platform": "TikTok"},
        {"keyword": "Matcha", "score": 0.85, "platform": "Instagram"},
        {"keyword": "Minimalist", "score": 0.78, "platform": "Pinterest"}
    ]

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "trends"}