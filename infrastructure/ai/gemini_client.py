# infrastructure/ai/gemini_client.py
import google.generativeai as genai
from configs.settings import settings
from typing import Optional
from dotenv import load_dotenv
load_dotenv()
    
class GeminiClient:
    def __init__(self):
        self.model = settings.DEFAULT_GEMINI_MODEL
        self.temperature = settings.DEFAULT_TEMPERATURE
        self.max_tokens = settings.MAX_OUTPUT_TOKENS
        self._configured = False

    def _ensure_config(self):
        if not self._configured:
            if not getattr(settings, "GEMINI_API_KEY", None):
                raise RuntimeError("GEMINI_API_KEY is not configured. Please set it in environment or .env")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._configured = True
    
    def generate_recipe_from_ingredients(self, ingredients: str, language: str = "vi") -> str:
        """Generate recipe from ingredients using Gemini"""
        self._ensure_config()
        model = genai.GenerativeModel(self.model)
        
        prompt = f"""
Với các nguyên liệu sau: {ingredients}

Hãy tạo một công thức bánh ngọt bằng tiếng {self._get_language_name(language)} theo format JSON:

{{
  "title": "Tên bánh hấp dẫn",
  "description": "Mô tả ngắn 2-3 câu về món bánh",
  "ingredients": [
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}},
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}}
  ],
  "instructions": [
    "Bước 1: Mô tả chi tiết",
    "Bước 2: Mô tả chi tiết"
  ],
  "prep_time": "thời gian chuẩn bị",
  "cook_time": "thời gian nướng",
  "servings": "số phần ăn",
  "difficulty": "easy/medium/hard",
  "tags": ["tag1", "tag2", "tag3"],
  "notes": "Lưu ý quan trọng khi làm bánh"
}}

Chỉ trả về JSON, không thêm text khác.
"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens
            }
        )
        
        return response.text
    
    def generate_creative_recipe(self, 
                               trend: str,
                               user_segment: str,
                               occasion: Optional[str] = None,
                               language: str = "vi") -> str:
        """Generate creative recipe based on trend and user segment"""
        self._ensure_config()
        model = genai.GenerativeModel(self.model)
        
        prompt = f"""
Bạn là một đầu bếp bánh ngọt chuyên nghiệp và chuyên gia marketing.

NHIỆM VỤ: Tạo công thức bánh ngọt phù hợp với:
- Xu hướng (Trend): {trend}
- Đối tượng khách hàng: {user_segment}
- Dịp/Sự kiện: {occasion or 'hàng ngày'}

YÊU CẦU OUTPUT theo format JSON (bằng tiếng {self._get_language_name(language)}):
{{
  "title": "Tên bánh sáng tạo, bắt trend",
  "description": "Mô tả 2-3 câu hấp dẫn về món bánh",
  "ingredients": [
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}},
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}}
  ],
  "instructions": [
    "Bước 1: Hướng dẫn chi tiết",
    "Bước 2: Hướng dẫn chi tiết"
  ],
  "prep_time": "thời gian chuẩn bị",
  "cook_time": "thời gian nướng", 
  "servings": "số phần ăn",
  "difficulty": "easy/medium/hard",
  "tags": ["tag1", "tag2", "tag3"],
  "decoration_tips": "Gợi ý trang trí phù hợp với trend",
  "marketing_caption": "Caption Facebook viral để đăng bán",
  "notes": "Lưu ý quan trọng khi làm bánh"
}}

Chỉ trả về JSON, không thêm text khác. Hãy sáng tạo và đảm bảo công thức khả thi cho tiệm bánh nhỏ.
"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens
            }
        )
        
        return response.text
    
    def _get_language_name(self, code: str) -> str:
        return "Việt" if code == "vi" else "English"