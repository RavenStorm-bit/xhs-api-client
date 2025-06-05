#!/usr/bin/env python3
"""
Super Simple XHS API Demo

Just drop your cookies.json in this folder and run:
    python quick_demo.py

That's it!
"""

from xhs_client import XHSClient

# Initialize client - that's all you need!
client = XHSClient()

# Get trending posts
print("Fetching trending posts from XiaoHongShu...")
posts = client.get_homefeed_posts(num=10)

# Display results
print(f"\n✨ Found {len(posts)} posts!\n")

for i, post in enumerate(posts, 1):
    info = client.extract_note_info(post)
    print(f"{i}. {info['title']}")
    print(f"   👤 {info['author']['nickname']}")
    print(f"   ❤️  {info['stats']['likes']:,} likes")
    print()

print("\n✅ Success! Your XHS API client is working!")
print("\n📝 Note: This uses a demo server with 1000 req/hour limit.")
print("   For unlimited access, contact us for a dedicated server.")