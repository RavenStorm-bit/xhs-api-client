#!/usr/bin/env python3
"""
Technical Demo - Understanding Token Generation

This technical demo shows the behind-the-scenes token generation process.
For normal usage, use quick_demo.py instead.

This is useful for:
- Developers who want to understand how tokens work
- Debugging connection issues
- Testing without cookies

Note: The demo server has rate limits. For production use, deploy your own server.
"""

import json
import sys
import time
from datetime import datetime

from xhs_client import XHSClient
from token_manager import TokenManager


# Demo server configuration
# This is a public demo server for testing purposes
# Rate limit: 1000 requests/hour shared among all users
# For production use, deploy your own server!
DEMO_SERVER = "https://31.97.132.244:8443"
DEMO_API_KEY = "dev-key-123"

# Demo device ID for testing (not linked to any real account)
# Must be 52 chars with a digit at position -10 for platform code
DEMO_DEVICE_ID = "188c2ce12d41012345671234567890abcdef1234567890123412"  # 52 chars


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def demo_token_generation():
    """Demonstrate the token generation process"""
    print_header("XHS API Client - Live Demo")
    
    print("This demo shows how the XHS API client works with a real token server.")
    print(f"Demo server: {DEMO_SERVER}")
    print("\nNOTE: You'll need valid XiaoHongShu cookies in 'cookies.json' file.")
    print("      Without cookies, you'll see the token generation but API calls will fail.\n")
    
    input("Press Enter to start the demo...")
    
    # Step 1: Initialize token manager
    print("\n1. Initializing Token Manager...")
    print(f"   Server: {DEMO_SERVER}")
    print(f"   API Key: {DEMO_API_KEY[:8]}...")
    
    try:
        token_manager = TokenManager(
            server_url=DEMO_SERVER,
            api_key=DEMO_API_KEY
        )
        
        # Check server health
        if token_manager.health_check():
            print("   ✅ Token server is online!")
        else:
            print("   ❌ Token server is not responding")
            return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 2: Generate tokens
    print("\n2. Generating Tokens...")
    
    # Generate X-S-Common token
    print("   Requesting X-S-Common token (device fingerprint)...")
    print(f"   Using demo device ID: {DEMO_DEVICE_ID[:20]}...")
    try:
        start_time = time.time()
        xs_common = token_manager.get_xs_common_token(a1=DEMO_DEVICE_ID)
        elapsed = (time.time() - start_time) * 1000
        
        print(f"   ✅ X-S-Common token received in {elapsed:.0f}ms")
        print(f"   Token preview: {xs_common[:50]}...")
        print(f"   Token length: {len(xs_common)} characters")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Generate X-S token
    print("\n   Requesting X-S token (request signature)...")
    try:
        start_time = time.time()
        endpoint = "/api/sns/web/v1/homefeed"
        payload = {"cursor_score": "", "num": 20, "refresh_type": 1}
        
        xs_token, timestamp = token_manager.get_xs_token(
            endpoint=endpoint,
            payload=payload,
            a1=DEMO_DEVICE_ID
        )
        elapsed = (time.time() - start_time) * 1000
        
        print(f"   ✅ X-S token received in {elapsed:.0f}ms")
        print(f"   Token preview: {xs_token[:50]}...")
        print(f"   Token length: {len(xs_token)} characters")
        print(f"   Timestamp: {timestamp}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 3: Show token usage
    print("\n3. How Tokens Are Used in API Requests:")
    print("   ```")
    print("   Headers: {")
    print(f'     "X-S": "{xs_token[:30]}...",')
    print(f'     "X-S-Common": "{xs_common[:30]}...",')
    print(f'     "X-T": "{timestamp}"')
    print("   }")
    print("   ```")
    
    # Step 4: Try API call (if cookies exist)
    print("\n4. Testing API Call...")
    
    try:
        # Check if cookies file exists
        import os
        if not os.path.exists("cookies.json"):
            print("   ⚠️  No cookies.json file found.")
            print("   To make actual API calls, you need:")
            print("   1. Login to xiaohongshu.com in your browser")
            print("   2. Export cookies to cookies.json file")
            print("   3. Run this demo again")
        else:
            # Try to make API call
            print("   Found cookies.json, attempting API call...")
            
            client = XHSClient(
                token_server_url=DEMO_SERVER,
                api_key=DEMO_API_KEY,
                cookies_path="cookies.json",
                enable_logging=False
            )
            
            posts = client.get_homefeed_posts(num=3)
            
            if posts:
                print(f"   ✅ Successfully fetched {len(posts)} posts!")
                print("\n   Sample posts:")
                for i, post in enumerate(posts[:3], 1):
                    info = client.extract_note_info(post)
                    print(f"   {i}. {info['title'][:50]}...")
                    print(f"      Author: {info['author']['nickname']}")
                    print(f"      Likes: {info['stats']['likes']:,}")
            else:
                print("   ❌ No posts returned. Cookies may be invalid.")
                
    except Exception as e:
        print(f"   ❌ API call failed: {str(e)}")
    
    # Step 5: Server stats
    print("\n5. Token Server Statistics:")
    try:
        stats = token_manager.get_stats()
        print(f"   Rate limit: {stats['rate_limit']} requests/hour")
        print(f"   Cache available: {stats['cache_available']}")
        print(f"   Client type: {stats['client']}")
    except:
        pass
    
    print_header("Demo Complete!")
    
    print("What you learned:")
    print("✓ Token server generates authentication tokens")
    print("✓ X-S-Common token = device fingerprint (cacheable)")
    print("✓ X-S token = request signature (unique per request)")
    print("✓ Both tokens required for API calls")
    print("✓ Cookies needed for actual data access")
    
    print("\nNext steps:")
    print("1. Get XiaoHongShu cookies (includes your device ID 'a1')")
    print("2. Try the full client with: python xhs_client.py")
    print("3. Deploy your own token server for production use")
    
    print("\n📝 About Device ID (a1):")
    print("- Each XHS account has a unique 52-character device ID in cookies")
    print("- Demo uses a fake ID for testing token generation")
    print("- Real API calls require your actual device ID from cookies")
    print("- Server now requires a1 - no default fallback")
    
    print("\n⭐ Star the repo if you found this helpful!")
    print("   https://github.com/RavenStorm-bit/xhs-api-client")


def demo_simple_test():
    """Simple connectivity test"""
    print("\n🔍 Quick Server Test")
    print(f"Testing connection to {DEMO_SERVER}...")
    
    try:
        token_manager = TokenManager(DEMO_SERVER, DEMO_API_KEY)
        if token_manager.health_check():
            print("✅ Server is online and ready!")
            
            # Quick token test
            print("\nGenerating sample token...")
            token = token_manager.get_xs_common_token()
            print(f"✅ Token generated successfully!")
            print(f"   Length: {len(token)} characters")
            print(f"   Preview: {token[:30]}...")
        else:
            print("❌ Server is not responding")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("XHS API Client - Interactive Demo")
    print("================================\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        demo_simple_test()
    else:
        demo_token_generation()
    
    print("\n")