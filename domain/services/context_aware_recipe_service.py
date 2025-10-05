# domain/services/context_aware_recipe_service.py
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
from pathlib import Path

from domain.entities.recipe import Recipe
from domain.entities.ingredient import Ingredient
from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ml_models.trend_predictor import TrendPredictor

@dataclass
class SeasonalContext:
    """Context về mùa vụ và sự kiện"""
    season: str
    month: int
    temperature: float
    events: List[str]
    trending_flavors: List[str]
    popular_occasions: List[str]
    demand_factor: float

@dataclass
class MarketContext:
    """Context về thị trường và khách hàng"""
    target_segment: str
    market_potential: float
    competition_level: float
    growth_trend: str
    preferred_flavors: List[str]
    price_sensitivity: str
    purchase_frequency: str

class ContextAwareRecipeService:
    """
    Service tạo công thức bánh ngọt dựa trên context đầy đủ:
    - Mùa vụ, thời tiết, sự kiện
    - Xu hướng thị trường
    - Phân khúc khách hàng
    - Dự đoán từ ML models
    """
    
    def __init__(self):
        self.gemini = GeminiClient()
        self.trend_predictor = TrendPredictor()
        
        # Load trained model nếu có
        self.trend_predictor.load_models()
        
        # Load context data
        self._load_seasonal_data()
        self._load_market_data()
    
    def _load_seasonal_data(self):
        """Load dữ liệu mùa vụ từ CSV"""
        try:
            import pandas as pd
            
            # Load seasonal trends
            seasonal_df = pd.read_csv("data/raw/seasonal_trends_20250920_061904.csv")
            self.seasonal_data = {}
            
            for _, row in seasonal_df.iterrows():
                self.seasonal_data[row['season']] = {
                    'trending_flavors': eval(row['trending_flavors']) if isinstance(row['trending_flavors'], str) else [],
                    'popular_occasions': eval(row['popular_occasions']) if isinstance(row['popular_occasions'], str) else [],
                    'average_orders': row['average_orders'],
                    'peak_months': row['peak_months']
                }
            
            # Load Vietnam events
            events_df = pd.read_csv("data/raw/vietnam_seasonal_events_2025.csv")
            self.events_data = events_df.to_dict('records')
            
        except Exception as e:
            print(f"Warning: Could not load seasonal data: {e}")
            self.seasonal_data = {}
            self.events_data = []
    
    def _load_market_data(self):
        """Load dữ liệu thị trường từ CSV"""
        try:
            import pandas as pd
            
            # Load consumer groups
            consumer_df = pd.read_csv("data/raw/consumer_groups_detailed_20250921_133329.csv")
            self.market_data = {}
            
            for _, row in consumer_df.iterrows():
                self.market_data[row['consumer_group']] = {
                    'market_potential': row['market_potential'],
                    'competition_level': row['competition_level'],
                    'growth_trend': row['growth_trend'],
                    'avg_engagement_rate': row['avg_engagement_rate'],
                    'top_keywords': row['top_5_keywords'].split(', ') if isinstance(row['top_5_keywords'], str) else []
                }
            
            # Load consumer profiles
            profiles_df = pd.read_csv("data/raw/consumer_profiles_20250920_061904.csv")
            self.profile_data = {}
            
            for _, row in profiles_df.iterrows():
                if pd.notna(row.get('preferred_flavors')):
                    self.profile_data[row.index] = {
                        'age_range': row.get('age_range'),
                        'characteristics': eval(row['characteristics']) if isinstance(row.get('characteristics'), str) else [],
                        'preferred_flavors': eval(row['preferred_flavors']) if isinstance(row.get('preferred_flavors'), str) else [],
                        'price_sensitivity': row.get('price_sensitivity'),
                        'purchase_frequency': row.get('purchase_frequency'),
                        'preferred_channels': eval(row['preferred_channels']) if isinstance(row.get('preferred_channels'), str) else []
                    }
                    
        except Exception as e:
            print(f"Warning: Could not load market data: {e}")
            self.market_data = {}
            self.profile_data = {}
    
    def get_current_context(self, target_date: Optional[datetime] = None) -> Tuple[SeasonalContext, MarketContext]:
        """Lấy context hiện tại dựa trên ngày"""
        
        if target_date is None:
            target_date = datetime.now()
        
        # Seasonal context
        seasonal_ctx = self._get_seasonal_context(target_date)
        
        # Market context (có thể customize theo yêu cầu)
        market_ctx = self._get_market_context("Gen Z")  # Default segment
        
        return seasonal_ctx, market_ctx
    
    def _get_seasonal_context(self, date: datetime) -> SeasonalContext:
        """Tạo seasonal context từ ngày"""
        
        # Determine season
        month = date.month
        season_map = {
            12: 'Đông', 1: 'Đông', 2: 'Đông',
            3: 'Xuân', 4: 'Xuân', 5: 'Xuân',
            6: 'Hè', 7: 'Hè', 8: 'Hè', 
            9: 'Thu', 10: 'Thu', 11: 'Thu'
        }
        
        season = season_map.get(month, 'Xuân')
        
        # Get seasonal data
        season_info = self.seasonal_data.get(season, {})
        
        # Determine events for current month
        current_events = []
        if month == 10:
            current_events = ['Halloween', 'Tháng ma quỷ', 'Thu hoạch']
        elif month == 2:
            current_events = ['Tết Nguyên Đán', 'Valentine', 'Xuân về']
        elif month in [6, 7, 8]:
            current_events = ['Mùa hè', 'Du lịch', 'Nghỉ học']
        elif month == 12:
            current_events = ['Giáng sinh', 'Năm mới', 'Đông']
        
        # Estimate temperature (simplified)
        temp_map = {
            12: 20, 1: 18, 2: 22, 3: 25, 4: 28, 5: 30,
            6: 32, 7: 33, 8: 32, 9: 29, 10: 26, 11: 23
        }
        
        return SeasonalContext(
            season=season,
            month=month,
            temperature=temp_map.get(month, 25),
            events=current_events,
            trending_flavors=season_info.get('trending_flavors', []),
            popular_occasions=season_info.get('popular_occasions', []),
            demand_factor=season_info.get('average_orders', 100) / 100
        )
    
    def _get_market_context(self, segment: str) -> MarketContext:
        """Tạo market context từ segment"""
        
        # Map segment names
        segment_mapping = {
            'genz': 'Gen Z',
            'gen_z': 'Gen Z', 
            'millennials': 'Millennials',
            'gym': 'Người Tập Gym',
            'kids': 'Trẻ Em',
            'health': 'Người Ăn Healthy'
        }
        
        mapped_segment = segment_mapping.get(segment.lower(), segment)
        
        # Get market data
        market_info = self.market_data.get(mapped_segment, {})
        profile_info = self.profile_data.get(mapped_segment.lower(), {})
        
        return MarketContext(
            target_segment=mapped_segment,
            market_potential=0.8 if market_info.get('market_potential') == 'Cao' else 0.5,
            competition_level=0.9 if market_info.get('competition_level') == 'Rất cao' else 0.6,
            growth_trend=market_info.get('growth_trend', 'Tăng'),
            preferred_flavors=profile_info.get('preferred_flavors', []),
            price_sensitivity=profile_info.get('price_sensitivity', 'trung bình'),
            purchase_frequency=profile_info.get('purchase_frequency', 'trung bình')
        )
    
    def generate_context_aware_recipe(self, 
                                    user_segment: str,
                                    target_date: Optional[datetime] = None,
                                    custom_trend: Optional[str] = None) -> Recipe:
        """Tạo công thức dựa trên context đầy đủ"""
        
        # Get contexts
        seasonal_ctx, market_ctx = self.get_current_context(target_date)
        
        # Update market context với segment yêu cầu
        market_ctx = self._get_market_context(user_segment)
        
        # Predict trends using ML model
        ml_context = {
            'month': seasonal_ctx.month,
            'temperature': seasonal_ctx.temperature,
            'user_segment': user_segment,
            'season': seasonal_ctx.season,
            'market_potential': market_ctx.market_potential,
            'competition_level': market_ctx.competition_level,
            'bakery_demand': seasonal_ctx.demand_factor
        }
        
        try:
            trend_predictions = self.trend_predictor.predict_trends(ml_context)
            trend_strength = trend_predictions.get('overall_trend_strength', 0.5)
        except Exception as e:
            print(f"Warning: Could not get ML predictions: {e}")
            trend_strength = 0.5
        
        # Build enhanced prompt
        recipe_data = self._generate_enhanced_recipe(
            seasonal_ctx, market_ctx, custom_trend, trend_strength
        )
        
        return self._parse_recipe_response(recipe_data, seasonal_ctx, market_ctx)
    
    def _generate_enhanced_recipe(self, 
                                seasonal_ctx: SeasonalContext,
                                market_ctx: MarketContext,
                                custom_trend: Optional[str],
                                trend_strength: float) -> str:
        """Tạo công thức với Gemini sử dụng context đầy đủ"""
        
        # Build comprehensive prompt
        prompt = f"""
Bạn là một đầu bếp bánh ngọt chuyên nghiệp và chuyên gia phân tích thị trường với 15+ năm kinh nghiệm.

🎯 NHIỆM VỤ: Tạo công thức bánh ngọt THÔNG MINH dựa trên phân tích thị trường đầy đủ

📊 PHÂN TÍCH THỊ TRƯỜNG HIỆN TẠI:
• Mùa: {seasonal_ctx.season} (tháng {seasonal_ctx.month})
• Nhiệt độ: {seasonal_ctx.temperature}°C
• Sự kiện đặc biệt: {', '.join(seasonal_ctx.events)}
• Xu hướng mùa vụ: {', '.join(seasonal_ctx.trending_flavors)}
• Dịp phổ biến: {', '.join(seasonal_ctx.popular_occasions)}
• Hệ số nhu cầu: {seasonal_ctx.demand_factor:.1f}

👥 PHÂN KHÚC KHÁCH HÀNG:
• Đối tượng: {market_ctx.target_segment}
• Tiềm năng thị trường: {market_ctx.market_potential:.1f}/1.0
• Mức độ cạnh tranh: {market_ctx.competition_level:.1f}/1.0  
• Xu hướng tăng trưởng: {market_ctx.growth_trend}
• Hương vị ưa thích: {', '.join(market_ctx.preferred_flavors) if market_ctx.preferred_flavors else 'đa dạng'}
• Độ nhạy cảm giá: {market_ctx.price_sensitivity}
• Tần suất mua: {market_ctx.purchase_frequency}

🔮 DỰ ĐOÁN XU HƯỚNG: 
• Điểm xu hướng AI: {trend_strength:.2f}/1.0
• Trend tùy chỉnh: {custom_trend or 'Không có'}

🎨 YÊU CẦU SÁNG TẠO:
1. Kết hợp HOÀN HẢO các yếu tố mùa vụ và sự kiện
2. Phù hợp CHÍNH XÁC với sở thích của {market_ctx.target_segment}
3. Tận dụng xu hướng flavor hot nhất: {', '.join(seasonal_ctx.trending_flavors)}
4. Thiết kế phù hợp với dịp: {', '.join(seasonal_ctx.popular_occasions)}
5. Tối ưu cho mức giá {market_ctx.price_sensitivity}

OUTPUT JSON format (tiếng Việt):
{{
  "title": "Tên bánh SÁNG TẠO kết hợp trend + mùa vụ + segment",
  "description": "Mô tả chi tiết 4-5 câu, nhấn mạnh WHY phù hợp với thời điểm và đối tượng này",
  "ingredients": [
    {{"name": "nguyên liệu chính", "quantity": "số lượng chính xác", "unit": "đơn vị"}},
    {{"name": "nguyên liệu phụ", "quantity": "số lượng", "unit": "đơn vị"}}
  ],
  "instructions": [
    "Bước 1: Hướng dẫn chi tiết với lý do kỹ thuật",
    "Bước 2: Hướng dẫn chi tiết với tips thành công"
  ],
  "prep_time": "thời gian chuẩn bị thực tế",
  "cook_time": "thời gian nướng + nhiệt độ cụ thể",
  "servings": "số phần ăn",
  "difficulty": "easy/medium/hard",
  "seasonal_relevance": "Tại sao phù hợp với {seasonal_ctx.season} và {', '.join(seasonal_ctx.events)}",
  "target_appeal": "Tại sao {market_ctx.target_segment} sẽ thích món này",
  "market_positioning": "Chiến lược bán hàng và định vị giá",
  "decoration_tips": "Hướng dẫn trang trí theo theme {seasonal_ctx.season} + trend",
  "marketing_caption": "Caption Facebook viral tận dụng sự kiện {', '.join(seasonal_ctx.events)} + hashtag",
  "profit_optimization": "Cách tối ưu lợi nhuận với segment {market_ctx.target_segment}",
  "viral_potential": "Yếu tố nào làm món này viral trong mùa {seasonal_ctx.season}",
  "notes": "Lưu ý quan trọng về mùa vụ, bảo quản, và biến thể"
}}

Hãy tạo công thức ĐỈNH CAO kết hợp data science + culinary art!
"""
        
        try:
            response = self.gemini.generate_creative_recipe(
                trend=custom_trend or f"{seasonal_ctx.season} {', '.join(seasonal_ctx.events)}",
                user_segment=market_ctx.target_segment,
                occasion=', '.join(seasonal_ctx.popular_occasions),
                language='vi'
            )
            return response
            
        except Exception as e:
            print(f"Error generating recipe: {e}")
            return self._generate_fallback_recipe(seasonal_ctx, market_ctx)
    
    def _generate_fallback_recipe(self, seasonal_ctx: SeasonalContext, market_ctx: MarketContext) -> str:
        """Fallback recipe nếu Gemini fail"""
        
        fallback_recipe = {
            "title": f"Bánh {seasonal_ctx.season} Đặc Biệt cho {market_ctx.target_segment}",
            "description": f"Món bánh được thiết kế đặc biệt cho mùa {seasonal_ctx.season} với hương vị phù hợp với {market_ctx.target_segment}.",
            "ingredients": [
                {"name": "bột mì", "quantity": "250", "unit": "g"},
                {"name": "đường", "quantity": "150", "unit": "g"},
                {"name": "trứng", "quantity": "3", "unit": "quả"},
                {"name": "bơ", "quantity": "100", "unit": "g"}
            ],
            "instructions": [
                "Trộn đều các nguyên liệu khô",
                "Đánh bông bơ với đường", 
                "Cho trứng từng quả một",
                "Trộn nhẹ nhàng bột vào",
                "Nướng ở 175°C trong 25-30 phút"
            ],
            "prep_time": "30 phút",
            "cook_time": "30 phút ở 175°C",
            "servings": "8 phần",
            "difficulty": "medium",
            "seasonal_relevance": f"Phù hợp với mùa {seasonal_ctx.season}",
            "target_appeal": f"Thiết kế cho {market_ctx.target_segment}",
            "market_positioning": "Giá cả phải chăng, chất lượng cao",
            "decoration_tips": "Trang trí theo màu sắc mùa vụ",
            "marketing_caption": f"🎂 Bánh {seasonal_ctx.season} đặc biệt! #BanhNgot #{seasonal_ctx.season}",
            "notes": "Bảo quản nơi khô ráo, thoáng mát"
        }
        
        return json.dumps(fallback_recipe, ensure_ascii=False, indent=2)
    
    def _parse_recipe_response(self, response: str, seasonal_ctx: SeasonalContext, market_ctx: MarketContext) -> Recipe:
        """Parse response thành Recipe object với context metadata"""
        
        try:
            # Parse JSON response
            data = json.loads(response)
        except:
            # Fallback parsing
            data = {
                "title": "Generated Recipe",
                "description": "A contextually generated recipe",
                "ingredients": [],
                "instructions": [],
                "prep_time": "30 phút",
                "cook_time": "30 phút", 
                "servings": "8 phần",
                "difficulty": "medium"
            }
        
        # Convert ingredients
        ingredients = []
        for ing_data in data.get('ingredients', []):
            ingredients.append(Ingredient(
                name=ing_data.get('name', ''),
                quantity=ing_data.get('quantity', '1'),
                unit=ing_data.get('unit'),
                category=self._categorize_ingredient(ing_data.get('name', ''))
            ))
        
        # Create recipe với extended metadata
        recipe = Recipe(
            title=data.get('title', 'Context-Aware Recipe'),
            description=data.get('description', ''),
            ingredients=ingredients,
            instructions=data.get('instructions', []),
            prep_time=data.get('prep_time', '30 phút'),
            cook_time=data.get('cook_time', '30 phút'),
            servings=data.get('servings', '8 phần'),
            difficulty=data.get('difficulty', 'medium'),
            tags=[
                seasonal_ctx.season,
                market_ctx.target_segment,
                f"month_{seasonal_ctx.month}",
                f"temp_{int(seasonal_ctx.temperature)}C"
            ] + seasonal_ctx.events,
            language='vi',
            trend_context=f"Generated for {seasonal_ctx.season} season targeting {market_ctx.target_segment}",
            user_segment=market_ctx.target_segment
        )
        
        # Add extended metadata nếu có
        if hasattr(recipe, 'metadata'):
            recipe.metadata.update({
                'seasonal_relevance': data.get('seasonal_relevance', ''),
                'target_appeal': data.get('target_appeal', ''),
                'market_positioning': data.get('market_positioning', ''),
                'decoration_tips': data.get('decoration_tips', ''),
                'marketing_caption': data.get('marketing_caption', ''),
                'profit_optimization': data.get('profit_optimization', ''),
                'viral_potential': data.get('viral_potential', ''),
                'seasonal_context': seasonal_ctx.__dict__,
                'market_context': market_ctx.__dict__
            })
        
        return recipe
    
    def _categorize_ingredient(self, ingredient_name: str) -> str:
        """Categorize ingredient"""
        ingredient_lower = ingredient_name.lower()
        
        seasonal_categories = {
            'xuân': ['strawberry', 'dâu', 'sakura', 'hoa anh đào', 'green tea', 'trà xanh'],
            'hè': ['mango', 'xoài', 'coconut', 'dừa', 'lemon', 'chanh', 'passion fruit'],
            'thu': ['pumpkin', 'bí đỏ', 'cinnamon', 'quế', 'apple', 'táo', 'caramel'],
            'đông': ['chocolate', 'socola', 'gingerbread', 'bánh gừng', 'peppermint', 'orange', 'cam']
        }
        
        for season, items in seasonal_categories.items():
            if any(item in ingredient_lower for item in items):
                return f'seasonal_{season}'
        
        # Standard categories
        if any(word in ingredient_lower for word in ['flour', 'bột', 'sugar', 'đường']):
            return 'base_ingredients'
        elif any(word in ingredient_lower for word in ['fruit', 'trái cây', 'berry']):
            return 'fruits'
        elif any(word in ingredient_lower for word in ['chocolate', 'cream', 'kem']):
            return 'luxury_ingredients'
        else:
            return 'other'

if __name__ == "__main__":
    # Test the service
    service = ContextAwareRecipeService()
    
    # Test with Halloween context
    halloween_date = datetime(2025, 10, 31)
    recipe = service.generate_context_aware_recipe(
        user_segment="gen_z",
        target_date=halloween_date,
        custom_trend="halloween labubu spooky"
    )
    
    print(f"Generated recipe: {recipe.title}")
    print(f"Description: {recipe.description}")
    print(f"Tags: {recipe.tags}")