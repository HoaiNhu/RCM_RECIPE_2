# test_gemini_fixed.py
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

def test_gemini_direct():
    print("Testing Gemini directly...")
    try:
        import google.generativeai as genai
        from configs.settings import settings
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = """
Bạn là một đầu bếp bánh ngọt chuyên nghiệp.

NHIỆM VỤ: Tạo công thức bánh ngọt phù hợp với:
- Xu hướng: labubu valentine matcha
- Đối tượng: genz
- Dịp: valentine

YÊU CẦU OUTPUT theo format JSON:
{
  "title": "Tên bánh sáng tạo",
  "description": "Mô tả 2-3 câu về món bánh",
  "ingredients": [
    {"name": "tên nguyên liệu", "quantity": "số lượng", "unit": "đơn vị"}
  ],
  "instructions": [
    "Bước 1: Hướng dẫn chi tiết",
    "Bước 2: Hướng dẫn chi tiết"
  ],
  "prep_time": "thời gian chuẩn bị",
  "cook_time": "thời gian nướng",
  "servings": "số phần ăn",
  "difficulty": "easy/medium/hard"
}

Chỉ trả về JSON, không thêm text khác.
"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2048
            },
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        print(f"Response candidates: {len(response.candidates) if response.candidates else 0}")
        if response.candidates:
            candidate = response.candidates[0]
            print(f"Finish reason: {candidate.finish_reason}")
            if candidate.finish_reason == 1:  # STOP
                try:
                    print(f"Response text: {response.text[:200]}...")
                except UnicodeEncodeError:
                    print("Response text: [Contains Unicode characters]")
            elif candidate.finish_reason == 2:  # MAX_TOKENS
                print("Response truncated due to max tokens")
                try:
                    print(f"Partial response: {response.text[:200]}...")
                except UnicodeEncodeError:
                    print("Partial response: [Contains Unicode characters]")
            else:
                print(f"Other finish reason: {candidate.finish_reason}")
        else:
            print("No candidates in response")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini_direct()
