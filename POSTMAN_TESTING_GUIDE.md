# 🧪 RCM_RECIPE_2 Analytics API Testing Guide

## 📋 **Files Created**

1. **`postman_analytics_collection.json`** - Postman collection với 11 test cases
2. **`postman_analytics_environment.json`** - Environment variables
3. **`postman_api_tester.py`** - Automated test runner

## 🚀 **Cách Sử Dụng**

### **Option 1: Sử dụng Postman GUI**

1. **Import Collection:**

   ```
   File > Import > postman_analytics_collection.json
   ```

2. **Import Environment:**

   ```
   File > Import > postman_analytics_environment.json
   ```

3. **Set Environment:**

   - Click dropdown góc phải trên
   - Chọn "RCM_RECIPE_2 Analytics Environment"

4. **Run Collection:**
   - Click "Run Collection"
   - Select all requests
   - Click "Run RCM_RECIPE_2 Analytics API"

### **Option 2: Automated Testing Script**

```bash
# Start server trước
python run_server.py

# Trong terminal khác, chạy test
python postman_api_tester.py
```

## 📊 **Test Cases Included**

### **🏥 Health Checks**

- ✅ Health Check (`GET /health`)
- ✅ API Root Info (`GET /`)

### **📈 Analytics Endpoints**

- ✅ Halloween Trend Prediction
- ✅ Christmas Trend Prediction
- ✅ Smart Halloween Recipe Generation
- ✅ Valentine Recipe Generation
- ✅ Market Insights - Gym Segment
- ✅ Current Trending Analysis
- ✅ Kids Segment Recommendations
- ✅ Gen Z Segment Recommendations

### **🍰 Existing Recipe APIs**

- ✅ Recipe from Ingredients
- ✅ Recipe from Trend

## 🎯 **Key Test Scenarios**

### **1. Halloween Gen Z Scenario**

```json
{
  "target_date": "2025-10-31",
  "user_segment": "gen_z",
  "trend_keywords": ["halloween", "pumpkin", "spooky"],
  "include_market_analysis": true
}
```

### **2. Valentine Young Adults Scenario**

```json
{
  "target_date": "2025-02-14",
  "user_segment": "young_adults",
  "trend_keywords": ["valentine", "romantic", "heart"],
  "preferred_ingredients": ["strawberry", "chocolate"]
}
```

### **3. Market Analysis Scenarios**

- Gym segment analysis
- Health conscious analysis
- Kids product recommendations

## ✅ **Expected Responses**

### **Trend Prediction Response:**

```json
{
  "success": true,
  "predictions": {
    "overall_trend_strength": 0.75,
    "popularity_score": 0.8,
    "engagement_score": 0.7
  },
  "recommended_ingredients": ["pumpkin", "cinnamon", "chocolate"],
  "market_insights": {...}
}
```

### **Smart Recipe Response:**

```json
{
  "success": true,
  "recipe": {
    "title": "Bánh Pumpkin Spice Halloween Gen Z",
    "ingredients": [...],
    "instructions": [...]
  },
  "viral_potential_score": 0.85,
  "market_opportunity": 0.7
}
```

## 🔧 **Environment Variables**

- `base_url`: http://localhost:8000
- `halloween_date`: 2025-10-31
- `christmas_date`: 2025-12-25
- `valentine_date`: 2025-02-14
- `tet_date`: 2025-01-29

## 📝 **Test Validation Criteria**

### **✅ Success Criteria:**

- Status code: 200
- Response time: < 5 seconds
- Valid JSON response
- Required fields present
- Logical data values

### **📊 Performance Benchmarks:**

- Health check: < 100ms
- Simple analytics: < 2 seconds
- Recipe generation: < 10 seconds
- Market analysis: < 3 seconds

## 🐛 **Common Issues & Solutions**

### **Issue 1: Server not running**

```bash
# Solution
python run_server.py
```

### **Issue 2: Models not trained**

```bash
# Solution
python train_models.py
```

### **Issue 3: Timeout errors**

- Increase timeout in environment (30000ms)
- Check server logs for errors

### **Issue 4: Data encoding errors**

- Check ML model preprocessing
- Ensure proper categorical encoding

## 📈 **Performance Monitoring**

The automated tester tracks:

- ✅ Response times
- ✅ Success rates
- ✅ Error patterns
- ✅ Data quality

Results saved to `test_results.json` for analysis.

## 🎉 **Quick Start Commands**

```bash
# 1. Start server
python run_server.py

# 2. Run automated tests (new terminal)
python postman_api_tester.py

# 3. Check results
cat test_results.json
```

---

**🔥 Ready to test your AI Analytics API!**

## 📋 Quick Setup

### 1. Import Collection & Environment

1. Mở Postman
2. Import `postman_collection.json`
3. Import `postman_environment.json`
4. Chọn environment "RCM Recipe - Local Development"

### 2. Start Server

