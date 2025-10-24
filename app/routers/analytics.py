# app/routers/analytics.py
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from domain.services.context_aware_recipe_service import ContextAwareRecipeService
from domain.services.recipe_generation_service import RecipeGenerationService
from infrastructure.ml_models.trend_predictor import TrendPredictor
import subprocess
import sys
from pathlib import Path

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Initialize services
context_service = ContextAwareRecipeService()
trend_predictor = TrendPredictor()
recipe_service = RecipeGenerationService()

class TrendPredictionRequest(BaseModel):
    target_date: Optional[str] = None  # Format: "2025-10-31"
    user_segment: str = "gen_z"
    location: str = "vietnam"
    custom_context: Optional[Dict[str, Any]] = None

class TrendPredictionResponse(BaseModel):
    predictions: Dict[str, float]
    seasonal_context: Dict[str, Any]
    market_context: Dict[str, Any]
    recommended_ingredients: List[str]
    trending_flavors: List[str]
    optimal_occasions: List[str]

class RecipeAnalyticsRequest(BaseModel):
    user_segment: str
    target_date: Optional[str] = None
    trend_keywords: Optional[List[str]] = None
    include_market_analysis: bool = True

class RecipeAnalyticsResponse(BaseModel):
    recipe: Dict[str, Any]
    analytics: Dict[str, Any]
    market_insights: Dict[str, Any]
    success_factors: List[str]
    viral_potential_score: float

class ForecastAndGenerateRequest(BaseModel):
    user_segment: str
    horizon_days: int = 30
    top_k: int = 3
    include_market_analysis: bool = True
    location: str = "vietnam"
    custom_context: Optional[Dict[str, Any]] = None

class ForecastAndGenerateResponse(BaseModel):
    forecast_window: Dict[str, Any]
    top_forecasted_events: List[str]
    trends_summary: Dict[str, Any]
    recommended_recipes: List[Dict[str, Any]]

class MarketInsightResponse(BaseModel):
    segment_analysis: Dict[str, Any]
    seasonal_trends: Dict[str, Any]
    competition_analysis: Dict[str, Any]
    opportunity_score: float
    recommended_strategies: List[str]

