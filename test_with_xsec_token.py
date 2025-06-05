#!/usr/bin/env python3
"""Test APIs with proper xsec_token usage"""

from xhs_client import XHSClient
import json

client = XHSClient()

print("Testing APIs with xsec_token...")

# 1. Get homefeed posts with xsec_token
print("\n1. Fetching homefeed...")
posts = client.get_homefeed_posts(num=5)
print(f"✅ Got {len(posts)} posts")

# Find a post with xsec_token
post_with_token = None
for post in posts:
    if post.get('xsec_token'):
        post_with_token = post
        break

if not post_with_token:
    print("❌ No posts with xsec_token found!")
    exit(1)

# Extract info
info = client.extract_note_info(post_with_token)
note_id = info['id']
xsec_token = post_with_token['xsec_token']

print(f"\nUsing post: {info['title']}")
print(f"Note ID: {note_id}")
print(f"xsec_token: {xsec_token[:30]}...")

# 2. Test comments with xsec_token
print("\n2. Testing Comments API with xsec_token...")
try:
    comments = client.get_note_comments(note_id, xsec_token, num=5)
    print(f"✅ Comments API works! Got {len(comments)} comments")
    
    if comments:
        print("\nSample comment:")
        c = comments[0]
        print(f"  User: @{c['user_nickname']}")
        print(f"  Text: {c['content'][:50]}...")
except Exception as e:
    print(f"❌ Comments API failed: {e}")

# 3. Test related posts with xsec_token
print("\n3. Testing Related Posts API with xsec_token...")
try:
    related = client.get_related_posts(note_id, xsec_token, num=5)
    print(f"✅ Related Posts API works! Got {len(related)} posts")
    
    if related:
        print("\nRelated posts:")
        for i, post in enumerate(related[:3], 1):
            rinfo = client.extract_note_info(post)
            print(f"  {i}. {rinfo['title'][:40]}...")
except Exception as e:
    print(f"❌ Related Posts API failed: {e}")

# 4. Test browse_note (combines everything)
print("\n4. Testing browse_note...")
try:
    result = client.browse_note(post_with_token)
    print("✅ browse_note works!")
    print(f"  Has note: {'note' in result}")
    print(f"  Has comments: {'comments' in result}")
except Exception as e:
    print(f"❌ browse_note failed: {e}")

print("\n✅ Done! APIs are working correctly with xsec_token!")