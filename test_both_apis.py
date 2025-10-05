# test_both_apis.py
import requests
import json

def test_ingredients_api():
    print("Testing generate-from-ingredients API...")
    url = "http://localhost:8000/api/v1/recipes/generate-from-ingredients"
    payload = {
        "ingredients": "bột mì, đường, trứng, bơ, bột matcha",
        "language": "vi"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Title: {data['data']['title']}")
        print(f"Ingredients: {len(data['data']['ingredients'])} items")
        print(f"Instructions: {len(data['data']['instructions'])} steps")
        print()
    except Exception as e:
        print(f"Error: {e}")

def test_trend_api():
    print("Testing generate-from-trend API...")
    url = "http://localhost:8000/api/v1/recipes/generate-from-trend"
    payload = {
        "trend": "labubu valentine matcha",
        "user_segment": "genz",
        "occasion": "valentine",
        "language": "vi"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Title: {data['data']['title']}")
        print(f"Ingredients: {len(data['data']['ingredients'])} items")
        print(f"Instructions: {len(data['data']['instructions'])} steps")
        print()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ingredients_api()
    test_trend_api()

