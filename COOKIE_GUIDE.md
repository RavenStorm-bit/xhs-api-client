# How to Get Your XiaoHongShu Cookies

## Quick Guide

### Step 1: Login to XiaoHongShu
1. Open https://www.xiaohongshu.com in Chrome/Firefox
2. Login with your account

### Step 2: Install Cookie Extension
Choose one:
- **Chrome**: [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
- **Firefox**: [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- **Chrome**: [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)

### Step 3: Export Cookies
1. Click the extension icon while on xiaohongshu.com
2. Click "Export" → "JSON"
3. Copy all cookies

### Step 4: Save as cookies.json
1. Create a file named `cookies.json` in the project folder
2. Paste the cookies
3. Save the file

## What Your cookies.json Should Look Like

```json
[
  {
    "domain": ".xiaohongshu.com",
    "name": "a1",
    "value": "YOUR_52_CHARACTER_DEVICE_ID_HERE",
    "path": "/",
    "httpOnly": false,
    "secure": true
  },
  {
    "domain": ".xiaohongshu.com", 
    "name": "web_session",
    "value": "YOUR_SESSION_TOKEN_HERE",
    "path": "/",
    "httpOnly": true,
    "secure": true
  },
  // ... more cookies
]
```

## Important Cookies

The most important cookie is **`a1`** - your device ID. It should be 52 characters long.

## Troubleshooting

### "No posts returned"
- Your cookies might be expired
- Re-export fresh cookies after logging in

### "Device ID (a1) is required"
- Make sure your cookies.json includes the `a1` cookie
- Check that it's 52 characters long

### Cookie Expiration
- Cookies typically last 7-30 days
- Re-export when they expire

## Privacy Note
- Your cookies are like passwords
- Never share your cookies.json file
- Only use cookies from your own account