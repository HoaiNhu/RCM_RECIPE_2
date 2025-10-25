# domain/services/recipe_generation_service.py
from typing import Dict, List, Optional, Tuple
import re
from domain.entities.recipe import Recipe, DifficultyLevel
from domain.entities.ingredient import Ingredient
from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ai.translator_service import TranslatorService
from infrastructure.ai.recipe_parser import RecipeParser
from infrastructure.external.t5_client import T5Client


QUANTITY_UNIT_PATTERN = re.compile(
    r"^(?:[-\s]*)?(?P<qty>(?:\d+[\/,\.]?\d*|\d*\.?\d+))\s*(?P<unit>(?:g|kg|mg|ml|l|tsp|tbsp|teaspoon|tablespoon|cup|cups|gram|grams|kilogram|liter|liters|ounce|oz|lb|lbs|muỗng|thìa|muong|ml|lít|gr|chén|cốc)\b)?\s*(?P<name>.*)$",
    re.IGNORECASE,
)


def parse_ingredient_line(line: str) -> Ingredient:
    """Parse one ingredient line to Ingredient(name, quantity, unit).
    Fallback gracefully if cannot parse quantity/unit.
    """
    cleaned = line.lstrip("- •\t ")
    match = QUANTITY_UNIT_PATTERN.match(cleaned)
    if match:
        name = match.group("name").strip() or cleaned
        qty = match.group("qty")
        unit = match.group("unit")
        # normalize decimal comma to dot
        if qty and "," in qty and "/" not in qty:
            qty = qty.replace(",", ".")
        quantity_str = qty if qty else None
        unit_str = unit.lower() if unit else None
        return Ingredient(name=name, quantity=quantity_str, unit=unit_str)
    return Ingredient(name=cleaned)


