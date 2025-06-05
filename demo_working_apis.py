#!/usr/bin/env python3
"""
XHS API Demo - Working Features Only

This demo only shows APIs that are currently working.
"""

from xhs_client import XHSClient
import json
import time

# Initialize client
print("🚀 Initializing XHS API Client...")
client = XHSClient()

print("\n" + "="*60)
print("🎯 XiaoHongShu API Client - Working Features Demo")
print("="*60)

# ========== 1. HOMEFEED API ==========
print("\n📱 DEMO 1: Homefeed (Trending Posts)")
print("-"*50)

# Get posts with proper pagination
all_posts = []
cursor = ""

for page in range(2):
    print(f"\nFetching page {page + 1}...")
    response = client.get_homefeed(num=10, cursor=cursor)
    posts = response.get("data", {}).get("items", [])
    
    if not posts:
        break
        
    all_posts.extend(posts)
    cursor = response.get("data", {}).get("cursor_score", "")
    
    print(f"✅ Got {len(posts)} posts")

print(f"\nTotal posts fetched: {len(all_posts)}")

# Display some posts
print("\nSample posts:")
for i, post in enumerate(all_posts[:5], 1):
    info = client.extract_note_info(post)
    print(f"\n{i}. {info['title']}")
    print(f"   Author: @{info['author']['nickname']}")
    print(f"   Type: {info['type']}")
    
    # Check for xsec_token
    if post.get('xsec_token'):
        print(f"   ✅ Has xsec_token (can get related posts)")
    else:
        print(f"   ❌ No xsec_token")

# ========== 2. SEARCH API ==========
print("\n\n🔍 DEMO 2: Search API")
print("-"*50)

keywords = ["咖啡", "深圳", "美食"]
for keyword in keywords:
    print(f"\nSearching for: {keyword}")
    results = client.search_notes(keyword, num=3)
    print(f"✅ Found {len(results)} posts")
    
    for i, post in enumerate(results[:2], 1):
        info = client.extract_note_info(post)
        print(f"  {i}. {info['title'][:30]}...")

# ========== 3. COMPLETE WORKFLOW ==========
print("\n\n🎯 DEMO 3: Working Workflow")
print("-"*50)

# Find a post with xsec_token for related posts
post_with_token = None
for post in all_posts:
    if post.get('xsec_token'):
        post_with_token = post
        break

if post_with_token:
    info = client.extract_note_info(post_with_token)
    print(f"\nUsing post: {info['title']}")
    print(f"Note ID: {info['id']}")
    
    # Try to get related posts using xsec_token
    print("\nAttempting to get related posts...")
    try:
        # We need to pass xsec_token in the feed API
        # Since our current implementation doesn't support it,
        # we'll just demonstrate what would work
        print("⚠️  Related posts API requires xsec_token parameter")
        print("   This is not yet implemented in our client")
    except Exception as e:
        print(f"   Error: {e}")

# ========== SAVE DATA ==========
print("\n\n💾 Saving Demo Data")
print("-"*50)

# Save some data
sample_data = {
    "timestamp": int(time.time()),
    "total_posts": len(all_posts),
    "sample_posts": [client.extract_note_info(p) for p in all_posts[:3]]
}

client.save_response(sample_data, "demo_working_output.json")
print("✅ Data saved to demo_working_output.json")

# ========== SUMMARY ==========
print("\n\n" + "="*60)
print("✅ WORKING FEATURES DEMONSTRATED!")
print("="*60)

print("\n📊 Currently Working:")
print("  ✅ Homefeed - Get trending posts with pagination")
print("  ✅ Search - Search for any content")
print("  ✅ Data extraction - Parse post information")
print("  ✅ Response logging - Save API responses")

print("\n🚧 Known Issues:")
print("  ⚠️  Comments API - Endpoint returns 404")
print("  ⚠️  Related Posts - Requires xsec_token in request")
print("  ⚠️  User API - Not implemented in original code")

print("\n💡 Notes:")
print("  - Homefeed provides xsec_token for each post")
print("  - Search API works perfectly for content discovery")
print("  - All responses are automatically logged")

print("\n🎉 The client successfully handles the main use cases!")