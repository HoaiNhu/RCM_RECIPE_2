# 🍰 HỆ THỐNG AI-POWERED RECIPE GENERATION

## 📋 Tổng quan

Hệ thống AI hoàn chỉnh để tạo công thức bánh ngọt dựa trên xu hướng social media, sử dụng **Gemini AI** + **T5 Model** + **Multiple APIs** với kiến trúc Clean Architecture.

### 🎯 Pipeline chính:

```
Data Collection → Gemini Analysis → Ingredient Selection → T5 Recipe Generation → Gemini Translation
```

## 🚀 Cài đặt nhanh

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình API keys

```python
# Trong configs/settings.py hoặc environment variables
GEMINI_API_KEY = "your_gemini_api_key"
NEWS_API_KEY = "your_news_api_key"  # Optional
YOUTUBE_API_KEY = "your_youtube_api_key"  # Optional
```

### 3. Chạy example

```bash
python example_usage.py
```

### 4. Chạy API server

```bash
python main.py
```

## 🔧 Cấu trúc dự án (Clean Architecture)

```
RCM_RECIPE/
├── 📁 domain/                    # Business logic
│   ├── entities/                 # Domain entities
│   │   └── recipe.py            # Recipe, TrendAnalysis entities
│   └── services/                # Domain services
│       ├── trend_analyzer.py    # Trend analysis logic
│       └── recipe_generator.py  # Recipe generation logic
├── 📁 application/               # Application layer
│   └── use_cases/               # Use cases
│       └── recipe_generation_use_case.py
├── 📁 infrastructure/           # External services
│   └── external/               # External APIs
│       ├── gemini_client.py    # Gemini AI client
│       ├── t5_client.py        # T5 model client
│       └── trend_data_client.py # Trend data collection
├── 📁 app/                     # API layer
│   └── routers/               # API routers
│       └── recipe_router.py   # Recipe API endpoints
├── 📁 configs/                # Configuration
│   └── settings.py           # Application settings
├── 📁 data/                   # Data storage
│   ├── raw/                  # Raw data
│   └── processed/            # Processed data
├── main.py                   # FastAPI application
├── example_usage.py          # Usage examples
└── requirements.txt          # Dependencies
```

## 🎯 Tính năng chính

### 1. **Trend Analysis với Gemini**

- Phân tích xu hướng từ Google Trends, News, Social Media
- Đưa ra insights về trend strength và duration
- Gợi ý nguyên liệu phù hợp với trend

### 2. **Smart Ingredient Selection**

- Chọn nguyên liệu dựa trên trend analysis
- Personalization theo user segment (Gen Z, Millennials, Health-conscious, etc.)
- Tối ưu hóa dựa trên available ingredients

### 3. **T5 Recipe Generation**

- Sử dụng model `flax-community/t5-recipe-generation`
- Tạo công thức chi tiết với instructions
- Format chuẩn: ingredients, instructions, timing, difficulty

### 4. **Multi-language Translation**

- Dịch công thức sang ngôn ngữ tùy ý với Gemini
- Hỗ trợ 10+ ngôn ngữ: Vietnamese, English, Korean, Japanese, etc.
- Giữ nguyên format và structure

## 📊 User Segments

| Segment              | Age   | Preferences                           | Ingredients                    | Style                    |
| -------------------- | ----- | ------------------------------------- | ------------------------------ | ------------------------ |
| **Gen Z**            | 10-25 | Viral trends, aesthetic, social media | Matcha, taro, brown sugar      | Korean style, minimalist |
| **Millennials**      | 26-40 | Quality, health-conscious, artisan    | Dark chocolate, salted caramel | Artisan, premium         |
| **Health-conscious** | All   | Low sugar, gluten-free, vegan         | Almond flour, coconut sugar    | Clean, natural           |
| **Kids**             | 3-12  | Colorful, fun, sweet                  | Colorful, fun ingredients      | Colorful, character      |
| **Elderly**          | 65+   | Traditional, less sweet, nutritious   | Traditional, soft              | Classic, simple          |

## 🎯 Trend Categories

### 1. **K-pop Trends**

- Keywords: newjeans, ive, aespa, le sserafim, itzy
- Style: Korean aesthetic, minimalist, Instagram-worthy
- Ingredients: Matcha, taro, brown sugar, cheese foam

### 2. **Character Trends**

- Keywords: labubu, baby three, sanrio, hello kitty
- Style: Cute, kawaii, pastel colors
- Ingredients: Colorful, fun, character-themed

### 3. **Food Trends**

- Keywords: matcha, taro, brown sugar, bubble tea
- Style: Asian-inspired, modern fusion
- Ingredients: Traditional Asian flavors

### 4. **Seasonal Trends**

- Keywords: valentine, tet, christmas, halloween
- Style: Seasonal colors and themes
- Ingredients: Seasonal fruits and flavors

## 💻 Usage Examples

### Basic Usage

```python
from application.use_cases.recipe_generation_use_case import RecipeGenerationUseCase
from domain.entities.recipe import UserSegment

# Initialize use case
use_case = RecipeGenerationUseCase(
    gemini_api_key="your_gemini_api_key",
    news_api_key="your_news_api_key",  # Optional
    youtube_api_key="your_youtube_api_key"  # Optional
)

# Input
trend_keywords = ['labubu', 'valentine', 'matcha']
user_segment = UserSegment.GEN_Z
available_ingredients = ['flour', 'sugar', 'eggs', 'butter', 'matcha_powder']

# Generate recipe
result = await use_case.generate_trend_recipe(
    trend_keywords=trend_keywords,
    user_segment=user_segment,
    available_ingredients=available_ingredients,
    target_language='Vietnamese'
)

print(f"Recipe: {result['final_output']['recipe_title']}")
print(f"Ingredients: {result['final_output']['ingredients']}")
```