class RecipeGenerationService:
    def __init__(self, use_t5: bool = True):
        self.gemini = GeminiClient()
        self.translator = TranslatorService()
        self.parser = RecipeParser()
        self.use_t5 = use_t5
        
        # Initialize T5 client nếu được enable
        if self.use_t5:
            try:
                self.t5_client = T5Client()
                print("✅ T5 Model initialized successfully")
            except Exception as e:
                print(f"⚠️ T5 Model initialization failed: {e}")
                print("   Falling back to Gemini-only mode")
                self.use_t5 = False
                self.t5_client = None
        else:
            self.t5_client = None
    
    def generate_from_ingredients(self, ingredients: str, language: str = "vi") -> Recipe:
        """
        Generate recipe from ingredients using T5 model + Gemini translation.
        
        Workflow:
        1. Translate Vietnamese ingredients → English (if needed)
        2. Generate recipe with T5 model (English output)
        3. Enhance & translate recipe to Vietnamese with Gemini (if needed)
        """
        
        # Strategy 1: Use T5 + Gemini Translation
        if self.use_t5 and self.t5_client:
            try:
                print(f"🤖 Using T5 Model for recipe generation...")
                
                # Step 1: Translate ingredients to English if Vietnamese
                if language == "vi":
                    print(f"🔄 Translating ingredients: {ingredients[:50]}...")
                    en_ingredients = self.translator.vi_to_en(ingredients)
                    print(f"✅ Translated to: {en_ingredients[:50]}...")
                else:
                    en_ingredients = ingredients
                
                # Step 2: Generate recipe with T5 (English output)
                print(f"🍰 Generating recipe with T5...")
                t5_recipe_text = self.t5_client.generate_recipe(en_ingredients)
                print(f"✅ T5 generated: {t5_recipe_text[:100]}...")
                if "directions:" not in t5_recipe_text.lower():
                    print(f"⚠️ Warning: T5 output missing 'directions' section")
                
                # Step 3: Enhance and translate with Gemini
                if language == "vi":
                    print(f"🔄 Translating & enhancing with Gemini...")
                    enhanced_recipe = self._enhance_and_translate_t5_output(
                        t5_recipe_text, en_ingredients, language
                    )
                else:
                    enhanced_recipe = self._enhance_t5_output(t5_recipe_text, en_ingredients)
                
                print(f"✅ T5 pipeline completed successfully!")
                return self._parse_recipe_response(enhanced_recipe, language)
                
            except Exception as e:
                print(f"⚠️ T5 pipeline failed: {e}")
                print(f"   Falling back to Gemini-only mode...")
        
        # Strategy 2: Fallback to Gemini-only
        print(f"🤖 Using Gemini for recipe generation...")
        recipe_text = self.gemini.generate_recipe_from_ingredients(ingredients, language)
        return self._parse_recipe_response(recipe_text, language)
    
    def generate_from_trend(self, 
                          trend: str, 
                          user_segment: str,
                          occasion: Optional[str] = None,
                          language: str = "vi") -> Recipe:
        """Generate creative recipe based on trend and user segment"""
        recipe_data = self.gemini.generate_creative_recipe(
            trend=trend,
            user_segment=user_segment,
            occasion=occasion,
            language=language
        )
        # Parse, có fallback nếu thiếu dữ liệu
        return self._parse_recipe_response(
            recipe_data, language, trend=trend, user_segment=user_segment, occasion=occasion
        )
    
    def _parse_recipe_response(self, response: str, language: str, *, trend: Optional[str] = None, user_segment: Optional[str] = None, occasion: Optional[str] = None) -> Recipe:
        """Parse model response into Recipe entity using improved parser.
        Nếu dữ liệu thiếu (title/ingredients/instructions), fallback sinh công thức chi tiết rồi parse lại.
        """
        # Parse lần 1
        parsed_data = self.parser.parse_gemini_output(response)
        
        # Debug logging
        print(f"🔍 Parsed data check:")
        print(f"   - Title: {parsed_data.get('title', 'MISSING')}")
        print(f"   - Ingredients: {len(parsed_data.get('ingredients', []))} items")
        print(f"   - Instructions: {len(parsed_data.get('instructions', []))} steps")

        def _is_incomplete(d: dict) -> bool:
            is_incomplete = not d.get('ingredients') or not d.get('instructions') or (d.get('title') in [None, '', 'Untitled Recipe'])
            if is_incomplete:
                print(f"   ❌ Recipe incomplete, triggering fallback...")
            else:
                print(f"   ✅ Recipe complete!")
            return is_incomplete

        # Fallback: generate simple detailed recipe theo ngôn ngữ yêu cầu
        if _is_incomplete(parsed_data):
            fallback_text = self.gemini._generate_simple_recipe(
                trend=trend or 'bánh ngọt',
                user_segment=user_segment or 'khách hàng',
                occasion=occasion or 'hàng ngày',
                language=language
            )
            parsed_data = self.parser.parse_gemini_output(fallback_text)

        # Convert ingredients to Ingredient objects
        recipe_ingredients = []
        for ing_data in parsed_data.get('ingredients', []):
            recipe_ingredients.append(Ingredient(
                name=ing_data.get('name', ''),
                quantity=ing_data.get('quantity', '1'),
                unit=ing_data.get('unit'),
                category=self._categorize_ingredient(ing_data.get('name', ''))
            ))

        # Convert difficulty
        difficulty_map = {
            'easy': DifficultyLevel.EASY,
            'medium': DifficultyLevel.MEDIUM,
            'hard': DifficultyLevel.HARD
        }
        difficulty = difficulty_map.get(parsed_data.get('difficulty', 'medium'), DifficultyLevel.MEDIUM)

        return Recipe(
            title=parsed_data.get('title', 'Generated Recipe'),
            description=parsed_data.get('description', ''),
            ingredients=recipe_ingredients,
            instructions=parsed_data.get('instructions', []),
            prep_time=parsed_data.get('prep_time', '30 phút'),
            cook_time=parsed_data.get('cook_time', '25 phút'),
            servings=parsed_data.get('servings', '8 phần'),
            difficulty=difficulty,
            tags=parsed_data.get('tags', []),
            trend_context=(f"{trend} | {occasion}" if trend else "Generated from trend"),
            user_segment=user_segment or 'general',
            language=language
        )
    
    def _categorize_ingredient(self, ingredient_name: str) -> str:
        """Categorize ingredient based on name"""
        ingredient_lower = ingredient_name.lower()
        
        if any(word in ingredient_lower for word in ['flour', 'bột', 'sugar', 'đường', 'salt', 'muối', 'baking']):
            return 'dry_ingredients'
        elif any(word in ingredient_lower for word in ['egg', 'trứng', 'milk', 'sữa', 'butter', 'bơ', 'cream']):
            return 'dairy_eggs'
        elif any(word in ingredient_lower for word in ['fruit', 'trái cây', 'berry', 'strawberry', 'dâu']):
            return 'fruits'
        elif any(word in ingredient_lower for word in ['chocolate', 'socola', 'cocoa', 'vanilla', 'vanilla']):
            return 'flavorings'
        else:
            return 'other'
    
    def _enhance_and_translate_t5_output(self, t5_text: str, ingredients: str, language: str) -> str:
        """
        Enhance T5 output và translate sang Vietnamese với Gemini.
        T5 thường output format đơn giản, cần enhance thêm details.
        """
        
        prompt = f"""
Bạn là chuyên gia bánh ngọt chuyên nghiệp. Nhiệm vụ của bạn là:

1. Dịch công thức bánh sau từ tiếng Anh sang tiếng Việt
2. Bổ sung thêm chi tiết để công thức đầy đủ và dễ hiểu hơn
3. Thêm thông tin về thời gian, độ khó, tips và marketing

CÔNG THỨC GỐC (English):
{t5_text}

NGUYÊN LIỆU ĐÃ DÙNG:
{ingredients}

YÊU CẦU OUTPUT (JSON format tiếng Việt):
{{
  "title": "Tên bánh dịch sang tiếng Việt, có thể sáng tạo thêm",
  "description": "Mô tả chi tiết 3-4 câu về món bánh",
  "ingredients": [
    {{"name": "nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}}
  ],
  "instructions": [
    "Bước 1: Chi tiết cách làm",
    "Bước 2: Chi tiết cách làm"
  ],
  "prep_time": "thời gian chuẩn bị (VD: 30 phút)",
  "cook_time": "thời gian nướng + nhiệt độ (VD: 35 phút ở 175°C)",
  "servings": "số phần ăn (VD: 8-10 phần)",
  "difficulty": "easy/medium/hard",
  "tags": ["tag1", "tag2", "tag3"],
  "decoration_tips": "Gợi ý trang trí",
  "marketing_caption": "Caption bán hàng Facebook với emoji và hashtag",
  "notes": "Lưu ý quan trọng khi làm bánh"
}}

Chỉ trả về JSON, không thêm text khác.
"""
        
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel(self.gemini.model)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 4096
                },
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Xử lý response an toàn
            try:
                # Cách 1: Thử truy cập text trực tiếp
                if hasattr(response, 'text') and response.text:
                    return response.text
            except ValueError as ve:
                # Cách 2: Nếu response phức tạp, truy cập qua parts
                print(f"⚠️ Response không phải simple text, extracting từ parts...")
                if response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        # Ghép tất cả text parts lại
                        text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        if text_parts:
                            return ''.join(text_parts)
                
                print(f"⚠️ Không thể extract text từ response: {ve}")
            
            # Fallback: parse T5 text and translate
            print("⚠️ Gemini response empty hoặc bị block, parsing T5 output directly...")
            return self._parse_and_translate_t5_text(t5_text, ingredients)
                
        except Exception as e:
            print(f"⚠️ Gemini enhancement failed: {e}")
            # Fallback: parse T5 text and translate to structured format
            return self._parse_and_translate_t5_text(t5_text, ingredients)
    
    def _enhance_t5_output(self, t5_text: str, ingredients: str) -> str:
        """
        Enhance T5 output (English) với Gemini - không translate.
        Thêm details, format chuẩn JSON.
        """
        
        prompt = f"""
You are a professional pastry chef. Your task is to enhance this recipe with more details:

ORIGINAL RECIPE:
{t5_text}

INGREDIENTS USED:
{ingredients}

REQUIREMENTS - Output in JSON format:
{{
  "title": "Recipe name",
  "description": "Detailed 3-4 sentences about the cake",
  "ingredients": [
    {{"name": "ingredient", "quantity": "amount", "unit": "unit"}}
  ],
  "instructions": [
    "Step 1: Detailed instructions",
    "Step 2: Detailed instructions"
  ],
  "prep_time": "preparation time (e.g., 30 minutes)",
  "cook_time": "baking time + temperature (e.g., 35 minutes at 175°C)",
  "servings": "number of servings (e.g., 8-10 servings)",
  "difficulty": "easy/medium/hard",
  "tags": ["tag1", "tag2", "tag3"],
  "decoration_tips": "Decoration suggestions",
  "marketing_caption": "Marketing caption for social media",
  "notes": "Important notes for making this cake"
}}

Return only JSON, no additional text.
"""
        
        try:
            import google.generativeai as genai
            model = genai.GenerativeModel(self.gemini.model)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 4096
                },
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Xử lý response an toàn
            try:
                # Cách 1: Thử truy cập text trực tiếp
                if hasattr(response, 'text') and response.text:
                    return response.text
            except ValueError as ve:
                # Cách 2: Nếu response phức tạp, truy cập qua parts
                print(f"⚠️ Response không phải simple text, extracting từ parts...")
                if response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        # Ghép tất cả text parts lại
                        text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        if text_parts:
                            return ''.join(text_parts)
                
                print(f"⚠️ Không thể extract text từ response: {ve}")
            
            # Fallback: return T5 text
            return t5_text
                
        except Exception as e:
            print(f"⚠️ Gemini enhancement failed: {e}")
            return t5_text
    
    def _parse_and_translate_t5_text(self, t5_text: str, original_ingredients: str) -> str:
        """
        Parse T5 raw output và convert sang JSON format tiếng Việt.
        Fallback khi Gemini enhancement fail.
        """
        import json
        import re
        
        print(f"📝 Parsing T5 output: {t5_text[:100]}...")
        
        # T5 output format: "title: xxx ingredients: xxx directions: xxx"
        result = {
            "title": "",
            "description": "",
            "ingredients": [],
            "instructions": [],
            "prep_time": "30 phút",
            "cook_time": "30 phút ở 175°C",
            "servings": "8-10 phần",
            "difficulty": "medium",
            "tags": [],
            "decoration_tips": "",
            "marketing_caption": "",
            "notes": ""
        }
        
        try:
            # Extract title
            title_match = re.search(r'title:\s*([^\n]+?)(?:\s+ingredients:|$)', t5_text, re.IGNORECASE)
            if title_match:
                en_title = title_match.group(1).strip()
                result["title"] = self.translator.en_to_vi(en_title) if en_title else "Bánh Tự Tạo"
                print(f"  ✅ Title: {en_title} → {result['title']}")
            
            # Extract ingredients
            ing_match = re.search(r'ingredients:\s*([^\n]+?)(?:\s+directions:|$)', t5_text, re.IGNORECASE)
            if ing_match:
                en_ingredients_text = ing_match.group(1).strip()
                print(f"  📋 Ingredients found: {en_ingredients_text[:80]}...")
                
                # Parse ingredients list
                # T5 format: "1 cup flour 2 eggs 1/2 cup sugar"
                ing_parts = re.split(r'\s+(?=\d)', en_ingredients_text)
                
                for part in ing_parts:
                    if not part.strip():
                        continue
                    
                    # Match quantity + unit + name
                    ing_parsed = re.match(r'(\d+(?:[\/\.]\d+)?)\s*([a-z]*\.?\s*)(.+)', part.strip(), re.IGNORECASE)
                    
                    if ing_parsed:
                        quantity = ing_parsed.group(1)
                        unit = ing_parsed.group(2).strip()
                        name_en = ing_parsed.group(3).strip()
                        
                        # Translate ingredient name
                        name_vi = self.translator.en_to_vi(name_en)
                        
                        result["ingredients"].append({
                            "name": name_vi,
                            "quantity": quantity,
                            "unit": unit if unit else None
                        })
                
                print(f"  ✅ Parsed {len(result['ingredients'])} ingredients")
            
            # Extract directions/instructions
            dir_match = re.search(r'directions:\s*(.+)', t5_text, re.IGNORECASE | re.DOTALL)
            if dir_match:
                en_directions = dir_match.group(1).strip()
                print(f"  📝 Directions found: {en_directions[:80]}...")
                
                # Split by common separators
                steps = re.split(r'[;.]|\s+(?=\d+[\.)]\s)', en_directions)
                
                for i, step in enumerate(steps, 1):
                    step = step.strip()
                    if len(step) > 10:  # Filter out too short steps
                        step_vi = self.translator.en_to_vi(step)
                        result["instructions"].append(f"Bước {i}: {step_vi}")
                
                print(f"  ✅ Parsed {len(result['instructions'])} steps")
            else:
                # Fallback: Generate simple instructions based on cake type
                print(f"  ⚠️ No directions found in T5 output, generating fallback instructions...")
                cake_type = result["title"].lower()
                
                if "brownie" in cake_type or "chocolate" in cake_type:
                    result["instructions"] = [
                        "Bước 1: Làm nóng lò nướng ở 175°C. Lót giấy nến vào khay nướng.",
                        "Bước 2: Trộn bột mì, bột ca cao, đường và muối trong một tô lớn.",
                        "Bước 3: Đánh tan bơ, thêm trứng và chiết xuất vani, đánh đều.",
                        "Bước 4: Rót hỗn hợp ướt vào hỗn hợp khô, trộn đều đến khi quyện.",
                        "Bước 5: Đổ bột vào khay đã lót giấy, nướng 25-30 phút.",
                        "Bước 6: Kiểm tra độ chín bằng tăm, để nguội trước khi cắt."
                    ]
                else:
                    result["instructions"] = [
                        "Bước 1: Làm nóng lò nướng ở 175°C. Chuẩn bị khuôn bánh.",
                        "Bước 2: Trộn đều các nguyên liệu khô (bột, đường, muối).",
                        "Bước 3: Đánh bông bơ với đường, thêm trứng từng quả.",
                        "Bước 4: Trộn hỗn hợp ướt với hỗn hợp khô, khuấy đều.",
                        "Bước 5: Đổ bột vào khuôn, nướng 30-35 phút.",
                        "Bước 6: Để nguội hoàn toàn trước khi trang trí."
                    ]
                
                print(f"  ✅ Generated {len(result['instructions'])} fallback steps")
            
            # Generate description based on title and ingredients
            if result["title"] and result["ingredients"]:
                main_ings = [ing["name"] for ing in result["ingredients"][:3]]
                result["description"] = f"Món {result['title']} được làm từ {', '.join(main_ings)}. Hương vị thơm ngon, kết cấu mềm mịn, phù hợp cho nhiều dịp."
            
            # Add tags based on title
            if result["title"]:
                result["tags"] = [result["title"].lower(), "homemade", "t5-generated"]
            
            # Generate marketing caption
            result["marketing_caption"] = f"🍰 {result['title']} tự tạo! Thơm ngon và dễ làm. #BanhNgot #Homemade"
            
            print(f"✅ Parsed successfully: {result['title']}")
            
        except Exception as e:
            print(f"⚠️ Parsing failed: {e}, using minimal template")
            result["title"] = "Bánh Tự Tạo"
            result["description"] = "Công thức bánh được tạo từ T5 model"
            result["ingredients"] = [{"name": ing.strip(), "quantity": "1", "unit": None} 
                                    for ing in original_ingredients.split(',')]
            result["instructions"] = ["Trộn các nguyên liệu lại với nhau", "Nướng ở 175°C trong 30-40 phút"]
        
        return json.dumps(result, ensure_ascii=False, indent=2)