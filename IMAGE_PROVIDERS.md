# 🎨 Image Generation Providers

## Available Options

### 1. **Hugging Face** (FREE - Default, Most Reliable) ⭐
- **Model:** FLUX.1-schnell
- **Quality:** Excellent
- **Speed:** Fast (10-20 seconds per image)
- **Reliability:** High
- **Cost:** $0.00
- **API Key:** Optional (works without, but with rate limits)

**Best for:** Production use, reliable generation

```
IMAGE_PROVIDER=huggingface
```

---

### 2. **Pollinations.ai** (FREE - Backup)
- **Quality:** Good
- **Speed:** Very fast (5-10 seconds)
- **Reliability:** Medium (can have downtime)
- **Cost:** $0.00
- **API Key:** None needed

**Best for:** Quick tests when Hugging Face is slow

```
IMAGE_PROVIDER=pollinations
```

---

### 3. **PiAPI FLUX** (PAID - Premium) 💎
- **Model:** FLUX.1.1-pro
- **Quality:** Excellent (best quality)
- **Speed:** Medium (15-30 seconds)
- **Reliability:** Very High
- **Cost:** $0.008 per video (5 images)
- **API Key:** Required

**Best for:** Professional videos, important content

```
IMAGE_PROVIDER=piapi
PIAPI_API_KEY=your_key_here
```

---

## Comparison

| Provider | Cost | Quality | Speed | Reliability |
|----------|------|---------|-------|-------------|
| Hugging Face | FREE | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Pollinations | FREE | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| PiAPI | $0.008 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## How to Switch

### Via Telegram:
```
/switch image huggingface
/switch image pollinations
/switch image piapi
```

### Via .env file:
```bash
# Edit .env
nano .env

# Change this line:
IMAGE_PROVIDER=huggingface

# Restart bot
./start.sh
```

---

## Getting API Keys

### Hugging Face (Optional, for higher rate limits):
1. Visit: https://huggingface.co/settings/tokens
2. Create new token
3. Add to .env:
   ```
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
   ```

### PiAPI (For premium quality):
1. Visit: https://piapi.ai
2. Sign up and get API key
3. Add to .env:
   ```
   PIAPI_API_KEY=your_key_here
   ```

---

## Troubleshooting

### Images Not Generating?

**Try switching providers:**
```
/switch image huggingface
```

**Or use paid provider:**
```
/switch image piapi
```

### Hugging Face Model Loading?
First request can take 30-60 seconds while model loads. Subsequent requests are faster.

### Rate Limits?
- Hugging Face: ~100 requests/hour without API key
- With API key: Much higher limits
- PiAPI: Based on your plan

---

## Recommendations

### For Testing:
✅ **Hugging Face** (free, reliable)

### For Production:
✅ **Hugging Face** with API key (free, high limits)
✅ **PiAPI** for premium quality ($0.008/video)

### For Quick Tests:
✅ **Pollinations** (fastest, but less reliable)

---

## Current Setup

Your bot is currently using: **Hugging Face (FREE)**

This provides:
- ✅ Excellent image quality
- ✅ High reliability
- ✅ No API key needed
- ✅ $0.00 cost

---

## Upgrade Path

1. **Start:** Hugging Face (free) ← You are here
2. **More videos:** Add Hugging Face API key (still free)
3. **Premium:** Switch to PiAPI ($0.008/video)

---

**Your system is optimized for the best free option! 🚀**

