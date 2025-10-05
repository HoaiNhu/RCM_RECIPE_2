# run_and_test_final.py
import subprocess
import time
import requests
import json
import sys
from pathlib import Path

def main():
    print("Starting RCM_RECIPE_2 Server...")
    
    # Start server
    process = subprocess.Popen([
        sys.executable, "start_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(20)
    
    # Test both APIs
    print("Testing generate-from-ingredients API...")
    url1 = "http://localhost:8000/api/v1/recipes/generate-from-ingredients"
    payload1 = {
        "ingredients": "bột mì, đường, trứng, bơ, bột matcha",
        "language": "vi"
    }
    
    try:
        response1 = requests.post(url1, json=payload1, timeout=60)
        print(f"Status Code: {response1.status_code}")
        data1 = response1.json()
        print(f"Title: {data1['data']['title']}")
        print(f"Ingredients: {len(data1['data']['ingredients'])} items")
        print(f"Instructions: {len(data1['data']['instructions'])} steps")
        print()
    except Exception as e:
        print(f"Error: {e}")
    
    print("Testing generate-from-trend API...")
    url2 = "http://localhost:8000/api/v1/recipes/generate-from-trend"
    payload2 = {
        "trend": "labubu valentine matcha",
        "user_segment": "genz",
        "occasion": "valentine",
        "language": "vi"
    }
    
    try:
        response2 = requests.post(url2, json=payload2, timeout=60)
        print(f"Status Code: {response2.status_code}")
        data2 = response2.json()
        print(f"Title: {data2['data']['title']}")
        print(f"Ingredients: {len(data2['data']['ingredients'])} items")
        print(f"Instructions: {len(data2['data']['instructions'])} steps")
        print()
    except Exception as e:
        print(f"Error: {e}")
    
    # Stop server
    print("Stopping server...")
    process.terminate()

if __name__ == "__main__":
    main()