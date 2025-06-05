#!/usr/bin/env python3
"""
Example: Using Custom Device ID (a1)

This example shows how to manually specify a device ID instead of
relying on cookies.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_manager import TokenManager


def main():
    """Demo of custom device ID usage"""
    
    # Initialize token manager
    token_manager = TokenManager(
        server_url="https://31.97.132.244:8443",  # Demo server
        api_key="dev-key-123"
    )
    
    print("Device ID (a1) Usage Examples")
    print("="*40)
    
    # Example 1: Default device ID
    print("\n1. Using default device ID:")
    token = token_manager.get_xs_common_token()
    print(f"   Token generated: {token[:30]}...")
    
    # Example 2: Custom device ID
    print("\n2. Using custom device ID:")
    custom_a1 = "1234567890abcdef" * 3 + "1234"  # 52 characters
    token = token_manager.get_xs_common_token(a1=custom_a1)
    print(f"   Device ID: {custom_a1}")
    print(f"   Token generated: {token[:30]}...")
    
    # Example 3: Extract from cookies
    print("\n3. Device ID from cookies:")
    print("   When you export cookies from XiaoHongShu, look for:")
    print("   {")
    print('     "name": "a1",')
    print('     "value": "YOUR_52_CHAR_DEVICE_ID_HERE"')
    print("   }")
    
    # Example 4: Full token generation with custom a1
    print("\n4. Complete example with custom device ID:")
    
    # X-S-Common token
    xs_common = token_manager.get_xs_common_token(a1=custom_a1)
    print(f"   X-S-Common: {xs_common[:30]}...")
    
    # X-S token
    xs_token, timestamp = token_manager.get_xs_token(
        endpoint="/api/sns/web/v1/homefeed",
        payload={"cursor_score": "", "num": 20},
        a1=custom_a1  # Same device ID
    )
    print(f"   X-S: {xs_token[:30]}...")
    print(f"   Timestamp: {timestamp}")
    
    print("\n✅ Important notes:")
    print("- Both tokens should use the same device ID")
    print("- Device ID must match your cookies for real API calls")
    print("- Default ID works for testing token generation only")


if __name__ == "__main__":
    main()