# app/routers/segments.py
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/segments", tags=["user-segments"])

class UserSegmentResponse(BaseModel):
    code: str
    name: str
    description: str

@router.get("/", response_model=List[UserSegmentResponse])
async def get_user_segments():
    """Get all user segments"""
    return [
        {
            "code": "genz",
            "name": "Gen Z (10-25 tuổi)",
            "description": "Thích trend viral, màu pastel, aesthetic"
        },
        {
            "code": "millennials",
            "name": "Millennials (26-40 tuổi)",
            "description": "Ưa chuộng chất lượng, artisan, organic"
        },
        {
            "code": "gym",
            "name": "Dân Gym",
            "description": "Ít đường, nhiều protein, healthy"
        },
        {
            "code": "kids",
            "name": "Trẻ em (3-12 tuổi)",
            "description": "Màu sắc, hình thù ngộ nghĩnh, vị ngọt vừa"
        }
    ]