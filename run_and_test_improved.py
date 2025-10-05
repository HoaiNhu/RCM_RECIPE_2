import subprocess
import time
import requests
import json
import sys
import os
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[0]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

def start_server():
    """Start the FastAPI server in background"""
    print("Starting server...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ], cwd=ROOT_DIR)
    return process

def wait_for_server(max_attempts=30):
    """Wait for server to be ready"""
    print("Waiting for server to start...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"Attempt {i+1}/{max_attempts}...")
    return False

def test_apis():
    """Test both APIs"""
    base_url = "http://localhost:8000"
    
    # Test 1: generate-from-trend
    print("\n" + "=" * 60)
    print("🧪 TEST 1: generate-from-trend API")
    print("=" * 60)
    
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
            print("✅ SUCCESS!")
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: generate-from-ingredients
    print("\n" + "=" * 60)
    print("🧪 TEST 2: generate-from-ingredients API")
    print("=" * 60)
    
    ingredients_data = {
        "ingredients": "bột mì, đường, trứng, bơ, bột matcha",
        "language": "vi"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/recipes/generate-from-ingredients", json=ingredients_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 Starting RCM_RECIPE_2 Server and Testing...")
    print(f"Project root: {ROOT_DIR}")
    
    # Start server
    server_process = start_server()
    
    try:
        # Wait for server to be ready
        if wait_for_server():
            # Test APIs
            test_apis()
        else:
            print("❌ Server failed to start within timeout")
    finally:
        # Clean up
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()

