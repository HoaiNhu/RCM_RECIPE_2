# test_api_simple.py
import requests
import json

def test_api():
    url = "http://localhost:8000/api/v1/recipes/generate-from-trend"
    payload = {
        "trend": "labubu valentine matcha",
        "user_segment": "genz",
        "occasion": "hallowen",
        "language": "vi"
    }
    
    try:
        print("Testing API...")
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
