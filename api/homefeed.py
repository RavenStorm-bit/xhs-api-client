"""
Homefeed API client for XiaoHongShu
"""

from typing import Dict, Any, List
from .base import BaseAPI


class HomefeedAPI(BaseAPI):
    """Client for XiaoHongShu Homefeed API"""
    
    def __init__(self, token_manager, cookies_path: str = "cookies.json"):
        """Initialize Homefeed API client"""
        super().__init__(token_manager, cookies_path)
        self.endpoint = "/api/sns/web/v1/homefeed"
    
    def fetch_homefeed(
        self,
        cursor_score: str = "",
        num: int = 20,
        refresh_type: int = 1,
        note_index: int = 0
    ) -> Dict[str, Any]:
        """
        Fetch homefeed posts
        
        Args:
            cursor_score: Pagination cursor (empty for first page)
            num: Number of posts to fetch (max 20)
            refresh_type: 1 for refresh, 3 for load more
            note_index: Note index for pagination
            
        Returns:
            API response with posts data
        """
        payload = {
            "cursor_score": cursor_score,
            "num": num,
            "refresh_type": refresh_type,
            "note_index": note_index,
            "image_scenes": ["CRD_PRV_WEBP", "CRD_WM_WEBP"]
        }
        
        return self._make_request(self.endpoint, payload)
    
    def get_posts(self, num: int = 20, pages: int = 1) -> List[Dict]:
        """
        Get multiple pages of homefeed posts
        
        Args:
            num: Posts per page (max 20)
            pages: Number of pages to fetch
            
        Returns:
            List of all fetched posts
        """
        all_posts = []
        cursor = ""
        
        for _ in range(pages):
            response = self.fetch_homefeed(
                cursor_score=cursor,
                num=num,
                refresh_type=3 if cursor else 1
            )
            
            posts = response.get("data", {}).get("items", [])
            if not posts:
                break
                
            all_posts.extend(posts)
            
            # Get cursor for next page
            cursor = response.get("data", {}).get("cursor_score", "")
            if not cursor:
                break
                
        return all_posts