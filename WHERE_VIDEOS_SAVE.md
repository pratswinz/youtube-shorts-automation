# Where Your Videos Are Saved 📁

## Video Storage Locations

### 1. **Temporary Files** (During Generation)
```
/Volumes/disc 2/coding/automation/temp/
```

While a video is being created, all temporary files are stored here:
- `temp/<job_id>/` - Each video gets its own folder
  - `script.json` - Generated script
  - `voiceover.mp3` - Generated audio
  - `scene_1.png`, `scene_2.png`, etc. - Generated images
  - `video.mp4` - Final assembled video
  - `thumbnail.jpg` - Video thumbnail

**Auto-cleanup:** Files older than 24 hours are automatically deleted.

---

### 2. **Final Videos** (After Completion)

#### Option A: Telegram Only (Current Setup)
✅ Videos are sent directly to you via **Telegram**
- You receive the video file in your Telegram chat
- You can download it from Telegram
- You can manually upload to YouTube

#### Option B: YouTube Auto-Upload (After Google Cloud Setup)
✅ Videos are automatically uploaded to **YouTube Shorts**
- Direct upload to your YouTube channel
- Thumbnail automatically set
- Title, description, tags automatically added
- You get the YouTube Shorts link via Telegram

---

### 3. **Assets Directory** (Optional - For Reuse)
```
/Volumes/disc 2/coding/automation/assets/
```

You can save:
- Custom background music
- Logo overlays
- Watermarks
- Font files

---

## How to Access Your Videos

### Current Setup (Telegram Only):

1. **Via Telegram:**
   - Open your Telegram bot chat
   - Scroll to completed video message
   - Click download button
   - Video saves to your Downloads folder

2. **From Temp Folder (within 24 hours):**
   ```bash
   cd "/Volumes/disc 2/coding/automation/temp"
   ls -la
   ```
   - Find your job folder
   - Copy `video.mp4` to desired location

---

### After YouTube Setup:

1. **Automatic YouTube Upload:**
   - Video uploads to YouTube Shorts automatically
   - Get YouTube link in Telegram
   - Video is live on your channel!

2. **Also Available via Telegram:**
   - Still get video file in Telegram
   - Can download as backup

---

## Video File Names

Format: `video_<job_id>.mp4`

Example:
```
video_a1b2c3d4-e5f6-7890-abcd-ef1234567890.mp4
```

---

## Storage Management

### Check Temp Folder Size:
```bash
du -sh "/Volumes/disc 2/coding/automation/temp"
```

### Manual Cleanup (if needed):
```bash
cd "/Volumes/disc 2/coding/automation/temp"
rm -rf */  # Removes all temp files
```

### Keep a Video Permanently:
```bash
# Copy from temp before it's auto-deleted
cp temp/<job_id>/video.mp4 ~/Desktop/my_video.mp4
```

---

## Recommended Workflow

### Option 1: Download from Telegram
1. Generate video via bot
2. Download from Telegram to your device
3. Upload to YouTube manually (if needed)
4. Edit/share as desired

### Option 2: Auto-Upload to YouTube
1. Setup Google Cloud (10 minutes)
2. Generate video via bot
3. Video auto-uploads to YouTube
4. Share YouTube link directly!

---

## Storage Space Requirements

Per video:
- Images: ~5-10 MB (5 scenes × 2 MB each)
- Audio: ~1-2 MB (60 seconds)
- Video: ~10-20 MB (60 seconds, 1080x1920)
- Total: ~20-30 MB per video

**With auto-cleanup:** Only active videos stored
**Without cleanup:** ~30 MB × number of videos

---

## Quick Commands

```bash
# View all temp videos
ls -lh temp/*/video.mp4

# Count videos in temp
ls temp/*/video.mp4 | wc -l

# Find latest video
ls -lt temp/*/video.mp4 | head -1

# Copy latest video to Desktop
cp $(ls -t temp/*/video.mp4 | head -1) ~/Desktop/latest_video.mp4
```

---

## Summary

📱 **Current:** Videos sent via Telegram → Download manually
🎬 **After Setup:** Videos auto-upload to YouTube → Get link instantly

Both options work great! Choose what fits your workflow.

