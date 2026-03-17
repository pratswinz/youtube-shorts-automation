# 🧪 Test Your System

## Quick Test (Recommended)

Run this to test all components:

```bash
source venv/bin/activate
python test_full_flow.py
```

This will test:
1. ✅ Script generation (Groq)
2. ✅ Text-to-Speech (Edge TTS)
3. ✅ Image generation (Hugging Face)
4. ✅ Video assembly (FFmpeg)

**Time:** 60-90 seconds
**Cost:** $0.00

---

## What to Expect

### Test 1: Script Generation
```
✅ Script generated!
Title: [Your video title]
Scenes: 5-6
Cost: $0.00
```

### Test 2: Text-to-Speech
```
✅ Audio generated!
Duration: 5-10s
Characters: 200
Cost: $0.00
File: temp/test_audio.mp3
```

### Test 3: Image Generation
```
⏳ Generating test image (may take 30-60s on first run)...
✅ Image generated!
File: temp/test_image.png
Cost: $0.00
```

**Note:** First Hugging Face request can take 30-60 seconds while model loads. After that, it's much faster!

### Test 4: FFmpeg
```
✅ FFmpeg found: ffmpeg version 8.0.1
```

---

## If Tests Pass

You'll see:
```
🎉 ALL TESTS PASSED!

✅ Script Generation: Working
✅ Text-to-Speech: Working
✅ Image Generation: Working
✅ Video Assembly: Working

🚀 YOUR SYSTEM IS READY!

💰 Cost per video: $0.0000
🎉 100% FREE!
```

Then start the bot:
```bash
./start.sh
```

---

## If Tests Fail

### Script Generation Failed
```
❌ Check your GROQ_API_KEY in .env
```

**Fix:**
1. Verify key in .env
2. Test key: https://console.groq.com/

### TTS Failed
```
❌ Edge TTS not working
```

**Fix:**
```bash
pip install edge-tts
```

### Image Generation Failed
```
❌ Hugging Face not responding
```

**Solutions:**
1. **Wait and retry** (model might be loading)
2. **Get HF API key** (free): https://huggingface.co/settings/tokens
   ```
   HUGGINGFACE_API_KEY=hf_xxxxx
   ```
3. **Switch to paid** ($0.008/video):
   ```
   IMAGE_PROVIDER=piapi
   PIAPI_API_KEY=your_key
   ```

### FFmpeg Failed
```
❌ FFmpeg not found
```

**Fix:**
Check `bin/ffmpeg` exists or install globally

---

## Full Bot Test

After component tests pass, test the full bot:

```bash
./start.sh
```

In Telegram:
1. Send: `/start`
2. Send: `Create a 30-second video about morning meditation`
3. Wait 60-90 seconds
4. Get video!

---

## Test with Different Languages

```
/language hindi
Create a video about yoga benefits
```

Should generate:
- Script in Hindi
- Voice in Hindi
- Title/description in Hindi

---

## Performance Benchmarks

**Expected timings:**
- Script generation: 5-10 seconds
- TTS generation: 5-10 seconds
- Image generation: 30-60 seconds (first time), 10-20 seconds (after)
- Video assembly: 10-15 seconds
- **Total: 60-90 seconds per video**

---

## Troubleshooting

### Slow Image Generation?
First Hugging Face request loads the model (30-60s). Subsequent requests are faster.

### Images Still Failing?
Switch to paid provider:
```
/switch image piapi
```
Only $0.008 per video (less than 1 cent)

### Want Faster Tests?
Use paid providers for instant results:
```
IMAGE_PROVIDER=piapi
PIAPI_API_KEY=your_key
```

---

## Quick Commands

```bash
# Run full test
python test_full_flow.py

# Test individual providers
python test_providers.py

# Start bot
./start.sh

# Check logs
tail -f logs/automation.log
```

---

**Run the test now to verify everything works! 🚀**

