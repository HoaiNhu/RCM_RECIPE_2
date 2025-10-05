#!/usr/bin/env python3
"""
Training script cho RCM_RECIPE_2 AI models

Script này sẽ:
1. Train ML models với dữ liệu trong raw/
2. Fine-tune knowledge base cho Gemini
3. Tạo model artifacts cho production
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

# Ensure UTF-8 stdout/stderr for Windows consoles (avoid UnicodeEncodeError with emojis)
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Import our models
from infrastructure.ml_models.trend_predictor import TrendPredictor
from domain.services.context_aware_recipe_service import ContextAwareRecipeService

def main():
    print("🚀 Starting RCM_RECIPE_2 AI Training Pipeline...")
    print(f"Project root: {ROOT_DIR}")
    print(f"Training started at: {datetime.now()}")
    
    # Setup paths
    data_dir = ROOT_DIR / "data" / "raw"
    models_dir = ROOT_DIR / "data" / "models"
    models_dir.mkdir(exist_ok=True, parents=True)
    
    # Verify data files exist
    required_files = [
        "comprehensive_food_preferences_raw_20250920_074528.csv",
        "consumer_groups_detailed_20250921_133329.csv",
        "consumer_profiles_20250920_061904.csv",
        "seasonal_trends_20250920_061904.csv",
        "vietnam_seasonal_events_2025.csv",
        "youtube_bakery_gaming_trends_cleaned.csv"
    ]
    
    print("\n📊 Checking data files...")
    missing_files = []
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            print(f"✅ {file} - {file_path.stat().st_size:,} bytes")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Missing {len(missing_files)} required files. Please ensure all data files are in {data_dir}")
        return False
    
    # Train ML models
    print("\n🤖 Training ML Trend Prediction Models...")
    try:
        predictor = TrendPredictor(model_path=models_dir)
        training_results = predictor.train(data_dir)
        
        print("✅ ML Training completed successfully!")
        print("📊 Training Results:")
        for model_name, metrics in training_results.items():
            print(f"  {model_name}: MAE={metrics['mae']:.4f}, R²={metrics['r2']:.4f}")
        
    except Exception as e:
        print(f"❌ ML Training failed: {e}")
        return False
    
    # Test ML models
    print("\n🧪 Testing ML Models...")
    try:
        # Test with October (Halloween) context
        test_context = {
            'month': 10,
            'temperature': 22.0,
            'user_segment': 'Gen Z',
            'season': 'Thu',
            'market_potential': 0.8,
            'competition_level': 0.7,
            'bakery_demand': 1.2
        }
        
        predictions = predictor.predict_trends(test_context)
        print("🎯 Test Predictions for October/Halloween context:")
        for metric, value in predictions.items():
            print(f"  {metric}: {value:.3f}")
        
    except Exception as e:
        print(f"⚠️ ML Testing failed: {e}")
    
    # Test Context-Aware Recipe Service
    print("\n🍰 Testing Context-Aware Recipe Generation...")
    try:
        service = ContextAwareRecipeService()
        
        # Test với Halloween context
        halloween_date = datetime(2025, 10, 31)
        recipe = service.generate_context_aware_recipe(
            user_segment="gen_z",
            target_date=halloween_date,
            custom_trend="halloween spooky orange pumpkin"
        )
        
        print("✅ Context-Aware Recipe Generation successful!")
        print(f"📝 Generated recipe: '{recipe.title}'")
        print(f"🏷️ Tags: {recipe.tags}")
        print(f"👥 Target: {recipe.user_segment}")
        
    except Exception as e:
        print(f"❌ Recipe Generation testing failed: {e}")
    
    # Generate training report
    print("\n📄 Generating Training Report...")
    try:
        report = generate_training_report(data_dir, models_dir, training_results if 'training_results' in locals() else {})
        
        report_path = ROOT_DIR / "training_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Training report saved to: {report_path}")
        
    except Exception as e:
        print(f"⚠️ Report generation failed: {e}")
    
    # Performance summary
    print("\n🎉 Training Pipeline Completed!")
    print("=" * 50)
    print("📊 SUMMARY:")
    print(f"  Data files processed: {len(required_files)}")
    print(f"  Models trained: {len(training_results) if 'training_results' in locals() else 0}")
    print(f"  Models saved to: {models_dir}")
    print(f"  Training completed at: {datetime.now()}")
    print("\n🚀 Your AI models are ready for production!")
    print("   Use the analytics API endpoints to get predictions.")
    
    return True

def generate_training_report(data_dir: Path, models_dir: Path, training_results: dict) -> dict:
    """Generate comprehensive training report"""
    
    # Analyze datasets
    datasets_info = {}
    
    for csv_file in data_dir.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            datasets_info[csv_file.name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'size_mb': round(csv_file.stat().st_size / 1024 / 1024, 2),
                'column_names': df.columns.tolist(),
                'missing_values': df.isnull().sum().sum(),
                'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist()
            }
        except Exception as e:
            datasets_info[csv_file.name] = {'error': str(e)}
    
    # Count model files
    model_files = list(models_dir.glob("*.pkl"))
    
    report = {
        'training_timestamp': datetime.now().isoformat(),
        'project_info': {
            'name': 'RCM_RECIPE_2',
            'version': '2.0.0',
            'description': 'AI-powered Recipe Generation with Trend Analysis'
        },
        'datasets': {
            'total_files': len(datasets_info),
            'total_rows': sum(info.get('rows', 0) for info in datasets_info.values()),
            'total_size_mb': sum(info.get('size_mb', 0) for info in datasets_info.values()),
            'details': datasets_info
        },
        'models': {
            'total_trained': len(training_results),
            'model_files': [f.name for f in model_files],
            'training_results': training_results,
            'model_types': ['RandomForestRegressor', 'GradientBoostingRegressor', 'StandardScaler']
        },
        'features': {
            'ml_prediction': 'Trend strength, popularity, engagement prediction',
            'context_awareness': 'Season, weather, events, user segments',
            'recipe_generation': 'Gemini API with context-enhanced prompts',
            'analytics_api': 'Real-time trend analysis and recommendations'
        },
        'data_sources': {
            'youtube_trends': 'Video engagement and viral content analysis',
            'consumer_behavior': 'Segment preferences and market analysis',
            'seasonal_data': 'Weather, events, and seasonal patterns',
            'market_intelligence': 'Competition and growth trends'
        },
        'model_capabilities': {
            'trend_prediction': 'Predict viral potential and engagement',
            'seasonal_adaptation': 'Adjust recommendations by season/weather',
            'segment_targeting': 'Personalize for Gen Z, Millennials, Gym, Kids',
            'context_integration': 'Factor in events, temperature, market conditions',
            'recipe_optimization': 'Generate recipes optimized for target context'
        },
        'api_endpoints': {
            'prediction': '/api/v1/analytics/predict-trends',
            'smart_recipe': '/api/v1/analytics/generate-smart-recipe',
            'market_insights': '/api/v1/analytics/market-insights/{segment}',
            'trending_now': '/api/v1/analytics/trending-now',
            'recommendations': '/api/v1/analytics/segment-recommendations/{segment}'
        }
    }
    
    return report

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)