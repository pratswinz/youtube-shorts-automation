# YouTube Shorts Automation - Setup Complete! 🎉

## ✅ What's Working

### Core Features
- ✅ **Script Generation** - Groq API with Llama 3.3 (free)
- ✅ **Text-to-Speech** - Edge TTS with female sweet voices (all languages)
- ✅ **Image Generation** - PiAPI with FLUX model (paid, high quality)
- ✅ **Video Assembly** - FFmpeg (local binary)
- ✅ **Telegram Bot** - Full integration with job queue
- ✅ **No Subtitles** - Removed from videos as requested
- ✅ **No Text Overlays** - Images are pure visuals without text
- ✅ **Content Safety** - Detects sensitive content and warns users
- ✅ **Multi-language** - Supports Hindi, English, and more

### Recent Fixes
- ✅ PiAPI model name corrected to `Qubico/flux1-dev`
- ✅ Video resolution adjusted to 720x1280 (PiAPI's max limit)
- ✅ FFmpeg path configured correctly
- ✅ Female voices configured for all languages
- ✅ Text overlays removed from image prompts
- ✅ Subtitles completely removed from video assembly

## 📋 Configuration

### Video Settings
- **Resolution**: 720x1280 (9:16 aspect ratio for Shorts)
- **Format**: MP4 (H.264)
- **FPS**: 30
- **Duration**: 30-60 seconds (configurable)

### API Keys Configured
- ✅ Telegram Bot Token
- ✅ Groq API Key (free tier)
- ✅ PiAPI API Key

### Providers
- **Script**: Groq (free)
- **TTS**: Edge TTS (free, no API key needed)
- **Images**: PiAPI (paid, $0.015 per image with flux1-dev)
- **Video**: FFmpeg (free, local binary)

## 🚀 How to Start the Bot

### Option 1: Using the Startup Script (Recommended)
```bash
cd "/Volumes/disc 2/coding/automation"
./start_bot.sh
```

This script will:
1. Kill any existing bot processes
2. Clear Telegram state
3. Wait 3 minutes for Telegram to release
4. Start the bot

### Option 2: Manual Start
```bash
cd "/Volumes/disc 2/coding/automation"
source venv/bin/activate

# Kill existing processes
pkill -9 -f "python main.py"

# Clear Telegram
python clear_telegram.py

# Wait 3 minutes
sleep 180

# Start bot
python main.py
```

## 💬 Using the Bot in Telegram

### Commands
- `/start` - Start the bot and see welcome message
- `/create <topic>` - Create a video (e.g., `/create benefits of eggs in hindi`)
- `/status <job_id>` - Check video generation status
- `/help` - Show help message

### Example Usage
```
/create benefits of drinking water in hindi
/create funny cat moments in english
/create healthy breakfast ideas
```

## ⚠️ Important Notes

### Telegram Conflicts
If you see "Conflict: terminated by other getUpdates request":
1. **Close Telegram on ALL devices** (phone, computer, browser tabs)
2. Wait **5 minutes**
3. Run `./start_bot.sh` again

### PiAPI Resolution Limit
- PiAPI has a maximum resolution of 1024x1024 pixels (width × height ≤ 1,048,576)
- We're using 720x1280 which is within this limit
- If you need 1080x1920, you'll need to use Pollinations (free but unreliable)

### Switching to Pollinations (Free Alternative)
Edit `.env` and change:
```bash
IMAGE_PROVIDER=pollinations
```

Note: Pollinations is free but has rate limits and may fail sometimes.

## 📁 Project Structure

```
automation/
├── main.py                 # Main entry point
├── start_bot.sh           # Startup script
├── clear_telegram.py      # Telegram state clearer
├── .env                   # Configuration (API keys, settings)
├── requirements.txt       # Python dependencies
├── bin/
│   └── ffmpeg            # FFmpeg binary
├── core/
│   ├── video_generator.py    # Main video generation orchestrator
│   ├── job_queue.py          # Job queue management
│   ├── content_analyzer.py   # Content analysis and language detection
│   ├── prompt_generator.py   # AI image prompt generation
│   ├── content_safety.py     # Content safety checks
│   └── video_assembler.py    # FFmpeg video assembly
├── bot/
│   └── telegram_bot.py       # Telegram bot handlers
├── providers/
│   ├── script_provider.py    # Script generation (Groq)
│   ├── tts_provider.py       # Text-to-speech (Edge TTS)
│   └── image_provider.py     # Image generation (PiAPI/Pollinations)
├── config/
│   ├── settings.py           # Pydantic settings
│   └── constants.py          # Constants and enums
├── temp/                     # Temporary job files
└── output/                   # Final videos

```

## 🧪 Testing

### Test Video Generation (Without Telegram)
```bash
source venv/bin/activate
python test_video_direct.py
```

### Test PiAPI Image Generation
```bash
source venv/bin/activate
python test_piapi.py
```

## 🐛 Troubleshooting

### Bot Won't Start
- Check if another instance is running: `ps aux | grep "python main.py"`
- Kill all instances: `pkill -9 -f "python main.py"`
- Clear Telegram: `python clear_telegram.py`
- Wait 5 minutes before restarting

### Videos Not Generating
- Check logs in the terminal output
- Verify API keys in `.env`
- Check `temp/` directory for partial files
- Ensure FFmpeg is accessible: `./bin/ffmpeg -version`

### PiAPI Errors
- Verify API key is correct
- Check account balance/credits
- Ensure resolution is ≤ 1024x1024 pixels (720x1280 works)

### Pollinations Rate Limits
- Pollinations is free but has rate limits (429 errors)
- The system will use fallback placeholder images if it fails
- Consider using PiAPI for production

## 💰 Cost Estimate

### Per Video (assuming 7 scenes):
- **Script Generation**: Free (Groq)
- **Text-to-Speech**: Free (Edge TTS)
- **Images**: $0.105 (7 images × $0.015 with PiAPI flux1-dev)
- **Video Assembly**: Free (FFmpeg)
- **Total**: ~$0.11 per video

### Free Alternative:
Use Pollinations for images → **$0.00 per video** (but less reliable)

## 📝 Next Steps

1. **Test the bot** with a simple topic
2. **Monitor the console** for any errors
3. **Check generated videos** in `output/` directory
4. **Adjust settings** in `.env` as needed
5. **Consider YouTube upload** (currently disabled, can be enabled later)

## 🎯 Features to Add Later

- YouTube automatic upload
- Video thumbnail generation
- Multiple video formats (Reels, TikTok)
- Custom voice selection
- Video editing (transitions, effects)
- Analytics and tracking

---

**Status**: ✅ Ready for Production
**Last Updated**: March 17, 2026
**Version**: 1.0.0
