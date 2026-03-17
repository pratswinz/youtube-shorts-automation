# 🎬 YouTube Shorts Automation Bot

Fully automated YouTube Shorts and Instagram Reels creation system via Telegram. Create professional short-form videos from simple text prompts in 12+ languages.

## ✨ Features

- 🤖 **AI-Powered Script Generation** - Groq (Llama 3.3)
- 🎙️ **Natural Text-to-Speech** - Edge TTS with 12+ languages, female voices
- 🎨 **AI Image Generation** - Multiple providers (PiAPI, Pollinations, HuggingFace)
- 🎬 **Professional Video Assembly** - FFmpeg with effects and transitions
- 📱 **Telegram Interface** - Simple bot commands
- 🌍 **Multi-language Support** - Hindi, English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic
- 🎯 **Reference Images** - Upload your own style reference images
- ⚠️ **Content Safety** - Automatic detection of sensitive content with alternatives

## 💰 Cost

| Component | Provider | Cost |
|-----------|----------|------|
| Script | Groq | FREE |
| Voice | Edge TTS | FREE |
| Images | PiAPI | $0.008/video |
| Video | FFmpeg | FREE |
| **Total** | | **$0.008/video** |

*100 videos = $0.80 | 1000 videos = $8.00*

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- FFmpeg 6.0+
- Telegram Bot Token
- Groq API Key (free)
- PiAPI Key (paid, $0.008/video)

### 2. Installation

```bash
# Clone repository
git clone https://github.com/pratswinz/youtube-shorts-automation.git
cd youtube-shorts-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download FFmpeg (if not installed)
# macOS: brew install ffmpeg
# Linux: apt-get install ffmpeg
# Or use: python download_ffmpeg.py
```

### 3. Configuration

Create a `.env` file:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# AI Script Generation (FREE)
GROQ_API_KEY=your_groq_api_key

# Image Generation (Choose one)
IMAGE_PROVIDER=piapi
PIAPI_API_KEY=your_piapi_key

# Optional: Other providers
# IMAGE_PROVIDER=pollinations  # Free but unreliable
# IMAGE_PROVIDER=huggingface
# HUGGINGFACE_API_KEY=your_hf_key

# Video Settings
VIDEO_FORMAT=shorts
VIDEO_DURATION=60
ENABLE_SUBTITLES=false
```

### 4. Get API Keys

**Telegram Bot Token** (Required, FREE):
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy the token

**Groq API Key** (Required, FREE):
1. Visit https://console.groq.com
2. Sign up (free)
3. Go to API Keys
4. Create new key

**PiAPI Key** (Recommended, $0.008/video):
1. Visit https://piapi.ai
2. Sign up
3. Add $5-10 credit
4. Copy API key

### 5. Start the Bot

```bash
# Clear any existing Telegram sessions
python clear_telegram.py

# Wait 2 minutes for Telegram to release
sleep 120

# Start the bot
./start.sh

# Or manually:
source venv/bin/activate
python main.py
```

### 6. Create Your First Video

Open Telegram and search for your bot (`@YourBotName`):

```
/start
create video about yoga benefits
```

Or in Hindi:
```
create hindi video about meditation
```

## 📖 Usage

### Basic Commands

- `/start` - Welcome message and instructions
- `/help` - Show all commands
- `/status` - Check bot status
- `/cancel` - Cancel current job

### Creating Videos

**Simple prompt:**
```
create video about healthy eating
```

**With language:**
```
create hindi video about yoga
create spanish video about travel tips
```

**With style:**
```
create cinematic video about nature
create educational video about science
```

### Reference Images

Upload an image to set a style reference:
```
1. Upload image to bot
2. Bot confirms: "Style reference saved"
3. Create video: "create video about sunset"
4. Clear style: /clearstyle
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Telegram Bot                         │
│                  (User Interface)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Video Generator                         │
│                  (Orchestrator)                         │
├─────────────────────────────────────────────────────────┤
│  • Content Analyzer  (Language, Subject, Style)        │
│  • Prompt Generator  (Image prompts + Inspector)       │
│  • Content Safety    (Sensitive content detection)     │
└────────┬────────────┬────────────┬─────────────────────┘
         │            │            │
         ▼            ▼            ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │ Script │  │   TTS   │  │  Image   │
    │Provider│  │Provider │  │ Provider │
    └────────┘  └─────────┘  └──────────┘
         │            │            │
         └────────────┴────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Video Assembler     │
         │      (FFmpeg)         │
         └───────────────────────┘
