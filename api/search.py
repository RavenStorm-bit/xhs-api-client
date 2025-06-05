"""
Search API client for XiaoHongShu
"""

from typing import Dict, Any, List, Optional
from urllib.parse import quote
from .base import BaseAPI


class SearchAPI(BaseAPI):
    """Client for XiaoHongShu Search API"""
    
    def __init__(self, token_manager, cookies_path: str = "cookies.json"):
        """Initialize Search API client"""
        super().__init__(token_manager, cookies_path)
        self.endpoint = "/api/sns/web/v1/search/notes"
    
    def search_notes(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
        sort: str = "general",
        note_type: int = 0,
        search_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for notes
        
        Args:
            keyword: Search keyword
            page: Page number (1-based)
            page_size: Results per page (must be 20)
            sort: Sort order ('general', 'time_descending', 'popularity_descending')
            note_type: Note type filter (0 for all)
            search_id: Search session ID (optional)
            
        Returns:
            Search results
        """
        # Generate search_id if not provided
        if not search_id:
            import uuid
            search_id = str(uuid.uuid4()).replace('-', '')
        
        payload = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "search_id": search_id,
            "sort": sort,
            "note_type": note_type,
            "ext_flags": [],
            "image_scenes": "FD_PRV_WEBP,FD_WM_WEBP"
        }
        
        return self._make_request(self.endpoint, payload)
    
    def search(
        self,
        keyword: str,
        num_results: int = 20,
        sort: str = "general"
    ) -> List[Dict]:
        """
        Simple search interface
        
        Args:
            keyword: Search keyword
            num_results: Total number of results to fetch
            sort: Sort order
            
        Returns:
            List of search results
        """
        all_results = []
        page = 1
        search_id = None
        
        while len(all_results) < num_results:
            response = self.search_notes(
                keyword=keyword,
                page=page,
                sort=sort,
                search_id=search_id
            )
            
            # Extract search_id for consistent results
            if not search_id and response.get("data"):
                search_id = response["data"].get("search_id")
            
            items = response.get("data", {}).get("items", [])
            if not items:
                break
                
            all_results.extend(items)
            page += 1
            
            # Check if we have more pages
            if not response.get("data", {}).get("has_more", False):
                break
        
        # Return only requested number of results
        return all_results[:num_results]