### API Usage

```bash
# Start API server
python main.py

# Generate recipe via API
curl -X POST "http://localhost:8000/api/recipes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "trend_keywords": ["labubu", "valentine", "matcha"],
    "user_segment": "gen_z",
    "available_ingredients": ["flour", "sugar", "eggs", "butter", "matcha_powder"],
    "target_language": "Vietnamese"
  }'
```

### Batch Generation

```python
# Multiple scenarios
scenarios = [
    {
        'trend_keywords': ['newjeans', 'korean_style'],
        'user_segment': UserSegment.GEN_Z,
        'available_ingredients': ['flour', 'sugar', 'matcha_powder'],
        'target_language': 'Korean'
    },
    {
        'trend_keywords': ['keto', 'vegan'],
        'user_segment': UserSegment.HEALTH_CONSCIOUS,
        'available_ingredients': ['almond_flour', 'coconut_sugar'],
        'target_language': 'English'
    }
]

results = await use_case.batch_generate_recipes(scenarios)
```

## 🔄 Pipeline Chi tiết

### Step 1: Data Collection

```python
# Collect trend data từ multiple sources
trend_data = await trend_data_client.collect_trend_data(['labubu', 'valentine'])
```

### Step 2: Gemini Analysis

```python
# Analyze trends với Gemini AI
analysis = await trend_analyzer_service.analyze_trends_for_recipe(keywords, user_segment)
```

### Step 3: Ingredient Selection

```python
# Smart ingredient selection
ingredients = recipe_generator_service.select_ingredients_smart(
    analysis.recommended_ingredients, available_ingredients, user_segment
)
```

### Step 4: T5 Recipe Generation

```python
# Generate recipe với T5 model
recipe = await t5_client.generate_recipe(ingredients, trend_context, preferences)
```

### Step 5: Translation

```python
# Translate với Gemini
translated_recipe = await gemini_client.translate_recipe(recipe_text, 'Vietnamese')
```

## 📈 Output Format

```json
{
  "final_output": {
    "recipe_title": "Labubu Valentine Matcha Cake",
    "ingredients": [
      "2 cups flour",
      "1 cup sugar",
      "3 eggs",
      "1/2 cup butter",
      "2 tbsp matcha powder"
    ],
    "instructions": [
      "1. Mix dry ingredients",
      "2. Beat eggs and butter",
      "3. Combine and bake at 350°F for 25 minutes"
    ],
    "prep_time": "30 minutes",
    "cook_time": "25 minutes",
    "servings": "8 servings",
    "difficulty": "Medium",
    "trend_context": "Labubu character trend with Valentine theme",
    "marketing_insights": "Perfect for Gen Z social media posts"
  }
}
```

## 🛠️ Configuration

### API Keys

```python
# Required
GEMINI_API_KEY = "your_gemini_api_key"

# Optional (for enhanced features)
NEWS_API_KEY = "your_news_api_key"
YOUTUBE_API_KEY = "your_youtube_api_key"
```

### Model Settings

```python
# T5 Model
T5_MODEL_NAME = "flax-community/t5-recipe-generation"

# Gemini Model
GEMINI_MODEL_NAME = "gemini-pro"

# Performance
MAX_INGREDIENTS = 8
RECIPE_MAX_LENGTH = 1024
```

## 🚨 Troubleshooting

### Common Issues

1. **Gemini API Error**

   ```
   ❌ API key not configured
   ✅ Solution: Set GEMINI_API_KEY in configs/settings.py
   ```

2. **T5 Model Loading Error**

   ```
   ❌ Model download failed
   ✅ Solution: Check internet connection, retry
   ```

3. **Trend Data Collection Error**
   ```
   ❌ Google Trends rate limit
   ✅ Solution: Increase delay between requests
   ```

### Performance Optimization

1. **GPU Usage**

   ```python
   # Enable GPU for T5 model
   device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   ```

2. **Caching**

   ```python
   # Cache trend data to avoid repeated API calls
   cache_trend_data = True
   ```

3. **Batch Processing**
   ```python
   # Process multiple scenarios in batch
   results = await batch_generate_recipes(scenarios)
   ```

## 📊 Monitoring & Analytics

### Quality Metrics

- Recipe completeness score
- Ingredient match rate
- Trend relevance score
- User satisfaction rating

### Performance Metrics

- Generation time
- API response time
- Model accuracy
- Translation quality

## 🔮 Future Enhancements

1. **Visual Generation**

   - DALL-E integration cho recipe images
   - Midjourney API cho design suggestions

2. **Advanced Personalization**

   - User preference learning
   - Dietary restrictions handling
   - Allergy-aware ingredient selection

3. **Real-time Updates**

   - Live trend monitoring
   - Automatic recipe updates
   - Social media integration

4. **Business Intelligence**
   - Market trend analysis
   - Competitor monitoring
   - Sales prediction

## 📞 Support

Nếu gặp vấn đề:

1. ✅ Kiểm tra API keys
2. ✅ Cài đặt đủ dependencies
3. ✅ Internet connection ổn định
4. ✅ Đủ memory cho T5 model

## 🎉 Kết quả mong đợi

Sau khi chạy thành công, bạn sẽ có:

- 📊 **Trend Analysis**: Insights về xu hướng hot nhất
- 🥘 **Smart Recipes**: Công thức phù hợp với trend và user segment
- 🌐 **Multi-language**: Công thức được dịch sang ngôn ngữ mong muốn
- 💡 **Marketing Insights**: Gợi ý quảng bá và target audience
- 📈 **Business Value**: Tối ưu hóa menu và pricing strategy

---

**Chúc bạn tạo ra những công thức bánh ngọt tuyệt vời! 🍰✨**
