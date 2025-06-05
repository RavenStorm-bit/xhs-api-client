#!/usr/bin/env python3
"""
Token Manager for XHS API Client

This module handles communication with the token generation server,
including caching and error handling.
"""

import time
import json
from typing import Dict, Any, Optional, Tuple
import requests
from datetime import datetime, timedelta


class TokenManager:
    """Manages token generation requests to the secure token server"""
    
    def __init__(self, server_url: str, api_key: str, cache_xs_common: bool = True):
        """
        Initialize TokenManager
        
        Args:
            server_url: Base URL of the token generation server
            api_key: API key for authentication
            cache_xs_common: Whether to cache X-S-Common tokens locally
        """
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.cache_xs_common = cache_xs_common
        self._xs_common_cache: Dict[str, dict] = {}
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        
        # Disable SSL verification for self-signed certificates
        # In production, use proper certificates or set verify='/path/to/cert'
        if server_url.startswith('https') and '31.97.132.244' in server_url:
            self.session.verify = False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_xs_token(self, endpoint: str, payload: Dict[str, Any], 
                     a1: Optional[str] = None, timestamp_ms: Optional[int] = None) -> Tuple[str, int]:
        """
        Get X-S token from server
        
        Args:
            endpoint: API endpoint (e.g., "/api/sns/web/v1/homefeed")
            payload: Request payload as dictionary
            a1: Device ID (optional)
            timestamp_ms: Timestamp in milliseconds (optional)
            
        Returns:
            Tuple of (x_s_token, timestamp)
        """
        url = f"{self.server_url}/api/v1/tokens/xs"
        
        request_data = {
            "endpoint": endpoint,
            "payload": payload
        }
        
        if a1:
            request_data["a1"] = a1
        if timestamp_ms:
            request_data["timestamp_ms"] = timestamp_ms
        
        try:
            response = self.session.post(url, json=request_data, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return data["x_s"], data["x_t"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get X-S token: {str(e)}")
    
    def get_xs_common_token(self, a1: Optional[str] = None, 
                           fingerprint: Optional[Dict[str, Any]] = None) -> str:
        """
        Get X-S-Common token from server (with caching)
        
        Args:
            a1: Device ID (optional)
            fingerprint: Browser fingerprint data (optional)
            
        Returns:
            X-S-Common token string
        """
        # Create cache key
        cache_key = f"{a1 or 'default'}:{json.dumps(fingerprint or {}, sort_keys=True)}"
        
        # Check local cache
        if self.cache_xs_common and cache_key in self._xs_common_cache:
            cached = self._xs_common_cache[cache_key]
            # Check if not expired
            if cached["expires_at"] > int(time.time() * 1000):
                return cached["token"]
        
        # Request from server
        url = f"{self.server_url}/api/v1/tokens/xs-common"
        
        request_data = {}
        if a1:
            request_data["a1"] = a1
        if fingerprint:
            request_data["fingerprint"] = fingerprint
        
        try:
            response = self.session.post(url, json=request_data, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            token = data["x_s_common"]
            
            # Cache locally
            if self.cache_xs_common:
                self._xs_common_cache[cache_key] = {
                    "token": token,
                    "expires_at": data["expires_at"]
                }
            
            return token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get X-S-Common token: {str(e)}")
    
    def clear_cache(self):
        """Clear local token cache"""
        self._xs_common_cache.clear()
    
    def health_check(self) -> bool:
        """
        Check if token server is healthy
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.server_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get token generation statistics from server"""
        try:
            response = self.session.get(f"{self.server_url}/api/v1/stats", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get stats: {str(e)}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


# Example usage
if __name__ == "__main__":
    # Initialize token manager
    token_manager = TokenManager(
        server_url="http://localhost:8000",
        api_key="your-api-key"
    )
    
    # Check server health
    if token_manager.health_check():
        print("✓ Token server is healthy")
    else:
        print("✗ Token server is not responding")
        exit(1)
    
    # Get X-S-Common token (will be cached)
    print("\nGetting X-S-Common token...")
    xs_common = token_manager.get_xs_common_token()
    print(f"X-S-Common: {xs_common[:50]}...")
    
    # Get X-S token for a request
    print("\nGetting X-S token...")
    xs, timestamp = token_manager.get_xs_token(
        endpoint="/api/sns/web/v1/homefeed",
        payload={"cursor_score": "", "num": 20}
    )
    print(f"X-S: {xs[:50]}...")
    print(f"Timestamp: {timestamp}")
    
    # Get stats
    print("\nServer stats:")
    stats = token_manager.get_stats()
    print(json.dumps(stats, indent=2))