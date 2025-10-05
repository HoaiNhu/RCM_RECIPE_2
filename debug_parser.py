# debug_parser.py
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

from infrastructure.ai.recipe_parser import RecipeParser

def test_parser():
    parser = RecipeParser()
    
    # Test với output giả lập từ Gemini
    test_output = '''```json
{
  "title": "Bánh Labubu Valentine Matcha",
  "description": "Bánh bông lan mềm mịn với hương vị matcha thơm ngon",
  "ingredients": [
    {"name": "bột mì", "quantity": "200", "unit": "g"},
    {"name": "đường", "quantity": "100", "unit": "g"},
    {"name": "trứng", "quantity": "3", "unit": "quả"}
  ],
  "instructions": [
    "Bước 1: Trộn bột mì với đường",
    "Bước 2: Thêm trứng vào và khuấy đều"
  ],
  "prep_time": "20 phút",
  "cook_time": "30 phút",
  "servings": "8 phần",
  "difficulty": "easy"
}
```'''
    
    result = parser.parse_gemini_output(test_output)
    print("Parsed result:")
    print(f"Title: {result.get('title')}")
    print(f"Description: {result.get('description')}")
    print(f"Ingredients: {len(result.get('ingredients', []))} items")
    print(f"Instructions: {len(result.get('instructions', []))} steps")

if __name__ == "__main__":
    test_parser()
