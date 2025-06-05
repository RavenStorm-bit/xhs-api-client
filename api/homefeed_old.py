#!/usr/bin/env python3
"""
Refactored XiaoHongShu Homefeed API Client

This version uses the TokenManager to get tokens from a secure server
instead of generating them locally.
"""

import json
import time
import uuid
from typing import Dict, Optional, Any, List
from curl_cffi import requests
from pathlib import Path
import argparse

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from token_manager import TokenManager


class HomefeedAPI:
    """XiaoHongShu Homefeed API client with server-based token generation"""
    
    BASE_URL = "https://edith.xiaohongshu.com"
    ENDPOINT = "/api/sns/web/v1/homefeed"
    
    def __init__(self, token_manager: TokenManager, cookies_path: Optional[str] = None):
        """
        Initialize Homefeed API client
        
        Args:
            token_manager: TokenManager instance for getting tokens
            cookies_path: Path to cookies file
        """
        self.token_manager = token_manager
        
        # Load cookies
        self.cookies = {}
        self.a1 = None
        
        if cookies_path and Path(cookies_path).exists():
            self.cookies = self._load_cookies(cookies_path)
            # Extract a1 from cookies
            self.a1 = self.cookies.get('a1')
    
    def _load_cookies(self, path: str) -> Dict[str, str]:
        """Load cookies from JSON file"""
        try:
            with open(path, 'r') as f:
                cookies_list = json.load(f)
                return {cookie['name']: cookie['value'] for cookie in cookies_list}
        except:
            print(f"Warning: Failed to load cookies from {path}")
            return {}
    
    def fetch_homefeed(self, cursor_score: str = "", num: int = 20, 
                      refresh_type: int = 1, note_index: int = 0) -> Dict[str, Any]:
        """
        Fetch homefeed data
        
        Args:
            cursor_score: Pagination cursor (empty for first page)
            num: Number of items to fetch
            refresh_type: Refresh type (1 = refresh, 3 = load more)
            note_index: Note index for pagination
            
        Returns:
            API response as dictionary
        """
        # Prepare request payload
        payload = {
            "cursor_score": cursor_score,
            "num": num,
            "refresh_type": refresh_type,
            "note_index": note_index,
            "image_formats": ["jpg", "webp", "avif"],
            "need_filter_image": False
        }
        
        # Get tokens from server
        print(f"Getting tokens from server...")
        
        # Get X-S-Common token (cached)
        x_s_common = self.token_manager.get_xs_common_token(a1=self.a1)
        
        # Get X-S token (per-request)
        x_s, timestamp = self.token_manager.get_xs_token(
            endpoint=self.ENDPOINT,
            payload=payload,
            a1=self.a1
        )
        
        # Prepare headers
        headers = {
            "X-S": x_s,
            "X-S-Common": x_s_common,
            "X-T": str(timestamp),
            "X-B3-TraceId": str(uuid.uuid4()).replace('-', ''),
            "X-Xray-TraceId": str(uuid.uuid4()).replace('-', ''),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en,en-US;q=0.9",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.xiaohongshu.com",
            "Referer": "https://www.xiaohongshu.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Make request
        print(f"Fetching homefeed (cursor: {cursor_score or '<empty>'})...")
        
        try:
            response = requests.post(
                f"{self.BASE_URL}{self.ENDPOINT}",
                headers=headers,
                cookies=self.cookies,
                json=payload,
                impersonate="chrome",
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return {"error": f"HTTP {response.status_code}", "response": response.text}
            
            return response.json()
            
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return {"error": str(e)}
    
    def fetch_multiple_pages(self, total_items: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch multiple pages of homefeed
        
        Args:
            total_items: Total number of items to fetch
            
        Returns:
            List of all items fetched
        """
        all_items = []
        cursor_score = ""
        note_index = 0
        
        while len(all_items) < total_items:
            # Calculate how many items to fetch
            remaining = total_items - len(all_items)
            num = min(20, remaining)  # Max 20 per request
            
            # Fetch page
            result = self.fetch_homefeed(
                cursor_score=cursor_score,
                num=num,
                refresh_type=1 if not cursor_score else 3,
                note_index=note_index
            )
            
            if "error" in result:
                print(f"Error fetching page: {result['error']}")
                break
            
            # Extract items
            items = result.get("data", {}).get("items", [])
            all_items.extend(items)
            
            # Update pagination
            cursor_score = result.get("data", {}).get("cursor_score", "")
            note_index = len(all_items)
            
            # Check if more data available
            has_more = result.get("data", {}).get("has_more", False)
            if not has_more or not cursor_score:
                break
            
            print(f"Fetched {len(all_items)}/{total_items} items...")
            
            # Small delay between requests
            if len(all_items) < total_items:
                time.sleep(0.5)
        
        return all_items


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="Fetch XiaoHongShu homefeed using secure token server")
    parser.add_argument("--server", default="http://localhost:8000", help="Token server URL")
    parser.add_argument("--api-key", default="your-api-key", help="API key for token server")
    parser.add_argument("--num", type=int, default=20, help="Number of items to fetch")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output")
    parser.add_argument("--cookies", default="cookies.json", help="Path to cookies file")
    
    args = parser.parse_args()
    
    # Initialize token manager
    print(f"Connecting to token server at {args.server}...")
    token_manager = TokenManager(
        server_url=args.server,
        api_key=args.api_key
    )
    
    # Check server health
    if not token_manager.health_check():
        print("Error: Token server is not responding")
        return 1
    
    print("✓ Token server connected")
    
    # Initialize API client
    api = HomefeedAPI(
        token_manager=token_manager,
        cookies_path=args.cookies
    )
    
    # Fetch homefeed
    if args.num <= 20:
        result = api.fetch_homefeed(num=args.num)
        items = result.get("data", {}).get("items", [])
    else:
        items = api.fetch_multiple_pages(total_items=args.num)
        result = {"data": {"items": items}}
    
    # Save output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump(result, f, ensure_ascii=False)
        print(f"\nOutput written to: {args.output}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Items fetched: {len(items)}")
    if items:
        print(f"\nFirst few items:")
        for i, item in enumerate(items[:3]):
            note_card = item.get("note_card", {})
            title = note_card.get("display_title", "Untitled")[:50]
            note_id = item.get("id", "Unknown")
            print(f"  {i+1}. [{note_id}] {title}...")
    
    return 0


if __name__ == "__main__":
    exit(main())