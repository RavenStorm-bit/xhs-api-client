#!/usr/bin/env python3
"""
XHS API Demo - Showcasing Available Features

Just drop your cookies.json in this folder and run:
    python quick_demo.py

That's it! This demo showcases the homefeed API and note details.
"""

from xhs_client import XHSClient
import json

# Initialize client - that's all you need!
print("🚀 Initializing XHS API Client...")
client = XHSClient()

# ========== 1. HOMEFEED API ==========
print("\n" + "="*50)
print("📱 DEMO: Homefeed (Trending Posts)")
print("="*50)

# Get multiple pages of posts
all_posts = []
cursor = ""

print("\nFetching trending posts from XiaoHongShu...")

# Fetch 3 pages
for page in range(3):
    print(f"\n📄 Page {page + 1}:")
    response = client.get_homefeed(num=10, cursor=cursor)
    posts = response.get("data", {}).get("items", [])
    
    if not posts:
        print("  No more posts available")
        break
        
    all_posts.extend(posts)
    print(f"  ✅ Fetched {len(posts)} posts")
    
    # Get cursor for next page
    cursor = response.get("data", {}).get("cursor", "")
    if not cursor:
        break

print(f"\n✨ Total posts fetched: {len(all_posts)}")

# Display first 10 posts with details
print("\n" + "="*50)
print("📊 Post Details (First 10)")
print("="*50)

for i, post in enumerate(all_posts[:10], 1):
    info = client.extract_note_info(post)
    print(f"\n{i}. {info['title']}")
    print(f"   👤 Author: {info['author']['nickname']}")
    print(f"   🆔 User ID: {info['author']['user_id']}")
    
    likes = int(info['stats']['likes']) if isinstance(info['stats']['likes'], (int, str)) and str(info['stats']['likes']).isdigit() else 0
    comments = int(info['stats']['comments']) if isinstance(info['stats']['comments'], (int, str)) and str(info['stats']['comments']).isdigit() else 0
    collects = int(info['stats']['collects']) if isinstance(info['stats']['collects'], (int, str)) and str(info['stats']['collects']).isdigit() else 0
    shares = int(info['stats']['shares']) if isinstance(info['stats']['shares'], (int, str)) and str(info['stats']['shares']).isdigit() else 0
    
    print(f"   ❤️  {likes:,} likes")
    print(f"   💬 {comments:,} comments")
    print(f"   ⭐ {collects:,} collects")
    print(f"   🔗 {shares:,} shares")
    print(f"   📝 Type: {info['type'].upper()}")
    print(f"   🎯 Note ID: {info['id']}")
    print(f"   🔑 Has Token: {'Yes' if info['has_token'] else 'No'}")

# ========== 2. SAVE DATA ==========
print("\n" + "="*50)
print("💾 Saving Data")
print("="*50)

# Save all posts
filename = "demo_trending_posts.json"
client.save_response(all_posts, filename)
print(f"✅ Saved {len(all_posts)} posts to {filename}")

# ========== 3. TOKEN SERVER STATS ==========
print("\n" + "="*50)
print("📈 Token Server Statistics")
print("="*50)

stats = client.get_stats()
print(f"  Server URL: {client.token_manager.server_url}")
print(f"  API Key: {client.token_manager.api_key[:10]}...")
print(f"  Cache available: {stats.get('cache_available', False)}")
print(f"  Health status: {stats.get('status', 'Unknown')}")

# ========== SUMMARY ==========
print("\n" + "="*50)
print("✅ DEMO COMPLETE!")
print("="*50)

print("\n📊 What This Client Can Do:")
print("  ✓ Fetch trending posts from homefeed")
print("  ✓ Handle pagination automatically")
print("  ✓ Extract and parse post information")
print("  ✓ Save data for analysis")
print("  ✓ Manage authentication tokens")

print("\n🚧 Coming Soon:")
print("  - Search API")
print("  - User posts API")
print("  - Comments API")
print("  - Note details API")
print("  - Related posts API")

print("\n💡 Tips:")
print("  - Check api_logs/ folder for raw API responses")
print("  - Use extract_note_info() to parse post data")
print("  - The demo server has a 1000 req/hour limit")

print("\n📝 Note: For production use with higher limits,")
print("   deploy your own token server or contact us.")

print("\n🎉 Happy coding with XHS API Client!")