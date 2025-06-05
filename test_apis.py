#!/usr/bin/env python3
"""Test individual APIs to see which ones work"""

from xhs_client import XHSClient
import json

client = XHSClient()

print("Testing APIs...")

# 1. Test homefeed
print("\n1. Testing Homefeed...")
try:
    posts = client.get_homefeed_posts(num=2)
    print(f"✅ Homefeed works! Got {len(posts)} posts")
    if posts:
        note_id = posts[0].get('id')
        print(f"   First post ID: {note_id}")
except Exception as e:
    print(f"❌ Homefeed failed: {e}")
    note_id = None

# 2. Test search
print("\n2. Testing Search...")
try:
    results = client.search_notes("test", num=2)
    print(f"✅ Search works! Got {len(results)} results")
except Exception as e:
    print(f"❌ Search failed: {e}")

# 3. Test comments (if we have a note_id)
print("\n3. Testing Comments...")
if note_id:
    try:
        # Try the raw endpoint first
        response = client.get_comments(note_id)
        print(f"✅ Comments raw endpoint works!")
        print(f"   Response keys: {list(response.keys())}")
    except Exception as e:
        print(f"❌ Comments failed: {e}")
        
# 4. Test feed/related posts
print("\n4. Testing Related Posts...")
if note_id:
    try:
        related = client.get_related_posts(note_id, num=2)
        print(f"✅ Related posts works! Got {len(related)} posts")
    except Exception as e:
        print(f"❌ Related posts failed: {e}")

print("\nDone!")