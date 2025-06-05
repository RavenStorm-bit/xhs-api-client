"""
User API client for XiaoHongShu
"""

from typing import Dict, Any, List, Optional
from .base import BaseAPI


class UserAPI(BaseAPI):
    """Client for XiaoHongShu User API"""
    
    def __init__(self, token_manager, cookies_path: str = "cookies.json"):
        """Initialize User API client"""
        super().__init__(token_manager, cookies_path)
        self.user_posted_endpoint = "/api/sns/web/v1/user_posted"
        self.user_info_endpoint = "/api/sns/web/v1/user/otherinfo"
    
    def fetch_user_posts(
        self,
        user_id: str,
        cursor: str = "",
        num: int = 30,
        image_formats: List[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch posts from a specific user
        
        Args:
            user_id: User ID
            cursor: Pagination cursor
            num: Number of posts to fetch (max 30)
            image_formats: Image format preferences
            
        Returns:
            User posts data
        """
        if image_formats is None:
            image_formats = ["jpg", "webp", "avif"]
        
        payload = {
            "user_id": user_id,
            "cursor": cursor,
            "num": num,
            "image_formats": image_formats
        }
        
        return self._make_request(self.user_posted_endpoint, payload)
    
    def fetch_user_info(
        self,
        user_id: str,
        target_user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch user profile information
        
        Args:
            user_id: User ID to fetch
            target_user_id: Optional target user ID for relationship info
            
        Returns:
            User profile data
        """
        payload = {
            "user_id": user_id
        }
        
        if target_user_id:
            payload["target_user_id"] = target_user_id
        
        return self._make_request(self.user_info_endpoint, payload)
    
    def get_user_posts(
        self,
        user_id: str,
        num_posts: int = 30
    ) -> List[Dict]:
        """
        Get all posts from a user
        
        Args:
            user_id: User ID
            num_posts: Total number of posts to fetch
            
        Returns:
            List of user posts
        """
        all_posts = []
        cursor = ""
        
        while len(all_posts) < num_posts:
            response = self.fetch_user_posts(
                user_id=user_id,
                cursor=cursor,
                num=min(30, num_posts - len(all_posts))
            )
            
            notes = response.get("data", {}).get("notes", [])
            if not notes:
                break
                
            all_posts.extend(notes)
            
            # Get cursor for next page
            cursor = response.get("data", {}).get("cursor", "")
            if not cursor:
                break
                
            # Check if we have more pages
            if not response.get("data", {}).get("has_more", False):
                break
        
        return all_posts[:num_posts]
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile information
        
        Args:
            user_id: User ID
            
        Returns:
            User profile info
        """
        response = self.fetch_user_info(user_id)
        user_data = response.get("data", {})
        
        return {
            "user_id": user_data.get("user_id"),
            "nickname": user_data.get("nickname"),
            "desc": user_data.get("desc", ""),
            "gender": user_data.get("gender", 0),
            "follows": user_data.get("follows", 0),
            "fans": user_data.get("fans", 0),
            "interaction": user_data.get("interaction", 0),
            "note_count": user_data.get("notes", 0),
            "collected_count": user_data.get("collected", 0),
            "avatar": user_data.get("image", ""),
            "level": user_data.get("level", {}).get("name", ""),
            "location": user_data.get("location", ""),
            "college": user_data.get("college", {}).get("name", "")
        }