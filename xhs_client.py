#!/usr/bin/env python3
"""
XiaoHongShu API Client - Main Interface

A comprehensive client for interacting with XiaoHongShu (Little Red Book) API
using secure token generation from a remote server.
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

try:
    from .token_manager import TokenManager
    from .api import HomefeedAPI, SearchAPI, CommentsAPI, FeedAPI, UserAPI
except ImportError:
    from token_manager import TokenManager
    from api import HomefeedAPI, SearchAPI, CommentsAPI, FeedAPI, UserAPI


class XHSClient:
    """
    Main XiaoHongShu API Client
    
    This client provides a unified interface to all XiaoHongShu APIs
    with automatic token management and response logging.
    """
    
    def __init__(
        self,
        cookies_path: str = "cookies.json",
        token_server_url: str = "https://31.97.132.244:8443",
        api_key: str = "dev-key-123",
        enable_logging: bool = True,
        log_dir: str = "api_logs"
    ):
        """
        Initialize XHS Client
        
        Args:
            cookies_path: Path to cookies.json file (default: "cookies.json")
            token_server_url: URL of the token generation server (default: public demo server)
            api_key: API key for token server authentication (default: demo key)
            enable_logging: Whether to log API responses (default: True)
            log_dir: Directory for API response logs (default: "api_logs")
            
        Note: The default server has rate limits (1000 req/hour). For production use,
              deploy your own server or contact us for higher limits.
        """
        # Initialize token manager
        self.token_manager = TokenManager(
            server_url=token_server_url,
            api_key=api_key
        )
        
        # Check server health
        if not self.token_manager.health_check():
            raise ConnectionError("Token server is not responding")
        
        # Initialize API clients
        self.homefeed_api = HomefeedAPI(
            token_manager=self.token_manager,
            cookies_path=cookies_path
        )
        self.search_api = SearchAPI(
            token_manager=self.token_manager,
            cookies_path=cookies_path
        )
        self.comments_api = CommentsAPI(
            token_manager=self.token_manager,
            cookies_path=cookies_path
        )
        self.feed_api = FeedAPI(
            token_manager=self.token_manager,
            cookies_path=cookies_path
        )
        self.user_api = UserAPI(
            token_manager=self.token_manager,
            cookies_path=cookies_path
        )
        
        # Setup logging
        self.enable_logging = enable_logging
        if enable_logging:
            self.log_dir = Path(log_dir)
            self.log_dir.mkdir(exist_ok=True)
            self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('XHSClient')
    
    def _log_response(self, api_type: str, response: Dict, metadata: Dict = None):
        """Log API response to file"""
        if not self.enable_logging:
            return
        
        timestamp = int(time.time() * 1000)
        filename = f"{api_type}_{timestamp}.json"
        filepath = self.log_dir / filename
        
        log_data = {
            "timestamp": timestamp,
            "api_type": api_type,
            "metadata": metadata or {},
            "response": response
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Response logged to: {filepath}")
    
    # === Homefeed API ===
    
    def get_homefeed(
        self,
        num: int = 20,
        cursor: str = "",
        refresh_type: int = 1
    ) -> Dict[str, Any]:
        """
        Get homefeed posts
        
        Args:
            num: Number of posts to fetch (max 20)
            cursor: Pagination cursor
            refresh_type: 1 for refresh, 3 for load more
            
        Returns:
            API response with posts data
        """
        self.logger.info(f"Fetching homefeed: num={num}, cursor={cursor}")
        
        response = self.homefeed_api.fetch_homefeed(
            cursor_score=cursor,
            num=num,
            refresh_type=refresh_type
        )
        
        self._log_response("homefeed", response, {
            "num": num,
            "cursor": cursor,
            "refresh_type": refresh_type
        })
        
        return response
    
    def get_homefeed_posts(self, num: int = 20) -> List[Dict]:
        """
        Get homefeed posts (simplified)
        
        Returns:
            List of post items
        """
        response = self.get_homefeed(num=num)
        return response.get("data", {}).get("items", [])
    
    # === Search API ===
    
    def search(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
        sort: str = "general"
    ) -> Dict[str, Any]:
        """
        Search for posts
        
        Args:
            keyword: Search keyword
            page: Page number (1-based)
            page_size: Results per page (must be 20)
            sort: Sort order (general, time_descending, popularity_descending)
            
        Returns:
            Search results
        """
        self.logger.info(f"Searching for: {keyword}, page={page}")
        
        response = self.search_api.search_notes(
            keyword=keyword,
            page=page,
            page_size=page_size,
            sort=sort
        )
        
        self._log_response("search", response, {
            "keyword": keyword,
            "page": page,
            "sort": sort
        })
        
        return response
    
    def search_notes(self, keyword: str, num: int = 20, sort: str = "general") -> List[Dict]:
        """
        Search for notes (simplified)
        
        Returns:
            List of search results
        """
        return self.search_api.search(keyword, num, sort)
    
    # === Comments API ===
    
    def get_comments(
        self,
        note_id: str,
        cursor: str = ""
    ) -> Dict[str, Any]:
        """
        Get comments for a note
        
        Args:
            note_id: Note ID
            cursor: Pagination cursor
            
        Returns:
            Comments data
        """
        self.logger.info(f"Fetching comments for note: {note_id}")
        
        response = self.comments_api.fetch_comments(
            note_id=note_id,
            cursor=cursor
        )
        
        self._log_response("comments", response, {
            "note_id": note_id,
            "cursor": cursor
        })
        
        return response
    
    def get_note_comments(self, note_id: str, num: int = 20) -> List[Dict]:
        """
        Get comments for a note (simplified)
        
        Returns:
            List of comments
        """
        comments = self.comments_api.get_comments(note_id, num)
        return [self.comments_api.parse_comment(c) for c in comments]
    
    # === Feed API (Related Posts) ===
    
    def get_related_posts(self, note_id: str, num: int = 10) -> List[Dict]:
        """
        Get posts related to a specific note
        
        Args:
            note_id: Source note ID
            num: Number of related posts to fetch
            
        Returns:
            List of related posts
        """
        self.logger.info(f"Fetching related posts for note: {note_id}")
        
        posts = self.feed_api.get_related_posts(note_id, num)
        
        self._log_response("feed", {"items": posts}, {
            "note_id": note_id,
            "num": num
        })
        
        return posts
    
    # === User API ===
    
    def get_user_posts(self, user_id: str, num: int = 30) -> List[Dict]:
        """
        Get posts from a specific user
        
        Args:
            user_id: User ID
            num: Number of posts to fetch
            
        Returns:
            List of user posts
        """
        self.logger.info(f"Fetching posts for user: {user_id}")
        
        posts = self.user_api.get_user_posts(user_id, num)
        
        self._log_response("user_posts", {"posts": posts}, {
            "user_id": user_id,
            "num": num
        })
        
        return posts
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile information
        
        Args:
            user_id: User ID
            
        Returns:
            User profile data
        """
        self.logger.info(f"Fetching profile for user: {user_id}")
        
        profile = self.user_api.get_user_profile(user_id)
        
        self._log_response("user_profile", profile, {
            "user_id": user_id
        })
        
        return profile
    
    # === Utility Methods ===
    
    def browse_note(self, note_item: Dict) -> Dict[str, Any]:
        """
        Browse a specific note with its comments
        
        Args:
            note_item: Note item from homefeed
            
        Returns:
            Dict with note details and comments
        """
        note_id = note_item.get("id")
        xsec_token = note_item.get("xsec_token")
        
        if not note_id or not xsec_token:
            return {"error": "Missing note_id or xsec_token"}
        
        # Get comments
        comments = self.get_comments(note_id)
        
        return {
            "note": note_item,
            "comments": comments
        }
    
    def extract_note_info(self, note_item: Dict) -> Dict[str, Any]:
        """
        Extract key information from a note item
        
        Args:
            note_item: Note item from API response
            
        Returns:
            Simplified note information
        """
        note_card = note_item.get("note_card", {})
        user_info = note_card.get("user", {})
        interact_info = note_card.get("interact_info", {})
        
        return {
            "id": note_item.get("id"),
            "title": note_card.get("display_title", ""),
            "desc": note_card.get("desc", ""),
            "type": note_card.get("type", ""),
            "author": {
                "nickname": user_info.get("nickname", ""),
                "user_id": user_info.get("user_id", "")
            },
            "stats": {
                "likes": interact_info.get("liked_count", 0),
                "comments": interact_info.get("comment_count", 0),
                "collects": interact_info.get("collected_count", 0),
                "shares": interact_info.get("share_count", 0)
            },
            "has_token": bool(note_item.get("xsec_token"))
        }
    
    def save_response(self, data: Any, filename: str):
        """
        Save API response to file
        
        Args:
            data: Response data
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.logger.info(f"Response saved to: {filename}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get token server statistics"""
        return self.token_manager.get_stats()


# === Example Usage ===

def main():
    """Example usage of XHS Client"""
    
    # Super simple - just need cookies.json!
    client = XHSClient()
    
    print("=== XiaoHongShu API Client Demo ===\n")
    
    # 1. Get homefeed
    print("1. Fetching homefeed...")
    posts = client.get_homefeed_posts(num=5)
    print(f"   ✓ Got {len(posts)} posts\n")
    
    # 2. Display posts
    print("2. Posts summary:")
    for i, post in enumerate(posts):
        info = client.extract_note_info(post)
        print(f"   {i+1}. {info['title']}")
        print(f"      Author: {info['author']['nickname']}")
        print(f"      Stats: {info['stats']['likes']} likes, {info['stats']['comments']} comments")
        print()
    
    # 3. Save data
    print("3. Saving responses...")
    client.save_response(posts, "demo_homefeed.json")
    
    # 4. Show server stats
    print("\n4. Token server stats:")
    stats = client.get_stats()
    print(f"   Client: {stats.get('client')}")
    print(f"   Rate limit: {stats.get('rate_limit')}")
    print(f"   Cache available: {stats.get('cache_available')}")
    
    print("\n✓ Demo complete!")


if __name__ == "__main__":
    main()