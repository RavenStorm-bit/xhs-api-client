# XHS API Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A secure Python client for XiaoHongShu (Little Red Book / 小红书) API with token server architecture.

## 🎯 Try It Now!

```bash
# Test the demo server
python test_server.py

# Run the interactive demo
python demo.py
```

We provide a **demo token server** for testing! You can immediately see how the API works without setting up your own server. The demo server has rate limits - for production use, you'll need to deploy your own server.

## 🚨 Important Notice

This client requires a **token generation server** that handles the authentication algorithms. You can:
- Use our demo server for testing (included in demo.py)
- Deploy your own token server for production use
- Contact us for dedicated server access

## Features

### 🔐 Secure Architecture
- Token generation algorithms remain on secure server
- Client never sees the implementation details
- API key authentication for access control
- HTTPS support with self-signed certificates

### 📱 API Support
- **Homefeed**: Browse the main content feed
- **Search**: Search for posts by keywords
- **Feed**: Get related/recommended content
- **Comments**: Read post comments and discussions

### 🚀 Performance
- Token caching to reduce server requests
- Connection pooling for better performance
- Automatic retry logic with exponential backoff
- Response time: ~10ms for cached tokens

## Installation

```bash
# Clone the repository
git clone https://github.com/RavenStorm-bit/xhs-api-client.git
cd xhs-api-client

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- `requests` - HTTP client library
- `curl-cffi` - For bypassing anti-bot detection
- `pycryptodome` - Required by server (not client)

## Quick Start

### 🚀 Try the Demo First!

```bash
# See it in action immediately
python demo.py
```

### 1. Initialize Token Manager

```python
from token_manager import TokenManager

# For testing - use our demo server
token_manager = TokenManager(
    server_url="https://31.97.132.244:8443",  # Demo server
    api_key="dev-key-123"                      # Demo API key
)

# For production - use your own server
token_manager = TokenManager(
    server_url="https://your-token-server.com:8443",
    api_key="your-api-key"
)
```

### 2. Use API Clients

#### Homefeed API
```python
from homefeed_refactored import HomefeedAPI

# Initialize with token manager
api = HomefeedAPI(
    token_manager=token_manager,
    cookies_path="cookies.json"  # XiaoHongShu cookies
)

# Fetch homefeed
result = api.fetch_homefeed(num=20)
items = result.get("data", {}).get("items", [])

for item in items:
    note_card = item.get("note_card", {})
    print(f"Title: {note_card.get('display_title')}")
    print(f"Author: {note_card.get('user', {}).get('nickname')}")
```

#### Search API
```python
from search_client import SearchAPI

api = SearchAPI(token_manager, cookies_path="cookies.json")

# Search for content
results = api.search(
    keyword="Python programming",
    page=1,
    sort="popularity_descending"
)
```

#### Comments API
```python
from comments_client import CommentsAPI

api = CommentsAPI(token_manager, cookies_path="cookies.json")

# Get comments (requires note_id and xsec_token from homefeed)
comments = api.get_comments(
    note_id="note_id_here",
    xsec_token="token_from_homefeed"
)
```

## Configuration

### Cookies
The client requires valid XiaoHongShu cookies. Export them from your browser:

1. Login to xiaohongshu.com
2. Export cookies using browser extension
3. Save as `cookies.json` in the format:
```json
[
  {
    "name": "cookie_name",
    "value": "cookie_value",
    "domain": ".xiaohongshu.com"
  }
]
```

### Token Server
Set up your token server URL and API key:

```python
# For development
token_manager = TokenManager(
    server_url="http://localhost:8000",
    api_key="dev-key-123"
)

# For production with HTTPS
token_manager = TokenManager(
    server_url="https://api.your-domain.com",
    api_key="prod-key-xxx"
)
```

## Advanced Usage

### Pagination
```python
# Fetch multiple pages
all_items = api.fetch_multiple_pages(total_items=100)
```

### Error Handling
```python
try:
    result = api.fetch_homefeed()
    if "error" in result:
        print(f"API Error: {result['error']}")
except Exception as e:
    print(f"Request failed: {e}")
```

### Logging Responses
```python
# Save responses for debugging
result = api.fetch_homefeed()

# Save to file
import json
with open("homefeed_response.json", "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
```

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 300031 | 当前笔记暂时无法浏览 | Use correct xsec_token from homefeed |
| -1 | Generic error | Check cookies validity |
| 461 | Access denied | Note may be deleted or private |

## Best Practices

1. **Always use xsec_token from homefeed** - Each note has its own token
2. **Cache responses** - Save API responses for debugging
3. **Handle rate limits** - Add delays between requests
4. **Update cookies regularly** - Cookies expire after some time

## Security Notes

- Never expose your API keys in code
- Use environment variables for sensitive data
- The token generation algorithms are kept secure on the server
- Client code can be safely open-sourced

## Examples

See the `examples/` directory for usage examples:
- `quick_start.py` - Basic usage example

More examples coming soon!

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

This is an unofficial API client. Use responsibly and respect XiaoHongShu's terms of service.