@router.post("/predict-trends", response_model=TrendPredictionResponse)
async def predict_future_trends(request: TrendPredictionRequest):
    """
    🔮 Dự đoán xu hướng bánh ngọt trong tương lai
    
    API này sử dụng ML models và context analysis để dự đoán:
    - Xu hướng viral potential
    - Nguyên liệu hot
    - Hương vị trending
    - Dịp tối ưu để bán
    """
    try:
        # Parse target date
        if request.target_date:
            target_date = datetime.strptime(request.target_date, "%Y-%m-%d")
        else:
            target_date = datetime.now()
        
        # Get contexts
        seasonal_ctx, market_ctx = context_service.get_current_context(target_date)
        
        # Update market context with requested segment
        market_ctx = context_service._get_market_context(request.user_segment)
        
        # Prepare ML context
        ml_context = {
            'month': seasonal_ctx.month,
            'temperature': seasonal_ctx.temperature,
            'user_segment': request.user_segment,
            'season': seasonal_ctx.season,
            'market_potential': market_ctx.market_potential,
            'competition_level': market_ctx.competition_level,
            'bakery_demand': seasonal_ctx.demand_factor
        }
        
        # Add custom context nếu có
        if request.custom_context:
            ml_context.update(request.custom_context)
        
        # Get ML predictions
        try:
            predictions = trend_predictor.predict_trends(ml_context)
        except Exception as e:
            print(f"ML prediction failed: {e}")
            predictions = {
                'popularity_score': 0.7,
                'engagement_score': 0.6,
                'trend_score': 0.5,
                'overall_trend_strength': 0.6
            }
        
        # Analyze recommended ingredients based on season and trends
        recommended_ingredients = context_service._get_recommended_ingredients(
            seasonal_ctx, market_ctx, predictions['overall_trend_strength']
        )
        
        return TrendPredictionResponse(
            predictions=predictions,
            seasonal_context={
                'season': seasonal_ctx.season,
                'month': seasonal_ctx.month,
                'temperature': seasonal_ctx.temperature,
                'events': seasonal_ctx.events,
                'demand_factor': seasonal_ctx.demand_factor
            },
            market_context={
                'target_segment': market_ctx.target_segment,
                'market_potential': market_ctx.market_potential,
                'competition_level': market_ctx.competition_level,
                'growth_trend': market_ctx.growth_trend,
                'price_sensitivity': market_ctx.price_sensitivity
            },
            recommended_ingredients=recommended_ingredients,
            trending_flavors=seasonal_ctx.trending_flavors,
            optimal_occasions=seasonal_ctx.popular_occasions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/forecast-and-generate", response_model=ForecastAndGenerateResponse)
async def forecast_and_generate(request: ForecastAndGenerateRequest):
    """
    📈 Dự báo xu hướng trong tương lai gần và tạo danh sách công thức đề xuất.
    - Dự báo context 4 tuần tới (mặc định 30 ngày)
    - Chọn ra top sự kiện/xu hướng có tiềm năng cao nhất
    - Sinh ra recipe đề xuất theo từng sự kiện/xu hướng
    """
    try:
        now = datetime.now()
        horizon_days = max(7, min(request.horizon_days, 90))

        # Quét từng tuần trong horizon để dự báo
        weekly_points = []
        for delta in range(0, horizon_days, 7):
            target_date = now + timedelta(days=delta)
            seasonal_ctx, market_ctx = context_service.get_current_context(target_date)

            ml_context = {
                'month': seasonal_ctx.month,
                'temperature': seasonal_ctx.temperature,
                'user_segment': request.user_segment,
                'season': seasonal_ctx.season,
                'market_potential': market_ctx.market_potential,
                'competition_level': market_ctx.competition_level,
                'bakery_demand': seasonal_ctx.demand_factor
            }
            if request.custom_context:
                ml_context.update(request.custom_context)

            try:
                preds = trend_predictor.predict_trends(ml_context)
            except Exception as e:
                # fallback khi model chưa train
                preds = {
                    'popularity_score': 0.65,
                    'engagement_score': 0.6,
                    'trend_score': 0.55,
                    'overall_trend_strength': 0.6
                }

            weekly_points.append({
                'date': target_date.strftime("%Y-%m-%d"),
                'events': seasonal_ctx.events,
                'trending_flavors': seasonal_ctx.trending_flavors,
                'overall_trend_strength': preds['overall_trend_strength'],
                'season': seasonal_ctx.season
            })

        # Xếp hạng sự kiện theo trend strength trung bình trong horizon
        event_scores: Dict[str, float] = {}
        for point in weekly_points:
            for evt in point['events']:
                event_scores.setdefault(evt, 0.0)
                event_scores[evt] += point['overall_trend_strength']

        # Top-k sự kiện
        top_events = sorted(event_scores.items(), key=lambda x: x[1], reverse=True)
        top_events = [e for e, _ in top_events[:max(1, request.top_k)]] or ["Regular season"]

        # Sinh công thức đề xuất cho mỗi sự kiện top bằng pipeline Gemini generate-from-trend
        recommended_recipes = []
        for evt in top_events:
            # Lấy ngày đại diện (ngày đầu tiên có evt)
            rep_date = next((p['date'] for p in weekly_points if evt in p['events']), weekly_points[0]['date'])
            rep_dt = datetime.strptime(rep_date, "%Y-%m-%d")

            # Kết hợp trend string từ event + flavors
            seasonal_ctx, _ = context_service.get_current_context(rep_dt)
            trend_text = " ".join([evt] + (seasonal_ctx.trending_flavors[:3] if seasonal_ctx.trending_flavors else [])) if evt != "Regular season" else " ".join(seasonal_ctx.trending_flavors[:3] or [])

            # Gọi pipeline generate-from-trend (Gemini) để tạo recipe chi tiết tiếng Việt
            gen_recipe = recipe_service.generate_from_trend(
                trend=trend_text.strip() or "seasonal",
                user_segment=request.user_segment,
                occasion=evt if evt != "Regular season" else seasonal_ctx.season,
                language='vi'
            )

            analytics = await _analyze_recipe_performance(gen_recipe, request.user_segment, rep_dt)
            market_insights = await _get_market_insights(request.user_segment, rep_dt) if request.include_market_analysis else {}
            viral_score = _calculate_viral_potential(gen_recipe, analytics, market_insights)

            recommended_recipes.append({
                'event': evt,
                'date': rep_date,
                'viral_potential': viral_score,
                'recipe': gen_recipe.dict(),
                'analytics': analytics,
                'market_insights': market_insights
            })

        response = ForecastAndGenerateResponse(
            forecast_window={
                'start': now.strftime("%Y-%m-%d"),
                'end': (now + timedelta(days=horizon_days)).strftime("%Y-%m-%d"),
                'points': weekly_points
            },
            top_forecasted_events=top_events,
            trends_summary={
                'avg_trend_strength': round(sum(p['overall_trend_strength'] for p in weekly_points) / len(weekly_points), 3),
                'seasons_in_window': sorted(list({p['season'] for p in weekly_points}))
            },
            recommended_recipes=recommended_recipes
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast and generate failed: {str(e)}")

@router.post("/train")
async def train_models():
    """
    🧠 Khởi chạy pipeline huấn luyện ML từ dữ liệu trong data/raw và cập nhật artifacts.
    Trả về log cơ bản và trạng thái.
    """
    try:
        # Chạy train_models.py bằng python hiện tại
        project_root = Path(__file__).resolve().parents[2]
        script_path = project_root / "train_models.py"
        if not script_path.exists():
            raise HTTPException(status_code=500, detail="Không tìm thấy train_models.py")

        proc = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        success = proc.returncode == 0
        output = (proc.stdout or "")[-4000:]  # Giới hạn log trả về
        error = (proc.stderr or "")[-4000:]

        # Reload models nếu train thành công
        if success:
            trend_predictor.load_models()

        return {
            'status': 'success' if success else 'failed',
            'return_code': proc.returncode,
            'stdout_tail': output,
            'stderr_tail': error
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Train failed: {str(e)}")

@router.post("/generate-smart-recipe", response_model=RecipeAnalyticsResponse)
async def generate_smart_recipe(request: RecipeAnalyticsRequest):
    """
    🤖 Tạo công thức thông minh với phân tích toàn diện
    
    API này kết hợp:
    - Context-aware recipe generation
    - Market analysis
    - Viral potential scoring
    - Success factor identification
    """
    try:
        # Parse target date
        if request.target_date:
            target_date = datetime.strptime(request.target_date, "%Y-%m-%d")
        else:
            target_date = datetime.now()
        
        # Generate context-aware recipe
        custom_trend = " ".join(request.trend_keywords) if request.trend_keywords else None
        
        recipe = context_service.generate_context_aware_recipe(
            user_segment=request.user_segment,
            target_date=target_date,
            custom_trend=custom_trend
        )
        
        # Get detailed analytics
        analytics = await _analyze_recipe_performance(recipe, request.user_segment, target_date)
        
        # Get market insights nếu được yêu cầu
        market_insights = {}
        if request.include_market_analysis:
            market_insights = await _get_market_insights(request.user_segment, target_date)
        
        # Calculate viral potential
        viral_score = _calculate_viral_potential(recipe, analytics, market_insights)
        
        # Identify success factors
        success_factors = _identify_success_factors(recipe, analytics, market_insights)
        
        return RecipeAnalyticsResponse(
            recipe=recipe.dict(),
            analytics=analytics,
            market_insights=market_insights,
            success_factors=success_factors,
            viral_potential_score=viral_score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {str(e)}")

@router.get("/market-insights/{segment}", response_model=MarketInsightResponse)
async def get_market_insights(
    segment: str,
    target_date: Optional[str] = Query(None, description="Target date (YYYY-MM-DD)"),
    include_competition: bool = Query(True, description="Include competition analysis")
):
    """
    📊 Phân tích sâu insights thị trường cho segment cụ thể
    
    Cung cấp:
    - Phân tích chi tiết segment
    - Xu hướng mùa vụ
    - Phân tích đối thủ
    - Điểm cơ hội
    - Chiến lược được gợi ý
    """
    try:
        # Parse date
        if target_date:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d")
        else:
            parsed_date = datetime.now()
        
        # Get market insights
        insights = await _get_comprehensive_market_insights(
            segment, parsed_date, include_competition
        )
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market insights failed: {str(e)}")

@router.get("/trending-now")
async def get_trending_now():
    """
    🔥 Lấy xu hướng hot nhất hiện tại
    
    Real-time analysis của:
    - Keywords trending
    - Flavors đang hot
    - Events sắp tới
    - Seasonal opportunities
    """
    try:
        now = datetime.now()
        seasonal_ctx, _ = context_service.get_current_context(now)
        
        # Get trending data from recent analysis
        trending_data = {
            'current_season': seasonal_ctx.season,
            'hot_events': seasonal_ctx.events,
            'trending_flavors': seasonal_ctx.trending_flavors,
            'popular_occasions': seasonal_ctx.popular_occasions,
            'temperature_context': f"{seasonal_ctx.temperature}°C",
            'demand_factor': seasonal_ctx.demand_factor,
            'month_insights': _get_month_specific_insights(now.month),
            'week_forecast': _get_weekly_forecast(now),
            'viral_keywords': _get_viral_keywords_now(),
            'opportunity_score': _calculate_current_opportunity_score(seasonal_ctx)
        }
        
        return {
            'status': 'success',
            'timestamp': now.isoformat(),
            'data': trending_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trending analysis failed: {str(e)}")

@router.get("/segment-recommendations/{segment}")
async def get_segment_recommendations(segment: str):
    """
    🎯 Gợi ý chi tiết cho segment cụ thể
    
    Tailored recommendations bao gồm:
    - Flavors preferences
    - Price points optimal
    - Marketing strategies
    - Timing recommendations
    """
    try:
        # Get market context cho segment
        market_ctx = context_service._get_market_context(segment)
        seasonal_ctx, _ = context_service.get_current_context()
        
        recommendations = {
            'segment_profile': {
                'name': market_ctx.target_segment,
                'market_potential': market_ctx.market_potential,
                'competition_level': market_ctx.competition_level,
                'growth_trend': market_ctx.growth_trend,
                'preferred_flavors': market_ctx.preferred_flavors,
                'price_sensitivity': market_ctx.price_sensitivity
            },
            'current_opportunities': _get_segment_opportunities(market_ctx, seasonal_ctx),
            'recommended_products': _get_recommended_products(segment, seasonal_ctx),
            'pricing_strategy': _get_pricing_strategy(market_ctx),
            'marketing_tips': _get_marketing_tips(market_ctx, seasonal_ctx),
            'success_metrics': _get_success_metrics(segment),
            'timing_optimization': _get_timing_optimization(seasonal_ctx)
        }
        
        return {
            'status': 'success',
            'segment': segment,
            'data': recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segment recommendations failed: {str(e)}")

# Helper functions
async def _analyze_recipe_performance(recipe, segment: str, target_date: datetime) -> Dict[str, Any]:
    """Phân tích performance potential của recipe"""
    
    seasonal_ctx, market_ctx = context_service.get_current_context(target_date)
    
    # Analyze ingredients alignment with trends
    ingredient_score = _score_ingredient_alignment(recipe.ingredients, seasonal_ctx.trending_flavors)
    
    # Analyze timing alignment
    timing_score = _score_timing_alignment(target_date, seasonal_ctx)
    
    # Analyze segment fit
    segment_score = _score_segment_fit(recipe, market_ctx)
    
    return {
        'ingredient_trend_alignment': ingredient_score,
        'timing_optimization': timing_score,
        'segment_fit_score': segment_score,
        'complexity_score': _score_complexity(recipe.difficulty),
        'seasonality_match': _score_seasonality(recipe, seasonal_ctx),
        'viral_elements': _identify_viral_elements(recipe),
        'cost_efficiency': _estimate_cost_efficiency(recipe.ingredients),
        'preparation_feasibility': _score_preparation_feasibility(recipe)
    }

async def _get_market_insights(segment: str, target_date: datetime) -> Dict[str, Any]:
    """Lấy market insights cho segment"""
    
    market_ctx = context_service._get_market_context(segment)
    seasonal_ctx, _ = context_service.get_current_context(target_date)
    
    return {
        'market_size_estimate': _estimate_market_size(market_ctx),
        'competition_density': market_ctx.competition_level,
        'growth_potential': _analyze_growth_potential(market_ctx),
        'seasonal_multiplier': seasonal_ctx.demand_factor,
        'price_elasticity': _analyze_price_elasticity(market_ctx),
        'channel_preferences': _get_channel_preferences(segment),
        'buying_triggers': _identify_buying_triggers(market_ctx, seasonal_ctx)
    }

def _calculate_viral_potential(recipe, analytics: Dict, market_insights: Dict) -> float:
    """Tính viral potential score"""
    
    # Base factors
    ingredient_trend = analytics.get('ingredient_trend_alignment', 0.5)
    timing_opt = analytics.get('timing_optimization', 0.5)
    segment_fit = analytics.get('segment_fit_score', 0.5)
    viral_elements = len(analytics.get('viral_elements', [])) / 10  # Normalize to 0-1
    
    # Market factors
    market_potential = market_insights.get('growth_potential', 0.5)
    
    # Calculate weighted score
    viral_score = (
        ingredient_trend * 0.25 +
        timing_opt * 0.20 +
        segment_fit * 0.20 +
        viral_elements * 0.20 +
        market_potential * 0.15
    )
    
    return min(viral_score, 1.0)

def _identify_success_factors(recipe, analytics: Dict, market_insights: Dict) -> List[str]:
    """Identify key success factors"""
    
    factors = []
    
    if analytics.get('ingredient_trend_alignment', 0) > 0.7:
        factors.append("✅ Ingredients align perfectly with current trends")
    
    if analytics.get('timing_optimization', 0) > 0.7:
        factors.append("✅ Perfect timing for seasonal demand")
    
    if analytics.get('segment_fit_score', 0) > 0.7:
        factors.append("✅ Excellent match for target segment preferences")
    
    if len(analytics.get('viral_elements', [])) >= 3:
        factors.append("✅ Contains multiple viral-worthy elements")
    
    if market_insights.get('growth_potential', 0) > 0.6:
        factors.append("✅ High market growth potential")
    
    if analytics.get('cost_efficiency', 0) > 0.6:
        factors.append("✅ Cost-efficient ingredient selection")
    
    return factors

# Additional helper functions for comprehensive analysis
def _score_ingredient_alignment(ingredients, trending_flavors) -> float:
    """Score how well ingredients align with trending flavors"""
    if not trending_flavors:
        return 0.5
    
    alignment_count = 0
    total = max(len(ingredients or []), 1)
    for ingredient in ingredients or []:
        for flavor in trending_flavors:
            if flavor.lower() in ingredient.name.lower():
                alignment_count += 1
                break
    
    return min(alignment_count / total, 1.0)

def _score_timing_alignment(target_date: datetime, seasonal_ctx) -> float:
    """Score timing alignment với seasonal context"""
    
    # Check nếu trong peak months
    month = target_date.month
    
    seasonal_peaks = {
        'Xuân': [3, 4, 5], 'Hè': [6, 7, 8], 
        'Thu': [9, 10, 11], 'Đông': [12, 1, 2]
    }
    
    peak_months = seasonal_peaks.get(seasonal_ctx.season, [])
    
    if month in peak_months:
        return 0.9
    elif abs(month - peak_months[len(peak_months)//2]) <= 1:
        return 0.7
    else:
        return 0.4

def _score_segment_fit(recipe, market_ctx) -> float:
    """Score recipe fit với market segment"""
    
    # Simple scoring based on complexity and preferences
    complexity_map = {'easy': 0.8, 'medium': 0.6, 'hard': 0.3}
    complexity_score = complexity_map.get(recipe.difficulty, 0.5)
    
    # Price sensitivity alignment (simple heuristic)
    if market_ctx.price_sensitivity == 'thấp':
        price_score = 0.9 if recipe.difficulty == 'hard' else 0.6
    elif market_ctx.price_sensitivity == 'cao':
        price_score = 0.9 if recipe.difficulty == 'easy' else 0.4
    else:
        price_score = 0.7
    
    return (complexity_score + price_score) / 2

def _score_complexity(difficulty: str) -> float:
    """Score recipe complexity"""
    complexity_scores = {'easy': 0.9, 'medium': 0.7, 'hard': 0.4}
    return complexity_scores.get(difficulty, 0.5)

def _score_seasonality(recipe, seasonal_ctx) -> float:
    """Score seasonal relevance"""
    
    seasonal_ingredients = {
        'Xuân': ['strawberry', 'dâu', 'green tea', 'trà xanh'],
        'Hè': ['mango', 'xoài', 'coconut', 'dừa', 'lemon'],
        'Thu': ['pumpkin', 'bí đỏ', 'apple', 'táo', 'cinnamon'],
        'Đông': ['chocolate', 'gingerbread', 'orange', 'cam']
    }
    
    season_ingredients = seasonal_ingredients.get(seasonal_ctx.season, [])
    
    match_count = 0
    for ingredient in recipe.ingredients:
        for seasonal_ing in season_ingredients:
            if seasonal_ing.lower() in ingredient.name.lower():
                match_count += 1
                break
    
    return min(match_count / max(len(recipe.ingredients), 1), 1.0)

def _identify_viral_elements(recipe) -> List[str]:
    """Identify elements that could make recipe viral"""
    
    viral_elements = []
    
    # Check title for viral words
    viral_keywords = ['trending', 'viral', 'hot', 'new', 'special', 'unique', 'amazing']
    if any(word in recipe.title.lower() for word in viral_keywords):
        viral_elements.append("Viral title keywords")
    
    # Check for seasonal relevance
    if any(tag in ['Halloween', 'Christmas', 'Valentine', 'Tết'] for tag in recipe.tags):
        viral_elements.append("Seasonal event tie-in")
    
    # Check for trending ingredients
    trending_ingredients = ['matcha', 'taro', 'ube', 'brown sugar', 'cheese foam']
    if any(ing.name.lower() in trending_ingredients for ing in recipe.ingredients):
        viral_elements.append("Trending ingredients")
    
    # Check difficulty (easier = more viral potential)
    if recipe.difficulty == 'easy':
        viral_elements.append("Easy to make (shareable)")
    
    return viral_elements

def _estimate_cost_efficiency(ingredients) -> float:
    """Estimate cost efficiency of ingredients"""
    
    # Simple cost categories (would be better with real pricing data)
    expensive_ingredients = ['vanilla', 'chocolate', 'cream', 'butter', 'nuts']
    cheap_ingredients = ['flour', 'sugar', 'milk', 'eggs']
    
    expensive_count = sum(1 for ing in ingredients 
                         if any(exp in ing.name.lower() for exp in expensive_ingredients))
    
    total_ingredients = len(ingredients)
    if total_ingredients == 0:
        return 0.5
    
    # Higher score for fewer expensive ingredients
    return max(0, 1 - (expensive_count / total_ingredients))

def _score_preparation_feasibility(recipe) -> float:
    """Score how feasible the recipe is to prepare"""
    
    # Factor in prep time, cook time, complexity
    try:
        prep_minutes = int(recipe.prep_time.split()[0]) if recipe.prep_time else 30
        cook_minutes = int(recipe.cook_time.split()[0]) if recipe.cook_time else 30
        
        total_time = prep_minutes + cook_minutes
        
        # Score based on total time (shorter = higher feasibility)
        if total_time <= 60:
            time_score = 0.9
        elif total_time <= 120:
            time_score = 0.7
        else:
            time_score = 0.4
        
        # Factor in difficulty
        difficulty_scores = {'easy': 0.9, 'medium': 0.6, 'hard': 0.3}
        difficulty_score = difficulty_scores.get(recipe.difficulty, 0.5)
        
        return (time_score + difficulty_score) / 2
        
    except:
        return 0.5

# Additional helper functions for market insights
async def _get_comprehensive_market_insights(segment: str, target_date: datetime, include_competition: bool) -> MarketInsightResponse:
    """Get comprehensive market insights"""
    
    market_ctx = context_service._get_market_context(segment)
    seasonal_ctx, _ = context_service.get_current_context(target_date)
    
    segment_analysis = {
        'profile': market_ctx.__dict__,
        'size_estimate': _estimate_market_size(market_ctx),
        'engagement_potential': _estimate_engagement_potential(market_ctx),
        'price_optimization': _get_price_optimization(market_ctx)
    }
    
    seasonal_trends = {
        'current_season': seasonal_ctx.season,
        'demand_multiplier': seasonal_ctx.demand_factor,
        'trending_flavors': seasonal_ctx.trending_flavors,
        'upcoming_events': seasonal_ctx.events,
        'temperature_impact': seasonal_ctx.temperature
    }
    
    competition_analysis = {}
    if include_competition:
        competition_analysis = {
            'intensity': market_ctx.competition_level,
            'differentiation_opportunities': _find_differentiation_opportunities(market_ctx),
            'competitive_advantages': _identify_competitive_advantages(market_ctx, seasonal_ctx)
        }
    
    opportunity_score = _calculate_opportunity_score(market_ctx, seasonal_ctx)
    
    strategies = _generate_recommended_strategies(market_ctx, seasonal_ctx, opportunity_score)
    
    return MarketInsightResponse(
        segment_analysis=segment_analysis,
        seasonal_trends=seasonal_trends,
        competition_analysis=competition_analysis,
        opportunity_score=opportunity_score,
        recommended_strategies=strategies
    )

def _estimate_market_size(market_ctx) -> str:
    """Estimate market size for segment"""
    if market_ctx.market_potential > 0.8:
        return "Large (High potential)"
    elif market_ctx.market_potential > 0.6:
        return "Medium (Moderate potential)"
    else:
        return "Small (Limited potential)"

def _calculate_opportunity_score(market_ctx, seasonal_ctx) -> float:
    """Calculate overall opportunity score"""
    return (
        market_ctx.market_potential * 0.4 +
        (1 - market_ctx.competition_level) * 0.3 +  # Lower competition = higher opportunity
        seasonal_ctx.demand_factor * 0.3
    )

def _generate_recommended_strategies(market_ctx, seasonal_ctx, opportunity_score: float) -> List[str]:
    """Generate strategic recommendations"""
    
    strategies = []
    
    if opportunity_score > 0.7:
        strategies.append("🚀 High opportunity - Aggressive market entry recommended")
    
    if market_ctx.competition_level > 0.8:
        strategies.append("💡 Focus on differentiation and unique value proposition")
    
    if seasonal_ctx.demand_factor > 1.2:
        strategies.append("⏰ Capitalize on seasonal demand peak")
    
    if market_ctx.growth_trend == "Tăng mạnh":
        strategies.append("📈 Scale production to meet growing demand")
    
    if market_ctx.price_sensitivity == "thấp":
        strategies.append("💰 Premium pricing strategy viable")
    
    return strategies

def _get_month_specific_insights(month: int) -> Dict[str, Any]:
    """Get insights specific to current month"""
    
    month_insights = {
        10: {
            'events': ['Halloween', 'Thu hoạch', 'Tháng ma quỷ'],
            'trending_themes': ['Spooky', 'Orange', 'Pumpkin', 'Dark chocolate'],
            'opportunities': ['Theme parties', 'School events', 'Horror movie tie-ins'],
            'recommended_colors': ['Orange', 'Black', 'Purple', 'Gold']
        },
        2: {
            'events': ['Tết', 'Valentine', 'Xuân về'],
            'trending_themes': ['Love', 'Red', 'Traditional', 'Prosperity'],
            'opportunities': ['Valentine gifts', 'Tết treats', 'Spring celebrations'],
            'recommended_colors': ['Red', 'Pink', 'Gold', 'White']
        },
        12: {
            'events': ['Christmas', 'Năm mới', 'Đông'],
            'trending_themes': ['Festive', 'Green', 'Red', 'Gingerbread'],
            'opportunities': ['Holiday parties', 'Gift giving', 'Family gatherings'],
            'recommended_colors': ['Red', 'Green', 'Gold', 'Silver']
        }
    }
    
    return month_insights.get(month, {
        'events': ['Regular season'],
        'trending_themes': ['Classic', 'Simple', 'Everyday'],
        'opportunities': ['Daily treats', 'Regular occasions'],
        'recommended_colors': ['Natural tones']
    })

def _get_weekly_forecast(current_date: datetime) -> Dict[str, Any]:
    """Get forecast for next week"""
    
    next_week = current_date + timedelta(days=7)
    
    return {
        'target_date': next_week.strftime("%Y-%m-%d"),
        'predicted_demand': "Medium to High",
        'recommended_prep_time': "3-4 days ahead",
        'optimal_launch_day': "Friday or Saturday",
        'expected_engagement': "Peak on weekends"
    }

def _get_viral_keywords_now() -> List[str]:
    """Get currently viral keywords"""
    
    # This would ideally connect to real-time trend APIs
    current_month = datetime.now().month
    
    seasonal_viral = {
        10: ['halloween', 'spooky', 'pumpkin', 'october', 'autumn', 'cozy'],
        11: ['thanksgiving', 'gratitude', 'harvest', 'family'],
        12: ['christmas', 'holiday', 'festive', 'winter', 'cozy', 'warm'],
        1: ['new year', 'resolution', 'fresh start', 'healthy'],
        2: ['valentine', 'love', 'romantic', 'tet', 'spring'],
        3: ['spring', 'fresh', 'green', 'renewal'],
        6: ['summer', 'cool', 'refreshing', 'vacation'],
        7: ['summer', 'ice', 'cold', 'beach'],
        8: ['back to school', 'energy', 'preparation']
    }
    
    return seasonal_viral.get(current_month, ['trending', 'popular', 'delicious', 'homemade'])

def _calculate_current_opportunity_score(seasonal_ctx) -> float:
    """Calculate current opportunity score"""
    
    # Base on seasonal demand and events
    base_score = seasonal_ctx.demand_factor
    
    # Boost for special events
    if seasonal_ctx.events:
        event_boost = len(seasonal_ctx.events) * 0.1
        base_score += event_boost
    
    # Temperature consideration
    if 20 <= seasonal_ctx.temperature <= 30:  # Optimal baking weather
        base_score += 0.1
    
    return min(base_score, 1.0)

def _get_segment_opportunities(market_ctx, seasonal_ctx) -> List[str]:
    """Get current opportunities for segment"""
    
    opportunities = []
    
    if market_ctx.growth_trend == "Tăng mạnh":
        opportunities.append(f"📈 {market_ctx.target_segment} segment showing strong growth")
    
    if seasonal_ctx.demand_factor > 1.0:
        opportunities.append(f"🔥 High seasonal demand ({seasonal_ctx.demand_factor:.1f}x normal)")
    
    if seasonal_ctx.events:
        opportunities.append(f"🎉 Upcoming events: {', '.join(seasonal_ctx.events)}")
    
    if market_ctx.competition_level < 0.7:
        opportunities.append("💎 Lower competition creates market opportunity")
    
    return opportunities

def _get_recommended_products(segment: str, seasonal_ctx) -> List[str]:
    """Get recommended products for segment"""
    
    segment_products = {
        'gen_z': ['Aesthetic cakes', 'Minimalist designs', 'Trendy flavors', 'Instagram-worthy'],
        'millennials': ['Artisan quality', 'Organic ingredients', 'Sophisticated flavors', 'Premium presentation'],
        'gym': ['Protein-rich', 'Low sugar', 'High nutrition', 'Clean ingredients'],
        'kids': ['Colorful designs', 'Fun shapes', 'Mild flavors', 'Interactive elements']
    }
    
    base_products = segment_products.get(segment.lower(), ['Classic cakes', 'Traditional flavors'])
    
    # Add seasonal products
    if seasonal_ctx.trending_flavors:
        seasonal_products = [f"{flavor} variations" for flavor in seasonal_ctx.trending_flavors[:2]]
        base_products.extend(seasonal_products)
    
    return base_products

def _get_pricing_strategy(market_ctx) -> Dict[str, Any]:
    """Get pricing strategy for market context"""
    
    if market_ctx.price_sensitivity == "thấp":
        return {
            'strategy': 'Premium pricing',
            'price_range': 'High-end',
            'positioning': 'Luxury/Premium',
            'recommendations': ['Focus on quality', 'Premium ingredients', 'Exclusive designs']
        }
    elif market_ctx.price_sensitivity == "cao":
        return {
            'strategy': 'Value pricing',
            'price_range': 'Budget-friendly',
            'positioning': 'Accessible/Affordable',
            'recommendations': ['Cost optimization', 'Bundle deals', 'Volume discounts']
        }
    else:
        return {
            'strategy': 'Competitive pricing',
            'price_range': 'Mid-range',
            'positioning': 'Quality-Value balance',
            'recommendations': ['Market-competitive rates', 'Quality focus', 'Occasional promotions']
        }

def _get_marketing_tips(market_ctx, seasonal_ctx) -> List[str]:
    """Get marketing tips for context"""
    
    tips = []
    
    # Segment-specific tips
    if 'gen' in market_ctx.target_segment.lower():
        tips.append("📱 Focus on social media marketing (Instagram, TikTok)")
        tips.append("🎨 Emphasize visual appeal and aesthetic presentation")
    
    if 'gym' in market_ctx.target_segment.lower():
        tips.append("💪 Highlight health benefits and nutritional value")
        tips.append("🏃‍♀️ Partner with fitness influencers and gyms")
    
    # Seasonal tips
    if seasonal_ctx.events:
        tips.append(f"🎉 Create themed content around {', '.join(seasonal_ctx.events)}")
    
    if seasonal_ctx.trending_flavors:
        tips.append(f"🍰 Promote trending flavors: {', '.join(seasonal_ctx.trending_flavors)}")
    
    # Competition-based tips
    if market_ctx.competition_level > 0.8:
        tips.append("🎯 Focus on unique selling propositions and differentiation")
    
    return tips

def _get_success_metrics(segment: str) -> Dict[str, Any]:
    """Get success metrics to track"""
    
    return {
        'engagement_metrics': ['Social media engagement', 'Share rate', 'User-generated content'],
        'sales_metrics': ['Conversion rate', 'Average order value', 'Repeat purchases'],
        'brand_metrics': ['Brand awareness', 'Customer satisfaction', 'Market share'],
        'kpis': [
            f'{segment} segment penetration',
            'Seasonal revenue growth',
            'Cost per acquisition',
            'Customer lifetime value'
        ]
    }

def _get_timing_optimization(seasonal_ctx) -> Dict[str, Any]:
    """Get timing optimization recommendations"""
    
    return {
        'best_launch_days': ['Friday', 'Saturday'] if seasonal_ctx.demand_factor > 1.0 else ['Thursday', 'Friday'],
        'optimal_seasons': [seasonal_ctx.season] if seasonal_ctx.demand_factor > 1.0 else ['All seasons'],
        'event_timing': f"Launch 1-2 weeks before {', '.join(seasonal_ctx.events)}" if seasonal_ctx.events else "Regular timing",
        'production_planning': f"Increase production by {int(seasonal_ctx.demand_factor * 100)}%" if seasonal_ctx.demand_factor > 1.0 else "Normal production levels"
    }

# Additional helper functions for analytics
def _analyze_growth_potential(market_ctx) -> float:
    """Analyze growth potential score"""
    growth_scores = {
        'Tăng mạnh': 0.9,
        'Tăng': 0.7,
        'Ổn định': 0.5,
        'Giảm': 0.3
    }
    return growth_scores.get(market_ctx.growth_trend, 0.5)

def _estimate_engagement_potential(market_ctx) -> float:
    """Estimate engagement potential"""
    # Simple heuristic based on market characteristics
    base_score = market_ctx.market_potential
    
    # Boost for high growth segments
    if market_ctx.growth_trend == "Tăng mạnh":
        base_score += 0.2
    
    # Penalty for high competition
    if market_ctx.competition_level > 0.8:
        base_score -= 0.1
    
    return min(max(base_score, 0), 1)

def _get_price_optimization(market_ctx) -> Dict[str, str]:
    """Get price optimization recommendations"""
    
    if market_ctx.price_sensitivity == "thấp":
        return {
            'strategy': 'Premium pricing viable',
            'markup': 'High margin (40-60%)',
            'positioning': 'Luxury segment'
        }
    elif market_ctx.price_sensitivity == "cao":
        return {
            'strategy': 'Competitive pricing required',
            'markup': 'Lower margin (20-30%)',
            'positioning': 'Value segment'
        }
    else:
        return {
            'strategy': 'Balanced pricing',
            'markup': 'Standard margin (30-40%)',
            'positioning': 'Mid-market'
        }

def _find_differentiation_opportunities(market_ctx) -> List[str]:
    """Find differentiation opportunities"""
    
    opportunities = []
    
    if market_ctx.competition_level > 0.8:
        opportunities.extend([
            "Unique flavor combinations",
            "Premium ingredient sourcing",
            "Customization options",
            "Exceptional presentation",
            "Themed collections"
        ])
    
    if market_ctx.growth_trend == "Tăng mạnh":
        opportunities.extend([
            "First-mover advantage in trends",
            "Innovative formats",
            "Social media optimization"
        ])
    
    return opportunities

def _identify_competitive_advantages(market_ctx, seasonal_ctx) -> List[str]:
    """Identify potential competitive advantages"""
    
    advantages = []
    
    if seasonal_ctx.demand_factor > 1.2:
        advantages.append("Strong seasonal demand timing")
    
    if market_ctx.market_potential > 0.7:
        advantages.append("High market potential segment")
    
    if len(seasonal_ctx.trending_flavors) > 3:
        advantages.append("Rich seasonal flavor options")
    
    if seasonal_ctx.events:
        advantages.append(f"Event-driven opportunities: {', '.join(seasonal_ctx.events)}")
    
    return advantages

# Add method to context service for ingredient recommendations
def _get_recommended_ingredients(self, seasonal_ctx, market_ctx, trend_strength: float) -> List[str]:
    """Get recommended ingredients based on context"""
    
    base_ingredients = seasonal_ctx.trending_flavors.copy()
    
    # Add segment-specific ingredients
    segment_ingredients = {
        'Gen Z': ['matcha', 'taro', 'ube', 'brown sugar', 'cheese foam'],
        'Millennials': ['vanilla bean', 'dark chocolate', 'salted caramel', 'artisan coffee'],
        'Gym': ['protein powder', 'oats', 'greek yogurt', 'berries', 'nuts'],
        'Kids': ['strawberry', 'vanilla', 'colorful sprinkles', 'mild chocolate']
    }
    
    if market_ctx.target_segment in segment_ingredients:
        base_ingredients.extend(segment_ingredients[market_ctx.target_segment])
    
    # Add trend-boosted ingredients if trend strength is high
    if trend_strength > 0.7:
        trending_boosters = ['viral', 'trending', 'instagram-worthy', 'aesthetic']
        base_ingredients.extend(trending_boosters)
    
    return list(set(base_ingredients))  # Remove duplicates

# Additional missing helper functions
def _analyze_price_elasticity(market_ctx) -> float:
    """Analyze price elasticity for market context"""
    sensitivity_scores = {
        'thấp': 0.3,  # Low sensitivity = high elasticity
        'trung bình': 0.6,
        'cao': 0.9   # High sensitivity = low elasticity
    }
    return sensitivity_scores.get(market_ctx.price_sensitivity, 0.6)

def _get_channel_preferences(segment: str) -> List[str]:
    """Get preferred channels for segment"""
    
    channel_mapping = {
        'gen_z': ['Instagram', 'TikTok', 'Grab Food', 'Online delivery'],
        'millennials': ['Facebook', 'Website', 'Delivery apps', 'Email'],
        'gym': ['Fitness apps', 'Instagram', 'Health websites', 'Gym partnerships'],
        'kids': ['Facebook (parents)', 'Local stores', 'School networks', 'Family referrals'],
        'health': ['Health food stores', 'Organic shops', 'Wellness websites', 'Instagram']
    }
    
    return channel_mapping.get(segment.lower(), ['Online', 'Social media', 'Local stores'])

def _identify_buying_triggers(market_ctx, seasonal_ctx) -> List[str]:
    """Identify buying triggers for market context"""
    
    triggers = []
    
    # Seasonal triggers
    if seasonal_ctx.events:
        triggers.extend([f"Upcoming {event}" for event in seasonal_ctx.events])
    
    # Segment-specific triggers
    if 'gen' in market_ctx.target_segment.lower():
        triggers.extend(['Viral trends', 'FOMO', 'Social media posts', 'Peer influence'])
    elif 'gym' in market_ctx.target_segment.lower():
        triggers.extend(['Fitness goals', 'Cheat day', 'Pre/post workout', 'Health benefits'])
    elif 'kids' in market_ctx.target_segment.lower():
        triggers.extend(['Birthday parties', 'School events', 'Achievements', 'Special occasions'])
    
    # Price sensitivity triggers
    if market_ctx.price_sensitivity == 'cao':
        triggers.extend(['Discounts', 'Promotions', 'Bundle deals', 'Limited time offers'])
    
    return triggers

# Monkey patch the method to context service
setattr(ContextAwareRecipeService, '_get_recommended_ingredients', _get_recommended_ingredients)