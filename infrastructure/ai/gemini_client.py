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
Bạn là một đầu bếp bánh ngọt chuyên nghiệp và chuyên gia marketing.

NHIỆM VỤ: Tạo công thức bánh ngọt chi tiết từ các nguyên liệu có sẵn:
- Nguyên liệu: {ingredients}
- Ngôn ngữ: {self._get_language_name(language)}

YÊU CẦU OUTPUT theo format JSON (bằng tiếng {self._get_language_name(language)}):
{{
  "title": "Tên bánh sáng tạo, hấp dẫn",
  "description": "Mô tả chi tiết 3-4 câu về món bánh, nhấn mạnh hương vị và đặc điểm nổi bật",
  "ingredients": [
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}},
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}}
  ],
  "instructions": [
    "Bước 1: Hướng dẫn chi tiết từng bước",
    "Bước 2: Hướng dẫn chi tiết từng bước",
    "Bước 3: Hướng dẫn chi tiết từng bước"
  ],
  "prep_time": "thời gian chuẩn bị chi tiết",
  "cook_time": "thời gian nướng chi tiết", 
  "servings": "số phần ăn",
  "difficulty": "easy/medium/hard",
  "tags": ["tag1", "tag2", "tag3"],
  "decoration_tips": "Gợi ý trang trí đẹp mắt",
  "marketing_caption": "Caption Facebook viral để đăng bán",
  "notes": "Lưu ý quan trọng khi làm bánh"
}}

