#!/usr/bin/env python3
"""
Complete XHS API Demo - Showcasing ALL Available Features

Just drop your cookies.json in this folder and run:
    python demo_all_apis.py

This demo showcases all implemented APIs.
"""

from xhs_client import XHSClient
import json
import time

# Initialize client - that's all you need!
print("🚀 Initializing XHS API Client...")
client = XHSClient()

print("\n" + "="*60)
print("🎯 XiaoHongShu API Client - Complete Feature Demo")
print("="*60)

# ========== 1. HOMEFEED API ==========
print("\n📱 DEMO 1: Homefeed (Trending Posts)")
print("-"*50)

posts = client.get_homefeed_posts(num=5)
print(f"✅ Found {len(posts)} trending posts")

if posts:
    first_post = posts[0]
    info = client.extract_note_info(first_post)
    print(f"\nExample post: {info['title']}")
    print(f"Author: {info['author']['nickname']} (@{info['author']['user_id']})")
    
    # Save for later demos
    note_id = info['id']
    user_id = info['author']['user_id']

# ========== 2. SEARCH API ==========
print("\n\n🔍 DEMO 2: Search API")
print("-"*50)

search_keyword = "咖啡"
print(f"Searching for: {search_keyword}")
search_results = client.search_notes(search_keyword, num=5)
print(f"✅ Found {len(search_results)} posts about '{search_keyword}'")

if search_results:
    for i, post in enumerate(search_results[:3], 1):
        info = client.extract_note_info(post)
        print(f"  {i}. {info['title']}")

# ========== 3. USER POSTS API ==========
print("\n\n👤 DEMO 3: User Posts & Profile")
print("-"*50)

if 'user_id' in locals():
    print(f"Fetching profile for user: {user_id}")
    
    # Get user profile
    profile = client.get_user_profile(user_id)
    print(f"\nUser Profile:")
    print(f"  Nickname: {profile['nickname']}")
    print(f"  Followers: {profile['fans']:,}")
    print(f"  Following: {profile['follows']:,}")
    print(f"  Posts: {profile['note_count']}")
    
    # Get user posts
    user_posts = client.get_user_posts(user_id, num=3)
    print(f"\n✅ Found {len(user_posts)} posts from this user")
    
    for i, post in enumerate(user_posts[:2], 1):
        print(f"  {i}. {post.get('display_title', 'Untitled')}")

# ========== 4. COMMENTS API ==========
print("\n\n💬 DEMO 4: Comments API")
print("-"*50)

if 'note_id' in locals():
    print(f"Fetching comments for note: {note_id}")
    comments = client.get_note_comments(note_id, num=5)
    print(f"✅ Found {len(comments)} comments")
    
    for i, comment in enumerate(comments[:3], 1):
        print(f"\n  Comment {i}:")
        print(f"    User: @{comment['user_nickname']}")
        print(f"    Text: {comment['content'][:50]}...")
        print(f"    Likes: {comment['like_count']}")

# ========== 5. RELATED POSTS API ==========
print("\n\n🔗 DEMO 5: Related Posts (Feed API)")
print("-"*50)

if 'note_id' in locals():
    print(f"Finding posts related to: {note_id}")
    related_posts = client.get_related_posts(note_id, num=5)
    print(f"✅ Found {len(related_posts)} related posts")
    
    for i, post in enumerate(related_posts[:3], 1):
        info = client.extract_note_info(post)
        print(f"  {i}. {info['title']}")
        print(f"     by @{info['author']['nickname']}")

# ========== 6. COMPLETE WORKFLOW EXAMPLE ==========
print("\n\n🎯 DEMO 6: Complete Workflow")
print("-"*50)
print("Demonstrating a full user journey:")

# Step 1: Search for a topic
topic = "深圳美食"
print(f"\n1️⃣ Searching for '{topic}'...")
results = client.search_notes(topic, num=1)

if results:
    post = results[0]
    post_info = client.extract_note_info(post)
    print(f"   Found: {post_info['title']}")
    
    # Step 2: Get the author's profile
    author_id = post_info['author']['user_id']
    print(f"\n2️⃣ Checking author's profile...")
    author_profile = client.get_user_profile(author_id)
    print(f"   Author: {author_profile['nickname']} ({author_profile['fans']} followers)")
    
    # Step 3: Get related posts
    print(f"\n3️⃣ Finding related posts...")
    related = client.get_related_posts(post_info['id'], num=3)
    print(f"   Found {len(related)} related posts")
    
    # Step 4: Check comments
    print(f"\n4️⃣ Reading comments...")
    post_comments = client.get_note_comments(post_info['id'], num=2)
    print(f"   Found {len(post_comments)} comments")

# ========== SAVE DATA ==========
print("\n\n💾 Saving Demo Data")
print("-"*50)

demo_data = {
    "timestamp": int(time.time()),
    "homefeed_sample": posts[:2] if 'posts' in locals() else [],
    "search_sample": search_results[:2] if 'search_results' in locals() else [],
    "stats": {
        "total_posts_fetched": len(posts) if 'posts' in locals() else 0,
        "search_results": len(search_results) if 'search_results' in locals() else 0
    }
}

client.save_response(demo_data, "demo_all_apis_output.json")
print("✅ Demo data saved to demo_all_apis_output.json")

# ========== SUMMARY ==========
print("\n\n" + "="*60)
print("✅ ALL APIS DEMONSTRATED SUCCESSFULLY!")
print("="*60)

print("\n📊 Available APIs:")
print("  ✓ Homefeed - Get trending posts")
print("  ✓ Search - Search for any content")
print("  ✓ User Posts - Get posts from specific users")
print("  ✓ User Profile - Get detailed user information")
print("  ✓ Comments - Read post comments")
print("  ✓ Related Posts - Find similar content")

print("\n💡 All APIs support:")
print("  - Automatic token generation")
print("  - Pagination for large datasets")
print("  - Response logging for debugging")
print("  - Simple, intuitive interfaces")

print("\n📝 Note: This uses a demo server with rate limits.")
print("   For production use, deploy your own token server.")

print("\n🎉 Happy coding with XHS API Client!")