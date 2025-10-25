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

 YÊU CẦU OUTPUT theo format JSON (bằng {self._get_language_name(language)}):
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
        
        # Prefer response text nếu có
        if getattr(response, "text", None):
            return response.text
        # Fallback: tạo công thức chi tiết theo ngôn ngữ
        return self._generate_simple_recipe(trend="từ nguyên liệu", user_segment="general", occasion="hàng ngày", language=language)
    
    def generate_creative_recipe(self, 
                               trend: str,
                               user_segment: str,
                               occasion: Optional[str] = None,
                               language: str = "vi") -> str:
        """Generate creative recipe based on trend and user segment"""
        self._ensure_config()
        model = genai.GenerativeModel(self.model)
        
        # Map user segments to detailed descriptions
        segment_profiles = {
            "gen_z": "Gen Z (18-25 tuổi): thích màu sắc rực rỡ, Instagram-worthy, viral trên TikTok, quan tâm đến giá cả hợp lý",
            "millennials": "Millennials (26-40 tuổi): quan tâm đến chất lượng nguyên liệu organic, thiết kế tinh tế, sẵn sàng trả giá cao hơn cho sản phẩm premium",
            "gym": "Gym Enthusiast: ưu tiên high protein, low carb, low sugar, healthy ingredients, cần thông tin dinh dưỡng rõ ràng",
            "kids": "Trẻ em & Phụ huynh: an toàn thực phẩm, màu sắc tươi sáng, hình dáng dễ thương, vị ngọt vừa phải, không chất bảo quản",
            "health": "Sức khỏe: organic, ít đường, không gluten (nếu có thể), nguyên liệu tự nhiên, tốt cho tiêu hóa"
        }
        
        segment_desc = segment_profiles.get(user_segment, f"Khách hàng {user_segment}")
        
        prompt = f"""
Bạn là BÀ TRẦN KIM CHI - Đầu bếp bánh ngọt 15 năm kinh nghiệm, từng làm việc tại Pháp, chuyên gia tư vấn cho hơn 200 tiệm bánh tại Việt Nam.

════════════════════════════════════════════════════════════
🎯 NHIỆM VỤ: Tạo công thức bánh ngọt SÁNG TẠO & KHẢ THI
════════════════════════════════════════════════════════════

📊 THÔNG TIN ĐẦU VÀO:
├─ Xu hướng (Trend): {trend}
├─ Đối tượng khách hàng: {segment_desc}
└─ Dịp/Sự kiện: {occasion or 'bán hàng ngày'}

════════════════════════════════════════════════════════════
✅ YÊU CẦU CÔNG THỨC (bằng {self._get_language_name(language)}):
════════════════════════════════════════════════════════════

1. TÊN BÁNH:
   - Sáng tạo, bắt trend {trend}
   - Dễ nhớ, dễ đọc, viral được trên mạng xã hội
   - Gợi lên cảm xúc và sự tò mò

2. MÔ TẢ:
   - 3-4 câu SINH ĐỘNG về món bánh
   - Nhấn mạnh: hương vị, kết cấu, điểm độc đáo
   - Kết nối cảm xúc với {segment_desc}
   - Tạo sự hấp dẫn để khách muốn mua ngay

3. NGUYÊN LIỆU:
   - Danh sách CHI TIẾT, CHÍNH XÁC
   - Định lượng CỤ THỂ (gram, ml, muỗng)
   - Ưu tiên nguyên liệu DỄ TÌM tại Việt Nam
   - Phù hợp với đối tượng {user_segment}

4. CÁCH LÀM:
   - Hướng dẫn TỪNG BƯỚC rõ ràng, dễ hiểu
   - Bao gồm: nhiệt độ, thời gian, kỹ thuật cụ thể
   - Thêm TIPS nhỏ trong mỗi bước để thành công
   - Phù hợp cho tiệm bánh nhỏ (không cần máy móc phức tạp)

5. TRANG TRÍ:
   - Gợi ý trang trí phù hợp với trend {trend}
   - Dễ thực hiện, đẹp mắt, Instagram-worthy
   - Tối ưu cho {segment_desc}

6. CAPTION FACEBOOK:
   - 2-3 câu VIRAL, thu hút
   - Sử dụng emoji phù hợp
   - Có call-to-action rõ ràng
   - Kèm 3-5 hashtag trending

════════════════════════════════════════════════════════════
📋 FORMAT OUTPUT - JSON:
════════════════════════════════════════════════════════════

{{
  "title": "Tên Bánh Sáng Tạo Bắt Trend",
  "description": "Mô tả sinh động, hấp dẫn, kết nối cảm xúc. Nhấn mạnh hương vị độc đáo và lý do khách hàng {user_segment} sẽ yêu thích món này. Tạo sự tò mò và mong muốn được thử.",
  "ingredients": [
    {{"name": "tên nguyên liệu chính xác", "quantity": "số lượng cụ thể", "unit": "đơn vị (g/ml/muỗng)"}},
    {{"name": "ví dụ: bột mì đa dụng", "quantity": "250", "unit": "g"}},
    {{"name": "ví dụ: đường cát trắng", "quantity": "120", "unit": "g"}}
  ],
  "instructions": [
    "Bước 1: Hướng dẫn chi tiết với nhiệt độ/thời gian cụ thể. Lưu ý kỹ thuật quan trọng.",
    "Bước 2: Tiếp tục hướng dẫn rõ ràng. Tips để thành công.",
    "Bước 3: Các bước tiếp theo với thông tin đầy đủ..."
  ],
  "prep_time": "X phút/giờ (ghi rõ từng phần: chuẩn bị, ủ, làm lạnh...)",
  "cook_time": "X phút ở Y°C (ghi rõ: nướng/hấp/làm lạnh, nhiệt độ chính xác)",
  "servings": "X-Y người / Z phần (cụ thể)",
  "difficulty": "easy/medium/hard (đánh giá thực tế)",
  "tags": ["#{trend}", "#{user_segment}", "thêm 2-3 tags liên quan"],
  "decoration_tips": "Gợi ý trang trí CỤ THỂ phù hợp với {trend}. Hướng dẫn ngắn gọn cách làm. Màu sắc/họa tiết phù hợp với {segment_desc}.",
  "marketing_caption": "🎂 Caption viral 2-3 câu với emoji! Tạo cảm giác FOMO. Có call-to-action. #Hashtag1 #Hashtag2 #Hashtag3",
  "notes": "Lưu ý QUAN TRỌNG để bánh thành công. Tips tránh lỗi thường gặp. Cách bảo quản và thời hạn sử dụng."
}}

════════════════════════════════════════════════════════════
⚠️ LƯU Ý QUAN TRỌNG:
════════════════════════════════════════════════════════════
✓ Công thức PHẢI khả thi cho tiệm bánh nhỏ
✓ Nguyên liệu dễ tìm tại Việt Nam
✓ Không cần máy móc đắt tiền, phức tạp
✓ Thời gian làm hợp lý (không quá 4-5 giờ)
✓ Chi phí nguyên liệu hợp lý với đối tượng
✓ An toàn thực phẩm, không dùng chất cấm

════════════════════════════════════════════════════════════

CHỈ TRẢ VỀ JSON, KHÔNG THÊM TEXT KHÁC.
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
        
        if getattr(response, "text", None):
            return response.text
        return self._generate_simple_recipe(trend=trend, user_segment=user_segment, occasion=occasion or "hàng ngày", language=language)
    
    def _get_language_name(self, code: str) -> str:
        return "tiếng Việt" if code == "vi" else "tiếng Anh"
    
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