# Google Cloud Setup - Step by Step (10 minutes)

## What You'll Get

✅ Free Text-to-Speech (1M characters/month)
✅ Automatic YouTube upload
✅ Better voice quality than Edge TTS

---

## Step 1: Create Google Cloud Project (2 minutes)

1. Visit: https://console.cloud.google.com/
2. Click "Select a project" (top left)
3. Click "NEW PROJECT"
4. Project name: `youtube-automation`
5. Click "CREATE"
6. Wait for project to be created
7. **Copy the Project ID** (looks like: `youtube-automation-123456`)

---

## Step 2: Enable APIs (2 minutes)

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Cloud Text-to-Speech API"
   - Click on it
   - Click "ENABLE"
   - Wait for it to enable
3. Search for "YouTube Data API v3"
   - Click on it
   - Click "ENABLE"
   - Wait for it to enable

---

## Step 3: Create Service Account (3 minutes)

This is for Text-to-Speech:

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "CREATE SERVICE ACCOUNT"
3. Service account name: `tts-service`
4. Click "CREATE AND CONTINUE"
5. Role: Select "Cloud Text-to-Speech User"
6. Click "CONTINUE"
7. Click "DONE"
8. Click on the service account you just created
9. Go to "KEYS" tab
10. Click "ADD KEY" → "Create new key"
11. Choose "JSON"
12. Click "CREATE"
13. A JSON file will download
14. **Rename it to:** `google_cloud_key.json`
15. **Move it to:** `config/credentials/google_cloud_key.json`

---

## Step 4: Create OAuth Credentials (3 minutes)

This is for YouTube upload:

1. Go to "APIs & Services" → "Credentials"
2. Click "CREATE CREDENTIALS" → "OAuth client ID"
3. If prompted to configure consent screen:
   - Click "CONFIGURE CONSENT SCREEN"
   - User Type: **External**
   - Click "CREATE"
   - App name: `YouTube Automation`
   - User support email: Your email
   - Developer contact: Your email
   - Click "SAVE AND CONTINUE"
   - Scopes: Click "SAVE AND CONTINUE" (no changes)
   - Test users: Click "ADD USERS" → Add your email
   - Click "SAVE AND CONTINUE"
   - Click "BACK TO DASHBOARD"
4. Go back to "Credentials" → "CREATE CREDENTIALS" → "OAuth client ID"
5. Application type: **Desktop app**
6. Name: `youtube-uploader`
7. Click "CREATE"
8. Click "DOWNLOAD JSON"
9. **Rename it to:** `youtube_oauth.json`
10. **Move it to:** `config/credentials/youtube_oauth.json`

---

## Step 5: Update .env (1 minute)

Open .env:
```bash
nano .env
```

Update these lines:
```env
# Add your Google Project ID
GOOGLE_PROJECT_ID=youtube-automation-123456

# Switch to Google TTS (better quality)
TTS_PROVIDER=google

# Enable YouTube upload
YOUTUBE_UPLOAD_ENABLED=true
```

Save: Ctrl+X, Y, Enter

---

## Step 6: Verify Files (1 minute)

Check that both files exist:
```bash
ls -la config/credentials/
```

You should see:
```
google_cloud_key.json
youtube_oauth.json
```

---

## Step 7: Test & Start

```bash
# Test providers
source venv/bin/activate
python test_providers.py

# Start bot
./start.sh
```

---

## First YouTube Upload

When you create your first video:

1. Send prompt via Telegram
2. Bot generates video
3. Bot will open browser for YouTube OAuth
4. Sign in with your YouTube account
5. Grant permissions
6. Video uploads automatically!
7. Get YouTube Shorts link!

**After first time, uploads are automatic (no browser needed).**

---

## Troubleshooting

### "Credentials not found"
```bash
ls config/credentials/
# Should show both JSON files
```

### "API not enabled"
- Go to console.cloud.google.com
- APIs & Services → Library
- Enable both APIs

### "OAuth error"
- Make sure you added yourself as test user
- Use the same Google account for YouTube

---

## What You Get

✅ **Better voice quality** - Google Neural2 voices
✅ **Automatic YouTube upload** - Direct to Shorts
✅ **Custom thumbnails** - Auto-uploaded
✅ **Still 100% FREE** - Within free tier limits

---

**Total time: 10 minutes**
**Cost: $0.00 (free tier)**
**Result: Professional YouTube Shorts automation!**

