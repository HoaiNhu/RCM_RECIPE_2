# infrastructure/external/t5_client.py
from typing import Optional
from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch


class T5Client:
    """Client cho model T5 sinh công thức từ nguyên liệu.

    Mặc định dùng PyTorch để tương thích môi trường server. Tự động chọn GPU nếu có.
    Tải model/tokenizer 1 lần và cache trong class-level để tránh load lại nhiều lần.
    """

    _tokenizer = None
    _model = None

    def __init__(self, model_name: str = "flax-community/t5-recipe-generation",
                 max_length: int = 300, num_beams: int = 4):
        self.model_name = model_name
        self.max_length = max_length
        self.num_beams = num_beams
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Lazy-load
        if T5Client._tokenizer is None or T5Client._model is None:
            T5Client._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            T5Client._model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            T5Client._model.to(self.device)

        self.tokenizer = T5Client._tokenizer
        self.model = T5Client._model

    def generate_recipe(self, ingredients: str) -> str:
        """Sinh công thức từ chuỗi nguyên liệu, phân tách bằng dấu phẩy.

        Ví dụ: "flour, sugar, eggs, butter, matcha powder"
        """
        input_text = f"generate recipe: {ingredients}"
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True).to(self.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs.get("attention_mask"),
                max_length=self.max_length,
                num_beams=self.num_beams,
                early_stopping=True
            )

        decoded = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return decoded
