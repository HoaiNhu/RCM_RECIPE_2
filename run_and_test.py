# run_and_test.py
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
        sys.executable, "run_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(15)
    
    # Test API
    print("Testing API...")
    url = "http://localhost:8000/api/v1/recipes/generate-from-trend"
    payload = {
        "trend": "labubu valentine matcha",
        "user_segment": "genz",
        "occasion": "hallowen", 
        "language": "vi"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Stop server
    print("Stopping server...")
    process.terminate()

if __name__ == "__main__":
    main()
