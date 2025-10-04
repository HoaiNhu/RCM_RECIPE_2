# infrastructure/ai/translator_service.py
from typing import Literal
from configs.settings import settings

try:
    import google.generativeai as genai  # optional
    _HAS_GEMINI = True
except Exception:
    _HAS_GEMINI = False

class TranslatorService:
    def __init__(self):
        self._enabled = _HAS_GEMINI and bool(getattr(settings, "GEMINI_API_KEY", None))
        if self._enabled:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # dùng model nhẹ cho dịch
            self._model = settings.DEFAULT_GEMINI_MODEL
        else:
            self._model = None
    
    def translate(self, text: str, src: Literal['vi','en'] = 'vi', dest: Literal['vi','en'] = 'en') -> str:
        """Translate text giữa vi <-> en. Nếu không có Gemini, trả về nguyên văn."""
        if not text:
            return text
        if not self._enabled or src == dest:
            return text
        try:
            model = genai.GenerativeModel(self._model)
            prompt = f"Dịch chính xác và tự nhiên từ {self._lang_name(src)} sang {self._lang_name(dest)}:\n\n{text}\n\nChỉ trả về bản dịch, không thêm giải thích."
            resp = model.generate_content(prompt, generation_config={
                "temperature": 0.2,
                "max_output_tokens": min(len(text) * 2, settings.MAX_OUTPUT_TOKENS)
            })
            return (resp.text or text).strip()
        except Exception:
            return text
    
    def vi_to_en(self, text: str) -> str:
        return self.translate(text, src='vi', dest='en')
    
    def en_to_vi(self, text: str) -> str:
        return self.translate(text, src='en', dest='vi')
    
    def _lang_name(self, code: str) -> str:
        return "tiếng Việt" if code == 'vi' else "tiếng Anh'" if code == 'en' else code