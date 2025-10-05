#!/usr/bin/env python3
"""
Enhanced Trend Prediction với improved thresholds và logic
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

class EnhancedTrendCalculator:
    """Improved trend calculation với seasonal và segment boosts"""
    
    def __init__(self):
        self.load_thresholds()
    
    def load_thresholds(self):
        """Load threshold config"""
        try:
            with open("configs/trend_thresholds.json", 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default enhanced config
            self.config = {
                "seasonal_boost": {
                    "halloween": 0.3,
                    "christmas": 0.4, 
                    "valentine": 0.25,
                    "summer": 0.2,
                    "back_to_school": 0.15,
                    "tet": 0.35,
                    "spring": 0.1,
                    "autumn": 0.15,
                    "winter": 0.2
                },
                "base_threshold": 0.35,  # Lowered từ 0.7
                "viral_threshold": 0.75,
                "trend_multipliers": {
                    "gen_z": 1.3,
                    "millennials": 1.15,
                    "gen_x": 0.95,
                    "baby_boomers": 0.8,
                    "kids": 1.1,
                    "teenagers": 1.25,
                    "young_adults": 1.2,
                    "office_workers": 1.0,
                    "gym_goers": 0.9,
                    "health_conscious": 0.85
                },
                "event_boosts": {
                    "halloween": 0.4,
                    "christmas": 0.5,
                    "valentine": 0.3,
                    "tet": 0.45,
                    "birthday": 0.2,
                    "wedding": 0.25,
                    "graduation": 0.2
                }
            }
    
    def calculate_enhanced_trend_strength(self, 
                                        base_predictions: Dict[str, float],
                                        seasonal_context: Dict[str, Any],
                                        user_segment: str,
                                        events: List[str] = None) -> float:
        """Calculate enhanced trend strength với multiple boosts"""
        
        # Base calculation
        popularity = base_predictions.get('popularity', 0.5)
        engagement = base_predictions.get('engagement', 0.5) 
        trend_score = base_predictions.get('trend_score', 0.5)
        
        # Base weighted score
        base_strength = (
            popularity * 0.4 +
            engagement * 0.3 +
            trend_score * 0.3
        )
        
        # Apply seasonal boost
        seasonal_boost = self._get_seasonal_boost(
            seasonal_context.get('season', ''),
            seasonal_context.get('month', 1)
        )
        
        # Apply segment multiplier
        segment_multiplier = self.config['trend_multipliers'].get(
            user_segment.lower(), 1.0
        )
        
        # Apply event boosts
        event_boost = self._get_event_boost(events or [])
        
        # Enhanced calculation
        enhanced_strength = base_strength * segment_multiplier * (1 + seasonal_boost + event_boost)
        
        # Cap tại 1.0
        return min(enhanced_strength, 1.0)
    
    def _get_seasonal_boost(self, season: str, month: int) -> float:
        """Get seasonal boost based on season và month"""
        
        season_lower = season.lower()
        boost = 0.0
        
        # Season-based boost
        if season_lower in self.config['seasonal_boost']:
            boost += self.config['seasonal_boost'][season_lower]
        
        # Month-specific boosts
        month_boosts = {
            10: 0.3,  # October - Halloween
            12: 0.4,  # December - Christmas
            2: 0.25,  # February - Valentine 
            1: 0.35,  # January - Tết (lunar calendar varies)
            6: 0.2,   # June - Summer start
            7: 0.2,   # July - Summer peak
            8: 0.15,  # August - Summer end
            9: 0.15   # September - Back to school
        }
        
        boost += month_boosts.get(month, 0.0)
        
        return boost
    
    def _get_event_boost(self, events: List[str]) -> float:
        """Get boost từ specific events"""
        
        total_boost = 0.0
        
        for event in events:
            event_lower = event.lower()
            for key, boost in self.config['event_boosts'].items():
                if key in event_lower:
                    total_boost += boost
                    break  # Chỉ apply 1 boost per event
        
        return total_boost
    
    def is_trending(self, trend_strength: float) -> bool:
        """Check if trend strength đủ high để generate recipe"""
        return trend_strength >= self.config['base_threshold']
    
    def is_viral_potential(self, trend_strength: float) -> bool:
        """Check if có viral potential"""
        return trend_strength >= self.config['viral_threshold']
    
    def get_trend_level(self, trend_strength: float) -> str:
        """Get descriptive trend level"""
        
        if trend_strength >= 0.9:
            return "Cực kỳ viral"
        elif trend_strength >= 0.75:
            return "Viral cao"
        elif trend_strength >= 0.6:
            return "Trending mạnh"
        elif trend_strength >= 0.45:
            return "Trending vừa"
        elif trend_strength >= 0.35:
            return "Có tiềm năng"
        else:
            return "Yếu"

def test_enhanced_calculator():
    """Test enhanced calculator với different scenarios"""
    
    print("🧪 Testing Enhanced Trend Calculator")
    print("=" * 50)
    
    calculator = EnhancedTrendCalculator()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Halloween Gen Z",
            "predictions": {"popularity": 0.6, "engagement": 0.7, "trend_score": 0.5},
            "seasonal": {"season": "autumn", "month": 10},
            "segment": "gen_z",
            "events": ["halloween", "october"]
        },
        {
            "name": "Christmas Millennials", 
            "predictions": {"popularity": 0.55, "engagement": 0.6, "trend_score": 0.45},
            "seasonal": {"season": "winter", "month": 12},
            "segment": "millennials",
            "events": ["christmas"]
        },
        {
            "name": "Summer Kids",
            "predictions": {"popularity": 0.5, "engagement": 0.55, "trend_score": 0.4},
            "seasonal": {"season": "summer", "month": 7},
            "segment": "kids", 
            "events": ["summer vacation"]
        },
        {
            "name": "Valentine Young Adults",
            "predictions": {"popularity": 0.65, "engagement": 0.8, "trend_score": 0.6},
            "seasonal": {"season": "winter", "month": 2},
            "segment": "young_adults",
            "events": ["valentine"]
        }
    ]
    
    for scenario in scenarios:
        strength = calculator.calculate_enhanced_trend_strength(
            scenario["predictions"],
            scenario["seasonal"], 
            scenario["segment"],
            scenario["events"]
        )
        
        level = calculator.get_trend_level(strength)
        trending = "✅" if calculator.is_trending(strength) else "❌"
        viral = "🔥" if calculator.is_viral_potential(strength) else ""
        
        print(f"\n{scenario['name']}:")
        print(f"   Strength: {strength:.3f} | Level: {level} {trending} {viral}")

if __name__ == "__main__":
    # Save enhanced config
    os.makedirs("configs", exist_ok=True)
    
    calculator = EnhancedTrendCalculator()
    with open("configs/trend_thresholds.json", 'w', encoding='utf-8') as f:
        json.dump(calculator.config, f, indent=2, ensure_ascii=False)
    
    print("✅ Enhanced config saved!")
    
    # Test calculator
    test_enhanced_calculator()