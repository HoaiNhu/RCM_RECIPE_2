# app/routers/recipes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from application.use_cases.generate_personalized_recipe_use_case import GeneratePersonalizedRecipeUseCase

router = APIRouter(prefix="/recipes", tags=["recipes"])
use_case = GeneratePersonalizedRecipeUseCase()

class IngredientsRequest(BaseModel):
    ingredients: str
    language: str = "vi"

class TrendRequest(BaseModel):
    trend: str
    user_segment: str
    occasion: Optional[str] = None
    language: str = "vi"

@router.post("/generate-from-ingredients")
async def generate_from_ingredients(request: IngredientsRequest):
    """Generate recipe from ingredients list"""
    try:
        result = use_case.execute_from_ingredients(
            ingredients=request.ingredients,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-from-trend")
async def generate_from_trend(request: TrendRequest):
    """Generate recipe from trend and user segment"""
    try:
        result = use_case.execute_from_trend(
            trend=request.trend,
            user_segment=request.user_segment,
            occasion=request.occasion,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "recipes"}