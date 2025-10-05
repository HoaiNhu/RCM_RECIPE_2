#!/usr/bin/env python3
"""
Tối ưu hóa ML models để cải thiện trend prediction accuracy
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from infrastructure.ml_models.trend_predictor import TrendPredictor
import joblib
import os

def optimize_trend_models():
    """Fine-tune hyperparameters cho better predictions"""
    
    print("🔧 Optimizing ML Models for Better Trend Prediction")
    print("=" * 60)
    
    # Load predictor
    predictor = TrendPredictor()
    
    try:
        # Load data
        print("📊 Loading training data...")
        X, y = predictor._prepare_training_data()
        print(f"   Training samples: {len(X)}")
        print(f"   Features: {len(X.columns)}")
        
        # Optimize RandomForest
        print("\n🌲 Optimizing RandomForest...")
        rf_params = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        from sklearn.ensemble import RandomForestRegressor
        rf_grid = GridSearchCV(
            RandomForestRegressor(random_state=42),
            rf_params,
            cv=5,
            scoring='r2',
            n_jobs=-1,
            verbose=1
        )
        
        # Train for popularity
        print("   Training for popularity prediction...")
        rf_grid.fit(X, y['popularity'])
        
        print(f"   Best params: {rf_grid.best_params_}")
        print(f"   Best score: {rf_grid.best_score_:.4f}")
        
        # Save optimized model
        models_dir = "data/models"
        os.makedirs(models_dir, exist_ok=True)
        
        joblib.dump(rf_grid.best_estimator_, f"{models_dir}/optimized_rf_popularity.pkl")
        
        # Test predictions với optimized model
        print("\n🧪 Testing optimized predictions...")
        
        # Test scenarios
        test_scenarios = [
            {"month": 12, "day_of_year": 360, "weekday": 5, "name": "Christmas"},
            {"month": 6, "day_of_year": 180, "weekday": 2, "name": "Summer"},
            {"month": 9, "day_of_year": 250, "weekday": 1, "name": "Back to School"},
            {"month": 10, "day_of_year": 304, "weekday": 4, "name": "Halloween"}
        ]
        
        for scenario in test_scenarios:
            # Create test data
            test_data = pd.DataFrame([{
                'month': scenario['month'],
                'day_of_year': scenario['day_of_year'], 
                'weekday': scenario['weekday'],
                'luot_xem': 100000,  # Average views
                'luot_thich': 5000,  # Average likes
                'luot_comment': 500, # Average comments
                'thoi_luong_video': 300, # 5 minutes
                'so_tu_khoa': 5,
                'do_tuoi_trung_binh': 25,
                'ti_le_nu': 0.6,
                'muc_luong_trung_binh': 15000000,
                'chi_tieu_hang_thang': 3000000
            }])
            
            # Align với training features
            for col in X.columns:
                if col not in test_data.columns:
                    test_data[col] = 0
            
            test_data = test_data[X.columns]
            
            # Predict
            prediction = rf_grid.best_estimator_.predict(test_data)[0]
            
            print(f"   {scenario['name']}: {prediction:.3f}")
        
        print("\n✅ Model optimization completed!")
        print(f"📁 Optimized model saved to: {models_dir}/optimized_rf_popularity.pkl")
        
        return True
        
    except Exception as e:
        print(f"❌ Optimization error: {e}")
        return False

def update_trend_thresholds():
    """Cập nhật thresholds cho better trend classification"""
    
    print("\n🎯 Updating Trend Classification Thresholds")
    print("=" * 50)
    
    # Định nghĩa thresholds mới dựa trên seasonal patterns
    new_thresholds = {
        "seasonal_boost": {
            "halloween": 0.3,      # October boost
            "christmas": 0.4,      # December boost  
            "valentine": 0.25,     # February boost
            "summer": 0.2,         # June-August boost
            "back_to_school": 0.15 # September boost
        },
        "base_threshold": 0.4,     # Lower từ 0.7 xuống 0.4
        "viral_threshold": 0.8,    # High viral potential
        "trend_multipliers": {
            "gen_z": 1.2,         # Gen Z trends mạnh hơn
            "millennials": 1.1,    # Millennials decent
            "gen_x": 0.9,         # Gen X ít viral hơn
            "baby_boomers": 0.7    # Boomers ít trend
        }
    }
    
    # Save config
    import json
    config_path = "configs/trend_thresholds.json"
    os.makedirs("configs", exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(new_thresholds, f, indent=2, ensure_ascii=False)
    
    print(f"✅ New thresholds saved to: {config_path}")
    print("📋 Key improvements:")
    print(f"   - Lowered base threshold: 0.7 → 0.4")
    print(f"   - Added seasonal boosts: Halloween +0.3, Christmas +0.4") 
    print(f"   - Added segment multipliers: Gen Z +20%")
    
    return new_thresholds

if __name__ == "__main__":
    print("🚀 Starting Model Optimization Process")
    print("=" * 60)
    
    # Step 1: Optimize models
    success = optimize_trend_models()
    
    if success:
        # Step 2: Update thresholds
        thresholds = update_trend_thresholds()
        
        print("\n🎉 Optimization Complete!")
        print("💡 Next steps:")
        print("   1. Update TrendPredictor to use new thresholds")
        print("   2. Test with optimized models")
        print("   3. Re-run API tests to see improvements")
    else:
        print("\n❌ Optimization failed - check errors above")