```bash
# Đảm bảo server đang chạy
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 Test Scenarios

### 1. **Health Checks** (Kiểm tra server)

- `GET /health` - Root health check
- `GET /api/v1/recipes/health` - Recipes service health
- `GET /api/v1/trends/health` - Trends service health

### 2. **Recipe Generation từ Nguyên Liệu**

#### Test Case 1: Vietnamese Matcha Recipe

```json
POST /api/v1/recipes/generate-from-ingredients
{
  "ingredients": "bột mì, đường, trứng, bơ, bột matcha, strawberry, cream cheese",
  "language": "vi"
}
```

#### Test Case 2: English Chocolate Recipe

```json
POST /api/v1/recipes/generate-from-ingredients
{
  "ingredients": "flour, sugar, eggs, butter, chocolate chips, vanilla extract",
  "language": "en"
}
```

### 3. **Recipe Generation từ Trend**

#### Test Case 1: Labubu Valentine (Gen Z)

```json
POST /api/v1/recipes/generate-from-trend
{
  "trend": "labubu valentine matcha",
  "user_segment": "genz",
  "occasion": "valentine",
  "language": "vi"
}
```

#### Test Case 2: Korean NewJeans Style (Gen Z)

```json
POST /api/v1/recipes/generate-from-trend
{
  "trend": "newjeans korean aesthetic minimalist",
  "user_segment": "genz",
  "occasion": "daily",
  "language": "vi"
}
```

#### Test Case 3: Healthy Gym Recipe

```json
POST /api/v1/recipes/generate-from-trend
{
  "trend": "keto vegan protein healthy",
  "user_segment": "gym",
  "occasion": "post-workout",
  "language": "vi"
}
```

#### Test Case 4: Kids Birthday Recipe

```json
POST /api/v1/recipes/generate-from-trend
{
  "trend": "colorful rainbow unicorn fun",
  "user_segment": "kids",
  "occasion": "birthday",
  "language": "vi"
}
```

### 4. **Support APIs**

- `GET /api/v1/trends/current` - Lấy trends hiện tại
- `GET /api/v1/segments/` - Lấy danh sách user segments

## 📊 Expected Response Format

### Recipe Generation Response:

```json
{
  "status": "success",
  "data": {
    "title": "Tên công thức bánh",
    "description": "Mô tả ngắn",
    "ingredients": [
      {
        "name": "Tên nguyên liệu",
        "quantity": "2",
        "unit": "cups"
      }
    ],
    "instructions": ["Bước 1: ...", "Bước 2: ..."],
    "prep_time": "30 phút",
    "cook_time": "25 phút",
    "servings": "8 phần",
    "difficulty": "medium",
    "language": "vi"
  }
}
```

## 🔧 User Segments Available

| Code          | Name                     | Description                               |
| ------------- | ------------------------ | ----------------------------------------- |
| `genz`        | Gen Z (10-25 tuổi)       | Thích trend viral, màu pastel, aesthetic  |
| `millennials` | Millennials (26-40 tuổi) | Ưa chuộng chất lượng, artisan, organic    |
| `gym`         | Dân Gym                  | Ít đường, nhiều protein, healthy          |
| `kids`        | Trẻ em (3-12 tuổi)       | Màu sắc, hình thù ngộ nghĩnh, vị ngọt vừa |

## 🌟 Trending Keywords Examples

### K-pop Trends:

- `newjeans`, `aespa`, `ive`, `le sserafim`, `itzy`
- `korean`, `aesthetic`, `minimalist`, `pastel`

### Character Trends:

- `labubu`, `baby three`, `sanrio`, `hello kitty`
- `cute`, `kawaii`, `character`, `colorful`

### Food Trends:

- `matcha`, `taro`, `brown sugar`, `bubble tea`
- `keto`, `vegan`, `gluten-free`, `organic`

### Seasonal Trends:

- `valentine`, `christmas`, `halloween`, `tet`
- `summer`, `winter`, `spring`, `autumn`

## 🚨 Troubleshooting

### Common Issues:

1. **Server not running**: Kiểm tra xem uvicorn có đang chạy không
2. **Connection refused**: Đảm bảo port 8000 không bị block
3. **500 Error**: Kiểm tra GEMINI_API_KEY trong .env file
4. **Empty response**: Kiểm tra request body format

### Debug Steps:

1. Test health endpoints trước
2. Kiểm tra server logs
3. Validate JSON format trong request body
4. Đảm bảo Content-Type header đúng

## 📖 API Documentation

### Auto-generated docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Manual test với curl:

```bash
# Health check
curl http://localhost:8000/health

# Generate recipe from ingredients
curl -X POST "http://localhost:8000/api/v1/recipes/generate-from-ingredients" \
     -H "Content-Type: application/json" \
     -d '{"ingredients": "bột mì, đường, trứng", "language": "vi"}'

# Generate recipe from trend
curl -X POST "http://localhost:8000/api/v1/recipes/generate-from-trend" \
     -H "Content-Type: application/json" \
     -d '{"trend": "labubu valentine", "user_segment": "genz", "language": "vi"}'
```

## 🎉 Happy Testing!

Với collection này, bạn có thể test toàn bộ tính năng AI Recipe Generation của RCM_RECIPE_2! 🍰✨
