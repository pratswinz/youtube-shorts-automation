# 🌍 Multi-Language Video Support

## Supported Languages

Your bot now supports creating videos in **12+ languages**!

### Available Languages:
- 🇮🇳 **Hindi** (हिंदी)
- 🇺🇸 **English**
- 🇪🇸 **Spanish** (Español)
- 🇫🇷 **French** (Français)
- 🇩🇪 **German** (Deutsch)
- 🇮🇹 **Italian** (Italiano)
- 🇧🇷 **Portuguese** (Português)
- 🇷🇺 **Russian** (Русский)
- 🇯🇵 **Japanese** (日本語)
- 🇰🇷 **Korean** (한국어)
- 🇨🇳 **Chinese** (中文)
- 🇸🇦 **Arabic** (عربي)

---

## How to Use

### Method 1: Set Default Language
```
/language hindi
```

All videos will now be generated in Hindi until you change it.

### Method 2: Specify in Prompt
```
Create a Hindi video about meditation benefits
```

The bot automatically detects language keywords in your prompt!

### Method 3: Mix Languages
```
/language spanish
Create a video about yoga
```

---

## Examples

### Hindi Video:
```
/language hindi
Create a video about morning meditation
```

**Result:**
- Script in Hindi
- Voiceover in Hindi (native speaker quality)
- Title, description, tags in Hindi

### Spanish Video:
```
Create a Spanish video about healthy eating
```

**Result:**
- Automatic detection from "Spanish" keyword
- Full video in Spanish

### English (Default):
```
Create a video about quantum computing
```

---

## Language Features

✅ **Native Voice Quality** - Uses Edge TTS with native speakers
✅ **Auto-Detection** - Detects language from prompt
✅ **Full Localization** - Title, description, script, voiceover
✅ **Free Forever** - All languages included at no cost

---

## Voice Quality

Each language uses Microsoft Edge TTS neural voices:

| Language | Voice | Gender |
|----------|-------|--------|
| Hindi | Madhur | Male |
| English | Guy | Male |
| Spanish | Alvaro | Male |
| French | Henri | Male |
| German | Conrad | Male |
| Italian | Diego | Male |
| Portuguese | Antonio | Male |
| Russian | Dmitry | Male |
| Japanese | Keita | Male |
| Korean | InJoon | Male |
| Chinese | Yunxi | Male |
| Arabic | Hamed | Male |

---

## Tips for Best Results

### 1. Be Specific
```
✅ Create a Hindi video about yoga benefits for beginners
❌ yoga video
```

### 2. Use Native Keywords
```
✅ "योग के फायदे" (if you know Hindi)
✅ "yoga benefits in Hindi" (if you don't)
```

### 3. Check Language Setting
```
/language
```
Shows current language setting

---

## Troubleshooting

### Wrong Language?
```
/language english
```
Reset to English

### Mixed Language Output?
Make sure to set language BEFORE sending prompt:
```
/language hindi
Create a video about meditation
```

### Voice Not Clear?
Edge TTS provides high-quality neural voices. If you want even better quality, upgrade to Google TTS or ElevenLabs (paid).

---

## Advanced: Custom Voices

Want a different voice? You can specify custom Edge TTS voices:

```python
# In your .env file:
EDGE_TTS_VOICE=hi-IN-SwaraNeural  # Female Hindi voice
```

Find more voices: https://speech.microsoft.com/portal/voicegallery

---

## Cost

**All languages: $0.00** 🎉

Edge TTS is completely free with unlimited usage!

---

## Coming Soon

- 🎭 Multiple voice options per language
- 👥 Multi-speaker dialogues
- 🎵 Language-specific background music
- 📝 Subtitle customization per language

---

## Quick Reference

```bash
# Set language
/language hindi

# Create video
Create a video about [topic]

# Check current language
/language

# Reset to English
/language english
```

---

**Your bot is now a multilingual video creation powerhouse! 🚀**

