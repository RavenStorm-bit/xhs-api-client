# Quick Start Guide

## 🚀 Run in 30 Seconds

### 1. Clone and Install

```bash
git clone https://github.com/RavenStorm-bit/xhs-api-client.git
cd xhs-api-client
pip install -r requirements.txt
```

### 2. Test the Demo Server

```bash
python test_server.py
```

You should see:
```
✅ Server is healthy!
✅ Token generated successfully!
✅ All tests completed!
```

### 3. Run the Interactive Demo

```bash
python demo.py
```

This will show you:
- How tokens are generated
- What the tokens look like
- How they're used in API requests
- Live server statistics

## 🍪 To Access Real Data

The demo shows token generation, but to fetch actual XiaoHongShu content, you need cookies:

1. **Login to XiaoHongShu**
   - Go to https://www.xiaohongshu.com
   - Login with your account

2. **Export Cookies**
   - Use a browser extension like "Cookie-Editor" or "EditThisCookie"
   - Export all cookies for domain `.xiaohongshu.com`
   - Save as `cookies.json` in the project directory

3. **Run Demo Again**
   ```bash
   python demo.py
   ```
   
   Now you'll see actual posts from XiaoHongShu!

## 📊 Example Output

```
=== XHS API Client - Live Demo ===

1. Initializing Token Manager...
   ✅ Token server is online!

2. Generating Tokens...
   ✅ X-S-Common token received in 42ms
   Token preview: 2UQAPsHCPsIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pa...
   
   ✅ X-S token received in 15ms
   Token preview: XYW_eyJzaWduU3ZuIjoiNTYiLCJzaWduVHlwZSI6IngyIiw...

3. Testing API Call...
   ✅ Successfully fetched 3 posts!
   
   Sample posts:
   1. 深圳美食探店｜这家火锅太好吃了...
      Author: 美食博主小王
      Likes: 2,341
```

## 🎯 What's Next?

1. **Explore the Client**
   ```python
   from xhs_client import XHSClient
   
   client = XHSClient(
       token_server_url="https://31.97.132.244:8443",
       api_key="dev-key-123",
       cookies_path="cookies.json"
   )
   
   # Get trending posts
   posts = client.get_homefeed_posts(num=50)
   ```

2. **Save Data**
   ```python
   # Save posts for analysis
   client.save_response(posts, "trending_posts.json")
   ```

3. **Deploy Your Own Server**
   - The demo server has rate limits
   - For production use, deploy your own token server
   - Contact us for server implementation details

## 🆘 Troubleshooting

**SSL Certificate Warning**
- Normal for demo server (self-signed certificate)
- The client handles this automatically

**No Posts Retrieved**
- Make sure cookies.json is valid
- Cookies expire - re-export if needed

**Rate Limit Exceeded**
- Demo server allows 1000 requests/hour
- Wait a bit or deploy your own server

## 💡 Tips

- Star ⭐ the repo to stay updated
- Check `examples/` for more code samples
- Read the full README for API documentation
- Join discussions in Issues section

Happy coding! 🎉