```

### Key Components

- **VideoGenerator** - Main orchestrator coordinating all components
- **ContentAnalyzer** - Analyzes prompts, detects language, extracts metadata
- **PromptGenerator** - Generates and inspects AI image prompts
- **ContentSafety** - Detects sensitive content and suggests alternatives
- **VideoAssembler** - FFmpeg-based video assembly with effects
- **JobQueue** - Manages video generation tasks

## 🔧 Providers

### Script Generation
- **Groq** (Default, FREE) - Llama 3.3
- OpenAI - GPT-4
- Anthropic - Claude

### Text-to-Speech
- **Edge TTS** (Default, FREE) - Microsoft voices, 12+ languages, all female
- Google Cloud TTS - Premium quality
- ElevenLabs - Ultra-realistic voices

### Image Generation
- **PiAPI** (Recommended, $0.008/video) - FLUX.1.1-pro, reliable
- Pollinations (FREE, unreliable) - Free but rate-limited
- HuggingFace (FREE with key) - Various models

## 🧪 Testing

```bash
# Test individual components
python test_refactored_system.py

# Test full pipeline
python test_full_refactored.py

# Test bot integration
python test_bot_integration.py

# Test subtitle removal
python test_no_subtitles.py

# Test female voices
python test_female_voice.py

# Run all tests
./run_all_tests.sh
```

## 📁 Project Structure

```
automation/
├── main.py                 # Entry point
├── clear_telegram.py       # Telegram state cleaner
├── bot/
│   ├── __init__.py
│   └── telegram_bot.py     # Telegram bot handlers
├── core/
│   ├── __init__.py
│   ├── job_queue.py        # Job queue management
│   ├── video_generator.py  # Main orchestrator
│   ├── content_analyzer.py # Content analysis
│   ├── prompt_generator.py # Image prompt generation
│   ├── content_safety.py   # Safety checks
│   └── video_assembler.py  # FFmpeg video assembly
├── providers/
│   ├── __init__.py
│   ├── script_provider.py  # AI script generation
│   ├── tts_provider.py     # Text-to-speech
│   └── image_provider.py   # Image generation
├── config/
│   ├── __init__.py
│   ├── settings.py         # Configuration
│   └── constants.py        # Constants
├── start.sh                # Start script
├── stop.sh                 # Stop script
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (create this)
```

## 🛠️ Configuration

### Environment Variables

See `.env.example` for all available options.

Key settings:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `GROQ_API_KEY` - Groq API key for script generation
- `IMAGE_PROVIDER` - piapi/pollinations/huggingface
- `PIAPI_API_KEY` - PiAPI key (if using PiAPI)
- `VIDEO_DURATION` - Target video duration (default: 60s)
- `ENABLE_SUBTITLES` - Enable/disable subtitles (default: false)

## 🐛 Troubleshooting

### Telegram Conflicts

If you see "Conflict: terminated by other getUpdates request":

```bash
# Kill all bot processes
pkill -9 -f "Python main.py"

# Clear Telegram state
python clear_telegram.py

# Wait 2 minutes
sleep 120

# Start bot
./start.sh
```

### Image Generation Issues

If images fail with "inappropriate content":
- The image provider may be filtering certain keywords
- Check the content warning message from the bot
- Try the suggested alternative prompt
- Or use a different image provider

### FFmpeg Not Found

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Or download locally
python download_ffmpeg.py
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

- GitHub Issues: Report bugs and request features
- Documentation: See `/docs` folder for detailed guides

## 🎯 Roadmap

- [ ] WhatsApp bot integration
- [ ] YouTube auto-upload
- [ ] Instagram auto-post
- [ ] Video editing features
- [ ] Custom templates
- [ ] Analytics dashboard

---

**Made with ❤️ for content creators**

*Create unlimited videos for less than 1 cent each!*
