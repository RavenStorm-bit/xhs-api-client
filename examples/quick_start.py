#!/usr/bin/env python3
"""
Quick Start Example for XHS API Client

This example shows basic usage of the XHS API client.
"""

import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xhs_client import XHSClient


def main():
    """Quick start example"""
    
    try:
        # Initialize client - super simple!
        print("Initializing XHS Client...")
        client = XHSClient()  # That's all you need!
        
        print("✓ Client initialized successfully!\n")
        
        # Get homefeed
        print("Fetching homefeed posts...")
        posts = client.get_homefeed_posts(num=5)
        
        if not posts:
            print("No posts retrieved. Please check:")
            print("1. Your cookies.json file is valid")
            print("2. Token server is running")
            print("3. API key is correct")
            return
        
        print(f"✓ Retrieved {len(posts)} posts\n")
        
        # Display posts
        for i, post in enumerate(posts, 1):
            info = client.extract_note_info(post)
            print(f"{i}. {info['title']}")
            print(f"   Author: {info['author']['nickname']}")
            print(f"   Likes: {info['stats']['likes']:,}")
            print(f"   Comments: {info['stats']['comments']:,}")
            print()
        
        # Save first post
        if posts:
            print("Saving first post data...")
            client.save_response(posts[0], "first_post.json")
            print("✓ Saved to first_post.json")
        
    except ConnectionError:
        print("❌ Error: Could not connect to token server")
        print(f"   Please ensure the server is running at: {TOKEN_SERVER_URL}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()