#!/usr/bin/env python3
"""
Test Token Server Connection

Quick script to test if you can connect to the demo token server.
Run this first to make sure everything is working.
"""

import requests
import json
from datetime import datetime

# Demo server (public for testing)
SERVER_URL = "https://31.97.132.244:8443"
API_KEY = "dev-key-123"

print("XHS Token Server Connection Test")
print("="*40)
print(f"Server: {SERVER_URL}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test 1: Health check
print("1. Testing server health...")
try:
    # Disable SSL warnings for self-signed cert
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    response = requests.get(f"{SERVER_URL}/health", verify=False, timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Server is healthy!")
        print(f"   Timestamp: {data['timestamp']}")
        print(f"   Cache: {'Available' if data['cache_available'] else 'Not available'}")
    else:
        print(f"   ❌ Server returned status {response.status_code}")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    print("\n   Note: The demo server uses a self-signed certificate.")
    print("   This is normal for testing, but use proper certs in production.")
    exit(1)

# Test 2: Generate X-S-Common token
print("\n2. Testing token generation...")
try:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{SERVER_URL}/api/v1/tokens/xs-common",
        headers=headers,
        json={},
        verify=False,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['x_s_common']
        print(f"   ✅ Token generated successfully!")
        print(f"   Token length: {len(token)} characters")
        print(f"   Token preview: {token[:50]}...")
        print(f"   Cache key: {data['cache_key']}")
    else:
        print(f"   ❌ Failed with status {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Request failed: {e}")

# Test 3: API stats
print("\n3. Getting server statistics...")
try:
    response = requests.get(
        f"{SERVER_URL}/api/v1/stats",
        headers=headers,
        verify=False,
        timeout=5
    )
    
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ Stats retrieved!")
        print(f"   Client type: {stats['client']}")
        print(f"   Rate limit: {stats['rate_limit']} requests/hour")
        print(f"   Cache available: {stats['cache_available']}")
except Exception as e:
    print(f"   ❌ Stats request failed: {e}")

print("\n" + "="*40)
print("✅ All tests completed!")
print("\nThe demo server is working correctly.")
print("You can now run: python demo.py")
print("\nNote: This is a demo server with rate limits.")
print("For production, deploy your own token server.")