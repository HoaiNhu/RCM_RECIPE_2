# start_and_test.py
import subprocess
import time
import requests
import json
import sys
from pathlib import Path

def start_server():
    """Start the server in background"""
    print("Starting server...")
    process = subprocess.Popen([
        sys.executable, "run_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def test_api():
    """Test the API"""
    url = "http://localhost:8000/api/v1/recipes/generate-from-trend"
    payload = {
        "trend": "labubu valentine matcha",
        "user_segment": "genz", 
        "occasion": "hallowen",
        "language": "vi"
    }
    
    print("Testing API...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Start server
    server_process = start_server()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(10)
    
    # Test API
    test_api()
    
    # Stop server
    print("Stopping server...")
    server_process.terminate()

if __name__ == "__main__":
    main()
