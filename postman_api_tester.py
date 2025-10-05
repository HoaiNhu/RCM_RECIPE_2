#!/usr/bin/env python3
"""
Automated Postman Collection Runner cho RCM_RECIPE_2 Analytics API
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class AnalyticsAPITester:
    """Comprehensive API tester cho analytics endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def test_endpoint(self, name: str, method: str, url: str, 
                     data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """Test single endpoint với comprehensive validation"""
        
        print(f"\n🧪 Testing: {name}")
        print(f"   URL: {method} {url}")
        
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # ms
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"error": "Invalid JSON response"}
            
            # Validation
            result = {
                "name": name,
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "success": response.status_code == 200,
                "response_size_bytes": len(response.content),
                "response_data": response_data,
                "timestamp": datetime.now().isoformat()
            }
            
            # Status display
            status = "✅" if result["success"] else "❌"
            print(f"   Status: {status} {response.status_code}")
            print(f"   Response time: {response_time:.0f}ms")
            
            if result["success"]:
                print(f"   Response size: {len(response.content)} bytes")
                # Show key data points
                if isinstance(response_data, dict):
                    if "data" in response_data:
                        data_keys = list(response_data["data"].keys())[:3]
                        print(f"   Key fields: {', '.join(data_keys)}")
            else:
                print(f"   Error: {response_data}")
                
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                "name": name,
                "method": method,
                "url": url,
                "status_code": 0,
                "response_time_ms": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            print(f"   ❌ Exception: {e}")
            self.results.append(error_result)
            return error_result
    
    def run_comprehensive_tests(self):
        """Chạy toàn bộ test suite"""
        
        print("🚀 Starting Comprehensive Analytics API Testing")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"Started at: {datetime.now()}")
        
        # Test cases
        test_cases = [
            # Health checks
            {
                "name": "Health Check",
                "method": "GET",
                "url": f"{self.base_url}/health"
            },
            {
                "name": "API Root Info",
                "method": "GET", 
                "url": f"{self.base_url}/"
            },
            
            # Analytics endpoints
            {
                "name": "Halloween Trend Prediction",
                "method": "POST",
                "url": f"{self.base_url}/api/v1/analytics/predict-trends",
                "data": {
                    "target_date": "2025-10-31",
                    "user_segment": "gen_z",
                    "include_seasonal_factors": True
                }
            },
            {
                "name": "Christmas Trend Prediction", 
                "method": "POST",
                "url": f"{self.base_url}/api/v1/analytics/predict-trends",
                "data": {
                    "target_date": "2025-12-25",
                    "user_segment": "millennials"
                }
            },
            {
                "name": "Smart Halloween Recipe Generation",
                "method": "POST",
                "url": f"{self.base_url}/api/v1/analytics/generate-smart-recipe",
                "data": {
                    "user_segment": "gen_z",
                    "target_date": "2025-10-31",
                    "trend_keywords": ["halloween", "pumpkin", "spooky"],
                    "include_market_analysis": True
                }
            },
            {
                "name": "Valentine Recipe Generation",
                "method": "POST",
                "url": f"{self.base_url}/api/v1/analytics/generate-smart-recipe",
                "data": {
                    "user_segment": "young_adults",
                    "target_date": "2025-02-14",
                    "trend_keywords": ["valentine", "romantic", "heart"]
                }
            },
            {
                "name": "Market Insights - Gym Segment",
                "method": "GET",
                "url": f"{self.base_url}/api/v1/analytics/market-insights/gym",
                "params": {
                    "target_date": "2025-11-01",
                    "include_competition": "true"
                }
            },
            {
                "name": "Current Trending Analysis",
                "method": "GET",
                "url": f"{self.base_url}/api/v1/analytics/trending-now"
            },
            {
                "name": "Kids Segment Recommendations",
                "method": "GET",
                "url": f"{self.base_url}/api/v1/analytics/segment-recommendations/kids"
            },
            {
                "name": "Gen Z Segment Recommendations",
                "method": "GET", 
                "url": f"{self.base_url}/api/v1/analytics/segment-recommendations/gen_z"
            },
            
            # Existing recipe APIs
            {
                "name": "Recipe from Ingredients",
                "method": "POST",
                "url": f"{self.base_url}/api/v1/recipes/generate-from-ingredients",
                "data": {
                    "ingredients": ["pumpkin", "chocolate", "cinnamon"],
                    "user_segment": "gen_z",
                    "language": "vi"
                }
            },
            {
                "name": "Recipe from Trend",
                "method": "POST",
                "url": f"{self.base_url}/api/v1/recipes/generate-from-trend",
                "data": {
                    "trend": "halloween spooky korean style",
                    "user_segment": "gen_z",
                    "occasion": "halloween",
                    "language": "vi"
                }
            }
        ]
        
        # Run tests
        for test_case in test_cases:
            self.test_endpoint(
                test_case["name"],
                test_case["method"],
                test_case["url"],
                test_case.get("data"),
                test_case.get("params")
            )
            time.sleep(0.5)  # Rate limiting
        
        # Summary
        self.print_summary()
        
    def print_summary(self):
        """In tổng kết results"""
        
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if successful_tests > 0:
            response_times = [r["response_time_ms"] for r in self.results if r["success"]]
            avg_response_time = sum(response_times) / len(response_times)
            print(f"Avg Response Time: {avg_response_time:.0f}ms")
        
        # Failed tests detail
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"   • {result['name']}: {result.get('error', 'HTTP ' + str(result['status_code']))}")
        
        # Save results
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Results saved to: test_results.json")

def main():
    """Main test runner"""
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not running or not healthy!")
            print("   Please start server first: python run_server.py")
            return
    except:
        print("❌ Cannot connect to server!")
        print("   Please start server first: python run_server.py")
        return
    
    # Run tests
    tester = AnalyticsAPITester()
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()