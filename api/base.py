"""
Base API class for all XHS API clients
"""

import json
import os
from typing import Dict, Optional, Any
from curl_cffi import requests


class BaseAPI:
    """Base class for all XHS API clients"""
    
    def __init__(self, token_manager, cookies_path: str = "cookies.json"):
        """
        Initialize base API client
        
        Args:
            token_manager: TokenManager instance for token generation
            cookies_path: Path to cookies.json file
        """
        self.token_manager = token_manager
        self.base_url = "https://edith.xiaohongshu.com"
        self.session = requests.Session(impersonate="chrome")
        
        # Load cookies
        self.cookies = self._load_cookies(cookies_path)
        
        # Extract device ID from cookies
        self.a1 = self._extract_device_id()
        
    def _load_cookies(self, cookies_path: str) -> Dict[str, str]:
        """Load cookies from file"""
        if not os.path.exists(cookies_path):
            raise FileNotFoundError(f"Cookies file not found: {cookies_path}")
            
        with open(cookies_path, 'r') as f:
            cookies_data = json.load(f)
            
        # Convert to dict format
        if isinstance(cookies_data, list):
            return {cookie['name']: cookie['value'] for cookie in cookies_data}
        return cookies_data
    
    def _extract_device_id(self) -> str:
        """Extract device ID (a1) from cookies"""
        a1 = self.cookies.get('a1', '')
        if not a1:
            raise ValueError("Device ID (a1) not found in cookies")
        return a1
    
    def _build_headers(self, endpoint: str, x_s: str, x_s_common: str, x_t: int) -> Dict[str, str]:
        """Build request headers"""
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.xiaohongshu.com",
            "referer": "https://www.xiaohongshu.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "x-s": x_s,
            "x-s-common": x_s_common,
            "x-t": str(x_t)
        }
    
    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API request with automatic token generation
        
        Args:
            endpoint: API endpoint path
            payload: Request payload
            
        Returns:
            API response as dict
        """
        # Get tokens from server
        x_s, timestamp = self.token_manager.get_xs_token(endpoint, payload, self.a1)
        x_s_common = self.token_manager.get_xs_common_token(self.a1)
        
        # Build headers
        headers = self._build_headers(endpoint, x_s, x_s_common, timestamp)
        
        # Make request
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(
            url,
            headers=headers,
            cookies=self.cookies,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
            
        return response.json()