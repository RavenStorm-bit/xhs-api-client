"""
XHS API Client - A Python client for XiaoHongShu (Little Red Book) API

This module provides a clean interface to interact with XiaoHongShu's API
without worrying about token generation or security algorithms.
"""

from .xhs_client import XHSClient
from .token_manager import TokenManager

__version__ = "0.1.0"
__author__ = "XHS API Client Team"
__all__ = ["XHSClient", "TokenManager"]