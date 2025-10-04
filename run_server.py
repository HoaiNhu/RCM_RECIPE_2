#!/usr/bin/env python3
"""
Script để chạy RCM_RECIPE_2 server
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT_DIR))

# Set environment variables
os.environ.setdefault('PYTHONPATH', str(ROOT_DIR))

if __name__ == "__main__":
    import uvicorn
    
    print("Starting RCM_RECIPE_2 Server...")
    print(f"Project root: {ROOT_DIR}")
    print(f"Python path: {sys.path[0]}")
    
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
