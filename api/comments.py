"""
Comments API client for XiaoHongShu
"""

from typing import Dict, Any, List
from .base import BaseAPI


class CommentsAPI(BaseAPI):
    """Client for XiaoHongShu Comments API"""
    
    def __init__(self, token_manager, cookies_path: str = "cookies.json"):
        """Initialize Comments API client"""
        super().__init__(token_manager, cookies_path)
        self.endpoint = "/api/sns/web/v2/comment/page"
    
    def fetch_comments(
        self,
        note_id: str,
        cursor: str = "",
        top_comment_id: str = "",
        image_formats: List[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch comments for a note
        
        Args:
            note_id: Note ID
            cursor: Pagination cursor (empty for first page)
            top_comment_id: ID of top comment (optional)
            image_formats: Image format preferences
            
        Returns:
            Comments data
        """
        if image_formats is None:
            image_formats = ["jpg", "webp", "avif"]
        
        payload = {
            "note_id": note_id,
            "cursor": cursor,
            "top_comment_id": top_comment_id,
            "image_formats": image_formats
        }
        
        return self._make_request(self.endpoint, payload)
    
    def get_comments(
        self,
        note_id: str,
        num_comments: int = 20
    ) -> List[Dict]:
        """
        Get comments for a note
        
        Args:
            note_id: Note ID
            num_comments: Number of comments to fetch
            
        Returns:
            List of comments
        """
        all_comments = []
        cursor = ""
        
        while len(all_comments) < num_comments:
            response = self.fetch_comments(
                note_id=note_id,
                cursor=cursor
            )
            
            comments = response.get("data", {}).get("comments", [])
            if not comments:
                break
                
            all_comments.extend(comments)
            
            # Get cursor for next page
            cursor = response.get("data", {}).get("cursor", "")
            if not cursor:
                break
                
            # Check if we have more pages
            if not response.get("data", {}).get("has_more", False):
                break
        
        return all_comments[:num_comments]
    
    def parse_comment(self, comment: Dict) -> Dict[str, Any]:
        """
        Parse comment data into a simpler format
        
        Args:
            comment: Raw comment data
            
        Returns:
            Simplified comment info
        """
        user_info = comment.get("user_info", {})
        
        return {
            "id": comment.get("id"),
            "content": comment.get("content"),
            "user_nickname": user_info.get("nickname", "Anonymous"),
            "user_id": user_info.get("user_id"),
            "like_count": comment.get("like_count", 0),
            "sub_comment_count": comment.get("sub_comment_count", 0),
            "create_time": comment.get("create_time"),
            "ip_location": comment.get("ip_location", ""),
            "pictures": [pic.get("url_default", "") for pic in comment.get("pictures", [])]
        }