#!/usr/bin/env python3
"""
Keep Alive Script for Render Free Tier
=====================================

This script pings your Render service every 5 minutes to prevent it from
spinning down due to inactivity on the free tier.

Usage:
    python keep_alive.py

Requirements:
    - requests library (install with: pip install requests)

Configuration:
    - Set SERVICE_URL to your Render service URL
    - Adjust PING_INTERVAL if needed (default: 5 minutes)
"""

import requests
import time
import logging
from datetime import datetime
from typing import Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

# ⚠️ IMPORTANT: Replace this with your actual Render service URL
SERVICE_URL = "https://your-service.onrender.com"

# Ping interval in seconds (5 minutes = 300 seconds)
PING_INTERVAL = 300  # 5 minutes

# Ping endpoint path
PING_ENDPOINT = "/ping"

# Health check endpoint (optional, for verification)
HEALTH_ENDPOINT = "/health"

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# Enable detailed logging
LOG_LEVEL = logging.INFO

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('keep_alive.log')
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# FUNCTIONS
# ============================================================================

def ping_service(url: str, endpoint: str = PING_ENDPOINT, timeout: int = REQUEST_TIMEOUT) -> bool:
    """
    Ping the service to keep it alive.
    
    Args:
        url: Base URL of the service
        endpoint: Endpoint path to ping
        timeout: Request timeout in seconds
        
    Returns:
        bool: True if ping successful, False otherwise
    """
    full_url = f"{url.rstrip('/')}{endpoint}"
    
    try:
        logger.info(f"Pinging service at {full_url}...")
        
        response = requests.get(full_url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        logger.info(f"✅ Ping successful! Status: {data.get('status', 'unknown')}")
        logger.debug(f"Response data: {data}")
        
        return True
        
    except requests.exceptions.Timeout:
        logger.error(f"❌ Ping timeout after {timeout} seconds")
        return False
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
        return False
        
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Connection error - Service may be down or URL is incorrect")
        return False
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request failed: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return False


def check_health(url: str, endpoint: str = HEALTH_ENDPOINT, timeout: int = REQUEST_TIMEOUT) -> Optional[dict]:
    """
    Check the health status of the service.
    
    Args:
        url: Base URL of the service
        endpoint: Health check endpoint path
        timeout: Request timeout in seconds
        
    Returns:
        dict: Health status data if successful, None otherwise
    """
    full_url = f"{url.rstrip('/')}{endpoint}"
    
    try:
        logger.info(f"Checking service health at {full_url}...")
        
        response = requests.get(full_url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        logger.info(f"✅ Health check successful! Status: {data.get('status', 'unknown')}")
        logger.info(f"   Service: {data.get('service', 'N/A')}")
        logger.info(f"   Version: {data.get('version', 'N/A')}")
        
        return data
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        return None


def validate_configuration() -> bool:
    """
    Validate the script configuration.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if SERVICE_URL == "https://your-service.onrender.com":
        logger.error("❌ SERVICE_URL not configured!")
        logger.error("   Please edit this script and set SERVICE_URL to your Render service URL")
        return False
        
    if not SERVICE_URL.startswith(('http://', 'https://')):
        logger.error(f"❌ Invalid SERVICE_URL: {SERVICE_URL}")
        logger.error("   URL must start with http:// or https://")
        return False
        
    if PING_INTERVAL < 60:
        logger.warning(f"⚠️  PING_INTERVAL is very short: {PING_INTERVAL}s")
        logger.warning("   This may cause excessive requests to your service")
        
    return True


def run_keep_alive():
    """
    Main function to run the keep-alive loop.
    """
    logger.info("=" * 80)
    logger.info("🚀 Starting Keep-Alive Service")
    logger.info("=" * 80)
    logger.info(f"Service URL: {SERVICE_URL}")
    logger.info(f"Ping Endpoint: {PING_ENDPOINT}")
    logger.info(f"Ping Interval: {PING_INTERVAL} seconds ({PING_INTERVAL / 60:.1f} minutes)")
    logger.info("=" * 80)
    
    # Validate configuration
    if not validate_configuration():
        logger.error("❌ Configuration validation failed. Exiting.")
        return
    
    # Initial health check
    logger.info("\n🔍 Performing initial health check...")
    health_data = check_health(SERVICE_URL)
    
    if health_data is None:
        logger.warning("⚠️  Initial health check failed - service may not be ready yet")
        logger.info("   Will continue with pings anyway...")
    
    # Stats
    ping_count = 0
    success_count = 0
    fail_count = 0
    start_time = datetime.now()
    
    logger.info("\n🔄 Starting ping loop...")
    logger.info("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            ping_count += 1
            
            logger.info(f"\n{'=' * 60}")
            logger.info(f"Ping #{ping_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'=' * 60}")
            
            # Perform ping
            success = ping_service(SERVICE_URL)
            
            if success:
                success_count += 1
            else:
                fail_count += 1
            
            # Display stats
            uptime = datetime.now() - start_time
            success_rate = (success_count / ping_count * 100) if ping_count > 0 else 0
            
            logger.info(f"\n📊 Statistics:")
            logger.info(f"   Total Pings: {ping_count}")
            logger.info(f"   Successful: {success_count} ({success_rate:.1f}%)")
            logger.info(f"   Failed: {fail_count}")
            logger.info(f"   Uptime: {uptime}")
            logger.info(f"   Next ping in {PING_INTERVAL} seconds...")
            
            # Wait for next ping
            time.sleep(PING_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Keep-Alive service stopped by user")
        logger.info(f"\n📊 Final Statistics:")
        logger.info(f"   Total Runtime: {datetime.now() - start_time}")
        logger.info(f"   Total Pings: {ping_count}")
        logger.info(f"   Successful: {success_count}")
        logger.info(f"   Failed: {fail_count}")
        logger.info(f"   Success Rate: {(success_count / ping_count * 100):.1f}%")
        logger.info("\n👋 Goodbye!\n")
        
    except Exception as e:
        logger.error(f"\n❌ Unexpected error in main loop: {str(e)}")
        logger.exception("Full traceback:")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        run_keep_alive()
    except Exception as e:
        logger.critical(f"❌ Fatal error: {str(e)}")
        logger.exception("Full traceback:")
        exit(1)