Hãy tạo công thức chi tiết, khả thi cho tiệm bánh nhỏ. Chỉ trả về JSON, không thêm text khác.
"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens
            },
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        # Check if response is valid
        if response.candidates and response.candidates[0].finish_reason == 1:
            return response.text
        else:
            # Fallback response
            return """{
  "title": "Generated Recipe",
  "description": "A delicious recipe generated for you",
  "ingredients": [
    {"name": "flour", "quantity": "200", "unit": "g"},
    {"name": "sugar", "quantity": "100", "unit": "g"},
    {"name": "eggs", "quantity": "2", "unit": "pieces"}
  ],
  "instructions": [
    "Step 1: Mix all ingredients together",
    "Step 2: Bake at 180°C for 25 minutes"
  ],
  "prep_time": "15 minutes",
  "cook_time": "25 minutes",
  "servings": "4 servings",
  "difficulty": "easy"
}"""
    
    def generate_creative_recipe(self, 
                               trend: str,
                               user_segment: str,
                               occasion: Optional[str] = None,
                               language: str = "vi") -> str:
        """Generate creative recipe based on trend and user segment"""
        self._ensure_config()
        model = genai.GenerativeModel(self.model)
        
        prompt = f"""
Bạn là một đầu bếp bánh ngọt chuyên nghiệp và chuyên gia marketing với 10+ năm kinh nghiệm.

NHIỆM VỤ: Tạo công thức bánh ngọt CHI TIẾT và SÁNG TẠO phù hợp với:
- Xu hướng (Trend): {trend}
- Đối tượng khách hàng: {user_segment}
- Dịp/Sự kiện: {occasion or 'hàng ngày'}

YÊU CẦU OUTPUT theo format JSON (bằng tiếng {self._get_language_name(language)}):
{{
  "title": "Tên bánh sáng tạo, bắt trend, dễ nhớ",
  "description": "Mô tả chi tiết 4-5 câu về món bánh, nhấn mạnh hương vị, kết cấu và điểm nổi bật",
  "ingredients": [
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}},
    {{"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}}
  ],
  "instructions": [
    "Bước 1: Hướng dẫn chi tiết từng bước với lưu ý kỹ thuật",
    "Bước 2: Hướng dẫn chi tiết từng bước với lưu ý kỹ thuật",
    "Bước 3: Hướng dẫn chi tiết từng bước với lưu ý kỹ thuật"
  ],
  "prep_time": "thời gian chuẩn bị chi tiết (bao gồm cả thời gian chờ)",
  "cook_time": "thời gian nướng chi tiết với nhiệt độ cụ thể", 
  "servings": "số phần ăn",
  "difficulty": "easy/medium/hard",
  "tags": ["tag1", "tag2", "tag3", "tag4"],
  "decoration_tips": "Gợi ý trang trí chi tiết phù hợp với trend và đối tượng khách hàng",
  "marketing_caption": "Caption Facebook viral dài 2-3 câu để đăng bán, có hashtag",
  "notes": "Lưu ý quan trọng khi làm bánh, tips thành công"
}}

Hãy tạo công thức CHI TIẾT, SÁNG TẠO và KHẢ THI cho tiệm bánh nhỏ. Chỉ trả về JSON, không thêm text khác.
"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens
            },
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        # Check if response is valid
        if response.candidates and response.candidates[0].finish_reason == 1:
            return response.text
        else:
            # Fallback response
            return """{
  "title": "Generated Recipe",
  "description": "A delicious recipe generated for you",
  "ingredients": [
    {"name": "flour", "quantity": "200", "unit": "g"},
    {"name": "sugar", "quantity": "100", "unit": "g"},
    {"name": "eggs", "quantity": "2", "unit": "pieces"}
  ],
  "instructions": [
    "Step 1: Mix all ingredients together",
    "Step 2: Bake at 180°C for 25 minutes"
  ],
  "prep_time": "15 minutes",
  "cook_time": "25 minutes",
  "servings": "4 servings",
  "difficulty": "easy"
}"""
    
    def _get_language_name(self, code: str) -> str:
        return "Việt" if code == "vi" else "English"
    
    def _generate_simple_recipe(self, trend: str, user_segment: str, occasion: str, language: str) -> str:
        """Generate simple recipe when main generation fails"""
        if language == "vi":
            return f"""{{
  "title": "Bánh {trend} Đặc Biệt",
  "description": "Món bánh ngọt thơm ngon, bắt trend {trend} được thiết kế đặc biệt cho {user_segment}. Với hương vị đậm đà và kết cấu mềm mịn, đây là lựa chọn hoàn hảo cho dịp {occasion}. Bánh có vị ngọt vừa phải, thơm lừng và dễ ăn, phù hợp với mọi lứa tuổi.",
  "ingredients": [
    {{"name": "bột mì đa dụng", "quantity": "250", "unit": "g"}},
    {{"name": "đường cát trắng", "quantity": "120", "unit": "g"}},
    {{"name": "trứng gà", "quantity": "3", "unit": "quả"}},
    {{"name": "bơ lạt", "quantity": "100", "unit": "g"}},
    {{"name": "sữa tươi không đường", "quantity": "80", "unit": "ml"}},
    {{"name": "tinh chất vanilla", "quantity": "5", "unit": "ml"}},
    {{"name": "baking powder", "quantity": "1", "unit": "muỗng cà phê"}},
    {{"name": "muối", "quantity": "1/4", "unit": "muỗng cà phê"}}
  ],
  "instructions": [
    "Bước 1: Làm nóng lò nướng ở 175°C (lửa trên và lửa dưới). Lót giấy nến vào khuôn bánh tròn 20cm.",
    "Bước 2: Rây bột mì, baking powder và muối vào một tô lớn. Trộn đều và để sang một bên.",
    "Bước 3: Trong tô khác, đánh bông bơ với đường bằng máy đánh trứng ở tốc độ trung bình trong 3-4 phút đến khi hỗn hợp bông xốp và chuyển màu vàng nhạt.",
    "Bước 4: Cho từng quả trứng vào một, đánh đều sau mỗi lần cho trứng. Thêm vanilla và đánh thêm 1 phút.",
    "Bước 5: Chia hỗn hợp bột khô làm 3 phần. Cho xen kẽ bột và sữa tươi vào hỗn hợp bơ trứng, bắt đầu và kết thúc bằng bột. Trộn nhẹ nhàng bằng phới dẹt.",
    "Bước 6: Đổ bột vào khuôn đã chuẩn bị. Đập nhẹ khuôn xuống bàn để vỡ bọt khí lớn. Nướng trong 35-40 phút đến khi bánh chín vàng và xiên tăm vào rút ra thấy khô.",
    "Bước 7: Lấy bánh ra khỏi lò, để nguội 10 phút trong khuôn rồi lật ngược lên rack để nguội hoàn toàn."
  ],
  "prep_time": "25 phút (không tính thời gian nguội)",
  "cook_time": "40 phút ở 175°C",
  "servings": "8-10 phần",
  "difficulty": "medium",
  "tags": ["{trend}", "{user_segment}", "{occasion}", "homemade"],
  "decoration_tips": "Trang trí theo phong cách {trend} với kem tươi, trái cây tươi hoặc chocolate. Sử dụng màu sắc pastel cho {user_segment} để tạo cảm giác dễ thương và hiện đại.",
  "marketing_caption": "🎂 Bánh {trend} đặc biệt dành cho {user_segment}! Với hương vị thơm ngon và thiết kế bắt trend, đây chính là món quà hoàn hảo cho dịp {occasion}. Đặt ngay để không bỏ lỡ! #Banh{trend} #BanhNgot #Homemade",
  "notes": "Lưu ý quan trọng: Đảm bảo tất cả nguyên liệu ở nhiệt độ phòng. Không trộn bột quá kỹ để tránh bánh bị chai. Kiểm tra bánh chín bằng cách xiên tăm vào giữa bánh."
}}"""
        else:
            return f"""{{
  "title": "{trend} Special Cake",
  "description": "A delicious and trendy {trend} cake specially designed for {user_segment}. With rich flavor and soft texture, this is the perfect choice for {occasion}. The cake has a balanced sweetness, aromatic and easy to eat, suitable for all ages.",
  "ingredients": [
    {{"name": "all-purpose flour", "quantity": "250", "unit": "g"}},
    {{"name": "white sugar", "quantity": "120", "unit": "g"}},
    {{"name": "eggs", "quantity": "3", "unit": "pieces"}},
    {{"name": "unsalted butter", "quantity": "100", "unit": "g"}},
    {{"name": "fresh milk", "quantity": "80", "unit": "ml"}},
    {{"name": "vanilla extract", "quantity": "5", "unit": "ml"}},
    {{"name": "baking powder", "quantity": "1", "unit": "teaspoon"}},
    {{"name": "salt", "quantity": "1/4", "unit": "teaspoon"}}
  ],
  "instructions": [
    "Step 1: Preheat oven to 175°C (top and bottom heat). Line a 20cm round cake pan with parchment paper.",
    "Step 2: Sift flour, baking powder and salt into a large bowl. Mix well and set aside.",
    "Step 3: In another bowl, cream butter with sugar using electric mixer at medium speed for 3-4 minutes until fluffy and light yellow.",
    "Step 4: Add eggs one at a time, beating well after each addition. Add vanilla and beat for another minute.",
    "Step 5: Divide dry ingredients into 3 parts. Alternately add flour mixture and milk to butter mixture, starting and ending with flour. Mix gently with spatula.",
    "Step 6: Pour batter into prepared pan. Tap pan lightly on counter to remove large air bubbles. Bake for 35-40 minutes until golden and toothpick inserted comes out clean.",
    "Step 7: Remove from oven, cool in pan for 10 minutes then invert onto wire rack to cool completely."
  ],
  "prep_time": "25 minutes (not including cooling time)",
  "cook_time": "40 minutes at 175°C",
  "servings": "8-10 servings",
  "difficulty": "medium",
  "tags": ["{trend}", "{user_segment}", "{occasion}", "homemade"],
  "decoration_tips": "Decorate in {trend} style with fresh cream, fresh fruits or chocolate. Use pastel colors for {user_segment} to create cute and modern feeling.",
  "marketing_caption": "🎂 Special {trend} cake for {user_segment}! With delicious flavor and trendy design, this is the perfect gift for {occasion}. Order now to not miss out! #Cake{trend} #SweetCake #Homemade",
  "notes": "Important notes: Ensure all ingredients are at room temperature. Don't overmix batter to avoid tough cake. Check doneness by inserting toothpick in center of cake."
}}"""