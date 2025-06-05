#!/usr/bin/env python3
"""
Complete XHS API Demo - Showcasing All Features

Just drop your cookies.json in this folder and run:
    python quick_demo.py

That's it! This demo showcases all available APIs.
"""

from xhs_client import XHSClient
import json

# Initialize client - that's all you need!
print("🚀 Initializing XHS API Client...")
client = XHSClient()

# ========== 1. HOMEFEED API ==========
print("\n" + "="*50)
print("📱 DEMO 1: Homefeed (Trending Posts)")
print("="*50)

posts = client.get_homefeed_posts(num=5)
print(f"\n✨ Found {len(posts)} trending posts!\n")

for i, post in enumerate(posts, 1):
    info = client.extract_note_info(post)
    print(f"{i}. {info['title']}")
    print(f"   👤 {info['author']['nickname']}")
    print(f"   ❤️  {info['stats']['likes']:,} likes")
    print(f"   💬 {info['stats']['comments']:,} comments")
    print(f"   🆔 Note ID: {info['note_id']}")
    print()

# Save first note ID for later demos
if posts:
    first_note_id = client.extract_note_info(posts[0])['note_id']
    first_xsec_token = posts[0].get('xsec_token', '')

# ========== 2. SEARCH API ==========
print("\n" + "="*50)
print("🔍 DEMO 2: Search API")
print("="*50)

search_keyword = "咖啡"
print(f"\nSearching for: {search_keyword}")
search_results = client.search_notes(search_keyword, num=5)
print(f"Found {len(search_results)} posts about '{search_keyword}'!\n")

for i, post in enumerate(search_results, 1):
    info = client.extract_note_info(post)
    print(f"{i}. {info['title']}")
    print(f"   👤 {info['author']['nickname']}")
    print(f"   📍 {info['type'].upper()} post")
    print()

# ========== 3. USER POSTS API ==========
print("\n" + "="*50)
print("👤 DEMO 3: User Posts API")
print("="*50)

# Get a user ID from the first post
if posts:
    first_user = client.extract_note_info(posts[0])['author']
    user_id = first_user['user_id']
    print(f"\nFetching posts from user: {first_user['nickname']}")
    print(f"User ID: {user_id}")
    
    user_posts = client.get_user_posts(user_id, num=3)
    print(f"\nFound {len(user_posts)} posts from this user!\n")
    
    for i, post in enumerate(user_posts, 1):
        info = client.extract_note_info(post)
        print(f"{i}. {info['title']}")
        print(f"   ❤️  {info['stats']['likes']:,} likes")
        print()

# ========== 4. NOTE DETAILS API ==========
print("\n" + "="*50)
print("📄 DEMO 4: Note Details API")
print("="*50)

if 'first_note_id' in locals() and 'first_xsec_token' in locals():
    print(f"\nFetching details for note: {first_note_id}")
    note_detail = client.get_note_by_id(first_note_id, first_xsec_token)
    
    if note_detail:
        print("\nNote Details:")
        print(f"  Title: {note_detail.get('title', 'N/A')}")
        print(f"  Description: {note_detail.get('desc', 'N/A')[:100]}...")
        print(f"  Image Count: {note_detail.get('image_count', 0)}")
        print(f"  Tags: {', '.join(note_detail.get('tags', []))}")
        print(f"  Posted at: {note_detail.get('time', 'N/A')}")

# ========== 5. COMMENTS API ==========
print("\n" + "="*50)
print("💬 DEMO 5: Comments API")
print("="*50)

if 'first_note_id' in locals() and 'first_xsec_token' in locals():
    print(f"\nFetching comments for note: {first_note_id}")
    comments = client.get_note_comments(first_note_id, first_xsec_token, num=5)
    
    print(f"Found {len(comments)} comments!\n")
    
    for i, comment in enumerate(comments, 1):
        print(f"{i}. @{comment.get('user_nickname', 'Anonymous')}: {comment.get('content', '')}")
        if comment.get('sub_comment_count', 0) > 0:
            print(f"   └─ {comment['sub_comment_count']} replies")
        print()

# ========== 6. FILTER API (Related/Similar Posts) ==========
print("\n" + "="*50)
print("🔗 DEMO 6: Related Posts API")
print("="*50)

if 'first_note_id' in locals():
    print(f"\nFinding posts related to: {first_note_id}")
    related_posts = client.get_related_posts(first_note_id, num=3)
    
    print(f"Found {len(related_posts)} related posts!\n")
    
    for i, post in enumerate(related_posts, 1):
        info = client.extract_note_info(post)
        print(f"{i}. {info['title']}")
        print(f"   👤 {info['author']['nickname']}")
        print()

# ========== SUMMARY ==========
print("\n" + "="*50)
print("✅ ALL APIS DEMONSTRATED SUCCESSFULLY!")
print("="*50)

print("\n📊 Available APIs Summary:")
print("  1. Homefeed - Get trending posts")
print("  2. Search - Search for specific content")
print("  3. User Posts - Get posts from a specific user")
print("  4. Note Details - Get detailed info about a post")
print("  5. Comments - Get comments on a post")
print("  6. Related Posts - Find similar content")

print("\n💡 Tips:")
print("  - All methods support pagination")
print("  - Use extract_note_info() to parse post data")
print("  - Check logs/ folder for debugging")

print("\n📝 Note: This uses a demo server with 1000 req/hour limit.")
print("   For unlimited access, contact us for a dedicated server.")

print("\n🎉 Happy coding with XHS API Client!")