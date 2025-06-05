"""
XHS API Modules

Individual API clients for different XiaoHongShu endpoints.
"""

from .base import BaseAPI
from .homefeed import HomefeedAPI
from .search import SearchAPI
from .comments import CommentsAPI
from .feed import FeedAPI
# from .user import UserAPI  # TODO: Implement user endpoints

__all__ = [
    "BaseAPI",
    "HomefeedAPI", 
    "SearchAPI",
    "CommentsAPI",
    "FeedAPI",
    # "UserAPI"  # TODO: Implement user endpoints
]