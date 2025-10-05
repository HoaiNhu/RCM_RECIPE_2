# infrastructure/ai/recipe_parser.py
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

class RecipeParser:
    """Parser để xử lý output từ Gemini và chuẩn hóa thành Recipe object"""
    
    def __init__(self):
        self.unit_mapping = {
            'tsp': 'thìa cà phê',
            'tbsp': 'thìa canh', 
            'cup': 'cốc',
            'g': 'gram',
            'kg': 'kilogram',
            'ml': 'ml',
            'l': 'lít',
            'muỗng': 'thìa',
            'thìa': 'thìa'
        }
    
    def parse_gemini_output(self, raw_output: str) -> Dict[str, Any]:
        """Parse output từ Gemini thành structured data"""
        try:
            # Thử parse JSON trực tiếp
            json_data = self._extract_json(raw_output)
            if json_data:
                return self._normalize_recipe_data(json_data)
        except Exception as e:
            print(f"JSON parsing failed: {e}")
        
        # Fallback: parse text format
        print("Falling back to text parsing...")
        return self._parse_text_format(raw_output)
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON từ text output"""
        # Loại bỏ markdown code blocks cẩn thận
        text = text.strip()
        
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*$', '', text, flags=re.MULTILINE)
        text = text.strip()
        
        # If text starts with {, try to parse directly
        if text.startswith('{'):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        
        # Tìm JSON block trong text
        json_patterns = [
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested JSON
            r'\{.*?\}',  # Simple JSON
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    # Clean up the match
                    clean_match = match.strip()
                    return json.loads(clean_match)
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def _normalize_recipe_data(self, data: Dict) -> Dict[str, Any]:
        """Chuẩn hóa dữ liệu recipe"""
        # Normalize ingredients
        ingredients = []
        if isinstance(data.get('ingredients'), list):
            for item in data['ingredients']:
                if isinstance(item, dict):
                    ingredients.append({
                        'name': item.get('name', '').strip(),
                        'quantity': item.get('quantity', '').strip(),
                        'unit': item.get('unit', '').strip() or None
                    })
                elif isinstance(item, str):
                    # Parse string format
                    parsed = self._parse_ingredient_string(item)
                    ingredients.append(parsed)
        
        # Normalize instructions
        instructions = []
        if isinstance(data.get('instructions'), list):
            instructions = [str(inst).strip() for inst in data['instructions'] if inst]
        
        # Normalize other fields
        return {
            'title': data.get('title', 'Untitled Recipe').strip(),
            'description': data.get('description', '').strip(),
            'ingredients': ingredients,
            'instructions': instructions,
            'prep_time': data.get('prep_time', '30 phút'),
            'cook_time': data.get('cook_time', '25 phút'),
            'servings': data.get('servings', '8 phần'),
            'difficulty': self._normalize_difficulty(data.get('difficulty', 'medium')),
            'tags': data.get('tags', []),
            'decoration_tips': data.get('decoration_tips', ''),
            'marketing_caption': data.get('marketing_caption', ''),
            'notes': data.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'language': 'vi'
        }
    
    def _parse_text_format(self, text: str) -> Dict[str, Any]:
        """Parse text format khi không có JSON"""
        lines = text.split('\n')
        
        # Extract title
        title = self._extract_title(lines)
        
        # Extract description
        description = self._extract_description(lines)
        
        # Extract ingredients
        ingredients = self._extract_ingredients(lines)
        
        # Extract instructions
        instructions = self._extract_instructions(lines)
        
        # Extract timing info
        prep_time, cook_time, servings = self._extract_timing_info(lines)
        
        return {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'servings': servings,
            'difficulty': 'medium',
            'tags': [],
            'decoration_tips': '',
            'marketing_caption': '',
            'notes': '',
            'created_at': datetime.now().isoformat(),
            'language': 'vi'
        }
    
    def _extract_title(self, lines: List[str]) -> str:
        """Extract title từ lines"""
        for line in lines:
            if 'TÊN BÁNH:' in line or 'Tên bánh:' in line:
                return line.split(':', 1)[1].strip()
            if line.strip() and not line.startswith(('1.', '2.', '3.', '-', '*', '**')):
                if len(line.strip()) < 100:  # Likely a title
                    return line.strip()
        return 'Untitled Recipe'
    
    def _extract_description(self, lines: List[str]) -> str:
        """Extract description từ lines"""
        for i, line in enumerate(lines):
            if 'MÔ TẢ:' in line or 'Mô tả:' in line:
                # Get next few lines as description
                desc_lines = []
                for j in range(i+1, min(i+4, len(lines))):
                    if lines[j].strip() and not lines[j].startswith(('1.', '2.', '3.', '-', '*', '**')):
                        desc_lines.append(lines[j].strip())
                return ' '.join(desc_lines)
        return ''
    
    def _extract_ingredients(self, lines: List[str]) -> List[Dict]:
        """Extract ingredients từ lines"""
        ingredients = []
        in_ingredients = False
        
        for line in lines:
            line = line.strip()
            
            if 'NGUYÊN LIỆU:' in line or 'Nguyên liệu:' in line:
                in_ingredients = True
                continue
            
            if in_ingredients:
                if line.startswith(('CÁCH LÀM:', 'Cách làm:', '1.', '2.', '3.')):
                    break
                
                if line.startswith('-') or line.startswith('*'):
                    ingredient_text = line[1:].strip()
                    parsed = self._parse_ingredient_string(ingredient_text)
                    ingredients.append(parsed)
        
        return ingredients
    
    def _extract_instructions(self, lines: List[str]) -> List[str]:
        """Extract instructions từ lines"""
        instructions = []
        in_instructions = False
        
        for line in lines:
            line = line.strip()
            
            if 'CÁCH LÀM:' in line or 'Cách làm:' in line:
                in_instructions = True
                continue
            
            if in_instructions:
                if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                    instructions.append(line)
                elif line and not line.startswith(('-', '*', '**')):
                    instructions.append(line)
        
        return instructions
    
    def _extract_timing_info(self, lines: List[str]) -> tuple:
        """Extract timing info từ lines"""
        prep_time = '30 phút'
        cook_time = '25 phút'
        servings = '8 phần'
        
        for line in lines:
            line = line.strip()
            if 'THỜI GIAN:' in line or 'Thời gian:' in line:
                # Parse timing info
                if 'chuẩn bị' in line.lower():
                    prep_match = re.search(r'(\d+)\s*(phút|giờ)', line)
                    if prep_match:
                        prep_time = f"{prep_match.group(1)} {prep_match.group(2)}"
                
                if 'nướng' in line.lower():
                    cook_match = re.search(r'(\d+)\s*(phút|giờ)', line)
                    if cook_match:
                        cook_time = f"{cook_match.group(1)} {cook_match.group(2)}"
        
        return prep_time, cook_time, servings
    
    def _parse_ingredient_string(self, text: str) -> Dict[str, str]:
        """Parse ingredient string thành structured format"""
        # Pattern để match quantity + unit + name
        patterns = [
            r'^(\d+(?:[.,]\d+)?)\s*([a-zA-Zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)?\s+(.+)$',
            r'^(\d+(?:[.,]\d+)?)\s+(.+)$',
            r'^(.+)$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, text.strip())
            if match:
                if len(match.groups()) == 3:
                    quantity, unit, name = match.groups()
                    return {
                        'name': name.strip(),
                        'quantity': quantity.strip(),
                        'unit': unit.strip() if unit else None
                    }
                elif len(match.groups()) == 2:
                    quantity, name = match.groups()
                    return {
                        'name': name.strip(),
                        'quantity': quantity.strip(),
                        'unit': None
                    }
                else:
                    return {
                        'name': text.strip(),
                        'quantity': '1',
                        'unit': None
                    }
        
        return {
            'name': text.strip(),
            'quantity': '1',
            'unit': None
        }
    
    def _normalize_difficulty(self, difficulty: str) -> str:
        """Normalize difficulty level"""
        if not difficulty:
            return 'medium'
        
        difficulty_lower = difficulty.lower()
        if any(word in difficulty_lower for word in ['easy', 'dễ', 'đơn giản']):
            return 'easy'
        elif any(word in difficulty_lower for word in ['hard', 'khó', 'phức tạp']):
            return 'hard'
        else:
            return 'medium'
