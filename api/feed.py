"""
Feed API client for XiaoHongShu (Related/Recommended posts)
"""

from typing import Dict, Any, List
from .base import BaseAPI


class FeedAPI(BaseAPI):
    """Client for XiaoHongShu Feed API"""
    
    def __init__(self, token_manager, cookies_path: str = "cookies.json"):
        """Initialize Feed API client"""
        super().__init__(token_manager, cookies_path)
        self.endpoint = "/api/sns/web/v1/feed"
    
    def fetch_related_posts(
        self,
        note_id: str,
        xsec_token: str,
        num: int = 10,
        ads_per_flow: int = 0,
        tag_info: Dict = None
    ) -> Dict[str, Any]:
        """
        Fetch related/recommended posts for a specific note
        
        Args:
            note_id: Source note ID
            num: Number of posts to fetch
            ads_per_flow: Number of ads per flow (usually 0)
            tag_info: Tag information (optional)
            
        Returns:
            Related posts data
        """
        payload = {
            "source_note_id": note_id,
            "image_scenes": ["CRD_PRV_WEBP", "CRD_WM_WEBP"],
            "num": num,
            "ads_per_flow": ads_per_flow,
            "xsec_source": "pc_feed",
            "xsec_token": xsec_token
        }
        
        if tag_info:
            payload["tag_info"] = tag_info
        
        return self._make_request(self.endpoint, payload)
    
    def get_related_posts(
        self,
        note_id: str,
        xsec_token: str,
        num_posts: int = 20
    ) -> List[Dict]:
        """
        Get related posts for a note
        
        Args:
            note_id: Source note ID
            num_posts: Total number of posts to fetch
            
        Returns:
            List of related posts
        """
        # The feed API usually returns all requested posts in one call
        response = self.fetch_related_posts(
            note_id=note_id,
            xsec_token=xsec_token,
            num=min(num_posts, 30)  # API limit
        )
        
        items = response.get("data", {}).get("items", [])
        return items[:num_posts]
    
    def extract_tag_info(self, note_item: Dict) -> Dict[str, Any]:
        """
        Extract tag information from a note for better recommendations
        
        Args:
            note_item: Note item from homefeed or search
            
        Returns:
            Tag info dict
        """
        note_card = note_item.get("note_card", {})
        tag_list = note_card.get("tag_list", [])
        
        return {
            "tags": [{"id": tag.get("id"), "name": tag.get("name")} for tag in tag_list],
            "type": note_card.get("type", "normal")
        }