#!/usr/bin/env python3
"""Check homefeed data structure to understand xsec_token usage"""

from xhs_client import XHSClient
import json

client = XHSClient()

print("Fetching homefeed to examine data structure...")
response = client.get_homefeed(num=3)

# Save full response for analysis
with open('homefeed_structure.json', 'w', encoding='utf-8') as f:
    json.dump(response, f, ensure_ascii=False, indent=2)
print("✅ Full response saved to homefeed_structure.json")

# Check the structure
items = response.get("data", {}).get("items", [])
print(f"\nFound {len(items)} items")

# Examine each item
for i, item in enumerate(items, 1):
    print(f"\n{'='*50}")
    print(f"Item {i}:")
    print(f"  ID: {item.get('id')}")
    print(f"  Model Type: {item.get('model_type')}")
    print(f"  xsec_token: {item.get('xsec_token', 'NOT FOUND')}")
    
    # Check note_card structure
    note_card = item.get('note_card', {})
    print(f"  Note Card:")
    print(f"    Title: {note_card.get('display_title', '')[:40]}...")
    print(f"    Type: {note_card.get('type')}")
    
    # Check if xsec_token exists
    if item.get('xsec_token'):
        print(f"\n  ✅ This note has xsec_token!")
        print(f"     Token preview: {item['xsec_token'][:50]}...")
    else:
        print(f"\n  ❌ No xsec_token found")
    
    # List all top-level keys
    print(f"\n  All keys in item: {list(item.keys())}")

print("\n" + "="*50)
print("Key findings:")
print("- Each note in homefeed should have its own xsec_token")
print("- The xsec_token is required for accessing that specific note's feed/comments")
print("- We need to pass this token when calling feed or comments API")