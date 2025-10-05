#!/usr/bin/env python3
"""
Test script for RCM_RECIPE_2 Analytics API

Tests all the new analytics endpoints with realistic scenarios
"""

import requests
import json
from datetime import datetime, timedelta
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_analytics_api():
    """Test all analytics endpoints"""
    
    print("🧪 Testing RCM_RECIPE_2 Analytics API")
    print("=" * 50)
    
    # Test 1: Predict Halloween trends
    print("\n1️⃣ Testing Halloween Trend Prediction...")
    halloween_request = {
        "target_date": "2025-10-31",
        "user_segment": "gen_z",
        "location": "vietnam",
        "custom_context": {
            "event_boost": 0.2,
            "spooky_factor": 0.8
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analytics/predict-trends", json=halloween_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Halloween prediction successful!")
            print(f"   Overall trend strength: {data['predictions']['overall_trend_strength']:.3f}")
            print(f"   Recommended ingredients: {', '.join(data['recommended_ingredients'][:3])}")
            print(f"   Trending flavors: {', '.join(data['trending_flavors'][:3])}")
        else:
            print(f"❌ Halloween prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Halloween prediction error: {e}")
    
    # Test 2: Generate smart recipe for Gen Z
    print("\n2️⃣ Testing Smart Recipe Generation for Gen Z...")
    recipe_request = {
        "user_segment": "gen_z",
        "target_date": "2025-10-31",
        "trend_keywords": ["halloween", "spooky", "orange", "aesthetic"],
        "include_market_analysis": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analytics/generate-smart-recipe", json=recipe_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Smart recipe generation successful!")
            print(f"   Recipe title: {data['recipe']['title']}")
            print(f"   Viral potential: {data['viral_potential_score']:.3f}")
            print(f"   Success factors: {len(data['success_factors'])} identified")
            print(f"   Market opportunity: {data['market_insights'].get('growth_potential', 'N/A')}")
        else:
            print(f"❌ Smart recipe generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Smart recipe generation error: {e}")
    
    # Test 3: Market insights for Gym segment
    print("\n3️⃣ Testing Market Insights for Gym Segment...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/market-insights/gym?target_date=2025-11-01&include_competition=true")
        if response.status_code == 200:
            data = response.json()
            print("✅ Market insights successful!")
            print(f"   Opportunity score: {data['opportunity_score']:.3f}")
            print(f"   Recommended strategies: {len(data['recommended_strategies'])}")
            print(f"   Competition level: {data['segment_analysis']['profile']['competition_level']:.2f}")
        else:
            print(f"❌ Market insights failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Market insights error: {e}")
    
    # Test 4: Current trending analysis
    print("\n4️⃣ Testing Current Trending Analysis...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/trending-now")
        if response.status_code == 200:
            data = response.json()
            print("✅ Trending analysis successful!")
            print(f"   Current season: {data['data']['current_season']}")
            print(f"   Hot events: {', '.join(data['data']['hot_events'][:3])}")
            print(f"   Viral keywords: {', '.join(data['data']['viral_keywords'][:5])}")
            print(f"   Opportunity score: {data['data']['opportunity_score']:.3f}")
        else:
            print(f"❌ Trending analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Trending analysis error: {e}")
    
    # Test 5: Segment recommendations for Kids
    print("\n5️⃣ Testing Segment Recommendations for Kids...")
    try:
        response = requests.get(f"{BASE_URL}/analytics/segment-recommendations/kids")
        if response.status_code == 200:
            data = response.json()
            print("✅ Segment recommendations successful!")
            print(f"   Market potential: {data['data']['segment_profile']['market_potential']:.2f}")
            print(f"   Recommended products: {', '.join(data['data']['recommended_products'][:3])}")
            print(f"   Pricing strategy: {data['data']['pricing_strategy']['strategy']}")
        else:
            print(f"❌ Segment recommendations failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Segment recommendations error: {e}")
    
    # Test 6: Valentine's Day prediction (future)
    print("\n6️⃣ Testing Valentine's Day Prediction...")
    valentine_request = {
        "target_date": "2026-02-14",
        "user_segment": "millennials",
        "location": "vietnam",
        "custom_context": {
            "romantic_factor": 0.9,
            "gift_season": True
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analytics/predict-trends", json=valentine_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Valentine prediction successful!")
            print(f"   Popularity score: {data['predictions']['popularity_score']:.3f}")
            print(f"   Engagement score: {data['predictions']['engagement_score']:.3f}")
            print(f"   Market potential: {data['market_context']['market_potential']:.2f}")
        else:
            print(f"❌ Valentine prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Valentine prediction error: {e}")
    
    print("\n🎉 Analytics API Testing Completed!")
    print("=" * 50)

def test_existing_apis():
    """Test existing recipe APIs to ensure they still work"""
    
    print("\n🔄 Testing Existing Recipe APIs...")
    
    # Test ingredients-based recipe
    print("\n📝 Testing ingredients-based recipe generation...")
    ingredients_request = {
        "ingredients": "bột mì, trứng, đường, bơ, chocolate, pumpkin",
        "language": "vi"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recipes/generate-from-ingredients", json=ingredients_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Ingredients-based recipe successful!")
            print(f"   Recipe title: {data['data']['title']}")
        else:
            print(f"❌ Ingredients-based recipe failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Ingredients-based recipe error: {e}")
    
    # Test trend-based recipe
    print("\n🔥 Testing trend-based recipe generation...")
    trend_request = {
        "trend": "halloween spooky matcha",
        "user_segment": "gen_z",
        "occasion": "halloween party",
        "language": "vi"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recipes/generate-from-trend", json=trend_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Trend-based recipe successful!")
            print(f"   Recipe title: {data['data']['title']}")
        else:
            print(f"❌ Trend-based recipe failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Trend-based recipe error: {e}")

def comprehensive_scenario_tests():
    """Test comprehensive real-world scenarios"""
    
    print("\n🌟 Comprehensive Scenario Testing")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "Christmas Marketing Campaign",
            "segment": "millennials",
            "date": "2025-12-20",
            "context": {"gift_season": True, "family_gathering": 0.8}
        },
        {
            "name": "Summer Fitness Trend",
            "segment": "gym",
            "date": "2025-07-15",
            "context": {"summer_boost": 0.7, "health_focus": 0.9}
        },
        {
            "name": "Back to School",
            "segment": "kids",
            "date": "2025-09-01",
            "context": {"school_season": True, "energy_need": 0.8}
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}️⃣ Testing {scenario['name']}...")
        
        # Predict trends for scenario
        trend_request = {
            "target_date": scenario["date"],
            "user_segment": scenario["segment"],
            "custom_context": scenario["context"]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/analytics/predict-trends", json=trend_request)
            if response.status_code == 200:
                data = response.json()
                trend_strength = data['predictions']['overall_trend_strength']
                print(f"   Trend strength: {trend_strength:.3f}")
                
                # Generate recipe if trend is promising
                if trend_strength > 0.6:
                    recipe_request = {
                        "user_segment": scenario["segment"],
                        "target_date": scenario["date"],
                        "include_market_analysis": True
                    }
                    
                    recipe_response = requests.post(f"{BASE_URL}/analytics/generate-smart-recipe", json=recipe_request)
                    if recipe_response.status_code == 200:
                        recipe_data = recipe_response.json()
                        print(f"   ✅ Generated: {recipe_data['recipe']['title']}")
                        print(f"   Viral potential: {recipe_data['viral_potential_score']:.3f}")
                    else:
                        print("   ⚠️ Recipe generation failed")
                else:
                    print("   ⚠️ Low trend strength - skipping recipe generation")
            else:
                print(f"   ❌ Trend prediction failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Scenario test error: {e}")

def main():
    """Main test function"""
    
    print("🚀 Starting RCM_RECIPE_2 API Testing Suite")
    print(f"Testing against: {BASE_URL}")
    print(f"Test started at: {datetime.now()}")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        if response.status_code != 200:
            print("❌ Server health check failed!")
            print("Make sure the server is running with: python run_server.py")
            return
        print("✅ Server is running!")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running with: python run_server.py")
        return
    
    # Run all tests
    test_analytics_api()
    test_existing_apis()
    comprehensive_scenario_tests()
    
    print(f"\n🎉 All tests completed at: {datetime.now()}")
    print("📊 Check the results above for any issues.")

if __name__ == "__main__":
    main()