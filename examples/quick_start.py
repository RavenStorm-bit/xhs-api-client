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
    
    # Configuration
    # Replace with your token server details
    TOKEN_SERVER_URL = "https://your-token-server.com:8443"
    API_KEY = "your-api-key"
    
    # Check for config file
    if os.path.exists("config.json"):
        with open("config.json") as f:
            config = json.load(f)
            TOKEN_SERVER_URL = config["token_server"]["url"]
            API_KEY = config["token_server"]["api_key"]
    
    try:
        # Initialize client
        print("Initializing XHS Client...")
        client = XHSClient(
            token_server_url=TOKEN_SERVER_URL,
            api_key=API_KEY,
            cookies_path="cookies.json",
            enable_logging=True
        )
        
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