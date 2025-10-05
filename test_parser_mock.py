#!/usr/bin/env python3
"""Mock Gemini responses để test parser logic"""

import sys
import os
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from infrastructure.ai.recipe_parser import RecipeParser
import json

def test_parser_with_mock_responses():
    """Test parser với các loại response khác nhau"""
    print("="*50)
    print("TESTING PARSER WITH MOCK RESPONSES")
    print("="*50)
    
    parser = RecipeParser()
    
    # Test case 1: Response có markdown code block (vấn đề hiện tại)
    mock_response_1 = """```json
{
  "title": "Bánh Matcha Nhật Bản",
  "description": "Bánh matcha thơm ngon với hương vị trà xanh đặc trưng",
  "ingredients": [
    {"name": "bột mì", "quantity": "200", "unit": "gram"},
    {"name": "đường", "quantity": "150", "unit": "gram"},
    {"name": "trứng", "quantity": "3", "unit": "quả"},
    {"name": "bơ", "quantity": "100", "unit": "gram"},
    {"name": "bột matcha", "quantity": "2", "unit": "thìa canh"}
  ],
  "instructions": [
    "Bước 1: Trộn bột mì, đường và bột matcha",
    "Bước 2: Đánh trứng tơi và thêm bơ đã tan",
    "Bước 3: Trộn đều hỗn hợp và nướng 25 phút"
  ],
  "prep_time": "20 phút",
  "cook_time": "25 phút", 
  "servings": "8 phần",
  "difficulty": "medium",
  "tags": ["matcha", "bánh ngọt", "nhật bản"]
}
```"""
    
    # Test case 2: Response pure JSON
    mock_response_2 = """{
  "title": "Bánh Valentine Labubu",
  "description": "Bánh đặc biệt cho Gen Z trong dịp Valentine với theme Labubu đáng yêu",
  "ingredients": [
    {"name": "bột mì", "quantity": "250", "unit": "gram"},
    {"name": "đường hồng", "quantity": "120", "unit": "gram"},
    {"name": "trứng", "quantity": "2", "unit": "quả"},
    {"name": "bơ lạt", "quantity": "80", "unit": "gram"},
    {"name": "bột matcha", "quantity": "1", "unit": "thìa canh"},
    {"name": "màu thực phẩm hồng", "quantity": "5", "unit": "giọt"}
  ],
  "instructions": [
    "Bước 1: Chuẩn bị khuôn hình Labubu",
    "Bước 2: Pha bột với màu hồng và matcha",
    "Bước 3: Nướng và trang trí hình Labubu"
  ],
  "prep_time": "30 phút",
  "cook_time": "25 phút",
  "servings": "6 phần", 
  "difficulty": "medium",
  "tags": ["valentine", "labubu", "genz", "matcha"],
  "decoration_tips": "Dùng kem tươi hồng và vẽ mặt Labubu bằng chocolate",
  "marketing_caption": "💕 Bánh Valentine Labubu siêu cute cho couple GenZ! 🧸✨"
}"""
    
    # Test case 3: Response bị broken JSON
    mock_response_3 = """```json
{
  "title": "Bánh Matcha",
  "description": "Bánh thơm ngon
  "ingredients": [
    {"name": "bột mì", "quantity": "200", "unit": "gram"}
  ],
  "instructions": ["Nướng bánh"]
}
```"""
    
    # Test case 4: Response text format
    mock_response_4 = """
TÊN BÁNH: Bánh Matcha Truyền Thống

MÔ TẢ: Bánh matcha với hương vị đặc trưng của trà xanh Nhật Bản

NGUYÊN LIỆU:
- 200g bột mì
- 150g đường 
- 3 quả trứng
- 100g bơ
- 2 thìa canh bột matcha

CÁCH LÀM:
1. Trộn bột mì với bột matcha
2. Đánh trứng với đường cho tơi
3. Thêm bơ đã tan và trộn đều
4. Nướng ở 180°C trong 25 phút

THỜI GIAN: Chuẩn bị 20 phút, nướng 25 phút
"""
    
    test_cases = [
        ("Markdown JSON (current issue)", mock_response_1),
        ("Pure JSON", mock_response_2), 
        ("Broken JSON", mock_response_3),
        ("Text format", mock_response_4)
    ]
    
    for name, response in test_cases:
        print(f"\n{'-'*30}")
        print(f"TEST: {name}")
        print(f"{'-'*30}")
        print(f"Input length: {len(response)}")
        print(f"First 100 chars: {repr(response[:100])}")
        
        try:
            parsed = parser.parse_gemini_output(response)
            print(f"✅ Parsed successfully!")
            print(f"Title: {parsed.get('title', 'N/A')}")
            print(f"Ingredients count: {len(parsed.get('ingredients', []))}")
            print(f"Instructions count: {len(parsed.get('instructions', []))}")
            
            # Show full result
            print(f"\nFull parsed result:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_parser_with_mock_responses()