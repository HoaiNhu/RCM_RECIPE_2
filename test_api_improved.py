import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test generate-from-trend API
    print("=" * 50)
    print("Testing generate-from-trend API")
    print("=" * 50)
    
    trend_data = {
        "trend": "labubu valentine matcha",
        "user_segment": "genz",
        "occasion": "valentine",
        "language": "vi"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/recipes/generate-from-trend", json=trend_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("Testing generate-from-ingredients API")
    print("=" * 50)
    
    ingredients_data = {
        "ingredients": "bột mì, đường, trứng, bơ, bột matcha",
        "language": "vi"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/recipes/generate-from-ingredients", json=ingredients_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
