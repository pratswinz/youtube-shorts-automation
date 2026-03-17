# 🔑 How to Get PiAPI Key (5 Minutes)

## Step-by-Step Guide

### Step 1: Visit PiAPI Website
```
https://piapi.ai
```

Click "Sign Up" or "Get Started"

---

### Step 2: Create Account

**Option A: Email Signup**
1. Enter your email
2. Create password
3. Verify email

**Option B: Google Signup**
1. Click "Sign up with Google"
2. Choose your Google account
3. Done!

---

### Step 3: Add Credits

**Pricing:**
- $5 = 2,500 images = 500 videos
- $10 = 5,000 images = 1,000 videos
- $20 = 10,000 images = 2,000 videos

**Recommendation:** Start with $5-10

**Payment Methods:**
- Credit Card
- PayPal
- Crypto (some providers)

**Steps:**
1. Go to "Billing" or "Credits"
2. Click "Add Credits"
3. Choose amount ($5, $10, $20)
4. Enter payment info
5. Confirm purchase

---

### Step 4: Get API Key

1. Go to "API Keys" or "Settings"
2. Click "Create New API Key"
3. Give it a name: "YouTube Automation"
4. Click "Create"
5. **Copy the key** (looks like: `piapi_xxxxxxxxxxxxxxxx`)

⚠️ **IMPORTANT:** Copy and save it now! You won't see it again.

---

### Step 5: Add to Your System

**Method 1: Edit .env file**
```bash
# Open .env
nano .env

# Add these lines:
IMAGE_PROVIDER=piapi
PIAPI_API_KEY=piapi_xxxxxxxxxxxxxxxx

# Save: Ctrl+X, Y, Enter
```

**Method 2: Direct edit**
1. Open `.env` file in text editor
2. Find `IMAGE_PROVIDER=huggingface`
3. Change to `IMAGE_PROVIDER=piapi`
4. Add line: `PIAPI_API_KEY=your_key_here`
5. Save file

---

### Step 6: Test It

```bash
# Activate environment
source venv/bin/activate

# Run test
python test_full_flow.py
```

Should see:
```
✅ Image generated!
Cost: $0.002
```

---

### Step 7: Start Bot

```bash
./start.sh
```

In Telegram:
```
Create a video about meditation
```

Wait 60-90 seconds → Get video!

---

## Visual Guide

### 1. Homepage
```
https://piapi.ai
┌─────────────────────────────┐
│  [Sign Up]  [Login]         │
│                             │
│  AI Image Generation API    │
│  Fast, Reliable, Affordable │
│                             │
│  [Get Started] →            │
└─────────────────────────────┘
```

### 2. Dashboard
```
┌─────────────────────────────┐
│  Dashboard                  │
│  ├─ API Keys                │
│  ├─ Billing                 │
│  ├─ Usage                   │
│  └─ Documentation           │
└─────────────────────────────┘
```

### 3. API Keys Page
```
┌─────────────────────────────┐
│  API Keys                   │
│                             │
│  [+ Create New Key]         │
│                             │
│  Name: YouTube Automation   │
│  Key: piapi_xxxxx...        │
│  Created: Today             │
│  [Copy] [Delete]            │
└─────────────────────────────┘
```

---

## Pricing Breakdown

### Per Image:
- 1 image = $0.002
- 5 images (1 video) = $0.010
- 100 videos = $1.00
- 1000 videos = $10.00

### Credit Packages:
```
$5   →   500 videos
$10  → 1,000 videos
$20  → 2,000 videos
$50  → 5,000 videos
```

### No Monthly Fee!
- Pay as you go
- No subscription
- Credits never expire

---

## Troubleshooting

### "Can't find API Keys section"
- Look for "Settings" → "API"
- Or "Developer" → "API Keys"
- Or "Account" → "API Keys"

### "Payment failed"
- Try different card
- Use PayPal
- Contact support: support@piapi.ai

### "Key not working"
- Make sure you copied full key
- Check for extra spaces
- Regenerate key if needed

### "Test still failing"
- Restart terminal
- Check .env file saved
- Run: `cat .env | grep PIAPI`

---

## Alternative: Free Trial

Some providers offer free trial credits:

1. Sign up
2. Get 10-50 free credits
3. Test the system
4. Add more credits later

**Check their website for current promotions!**

---

## Security Tips

### ✅ DO:
- Keep your API key secret
- Don't share in public
- Don't commit to git
- Regenerate if exposed

### ❌ DON'T:
- Share key publicly
- Post on forums
- Include in screenshots
- Commit to GitHub

---

## Quick Reference

```bash
# Website
https://piapi.ai

# Support
support@piapi.ai

# Documentation
https://docs.piapi.ai

# Pricing
https://piapi.ai/pricing
```

---

## After Getting Key

### 1. Update .env
```bash
IMAGE_PROVIDER=piapi
PIAPI_API_KEY=your_key_here
```

### 2. Test
```bash
python test_full_flow.py
```

### 3. Start
```bash
./start.sh
```

### 4. Create!
```
In Telegram: "Create a video about yoga"
```

---

## Cost Calculator

**How many videos can you make?**

```
$5   = 500 videos
$10  = 1,000 videos
$20  = 2,000 videos
$50  = 5,000 videos
$100 = 10,000 videos
```

**Per video:** $0.008 (less than 1 cent!)

---

## FAQ

**Q: Do I need a credit card?**
A: Yes, or PayPal. No free tier for production use.

**Q: Is there a free trial?**
A: Sometimes. Check their website for promotions.

**Q: Can I use prepaid cards?**
A: Usually yes, if they support online payments.

**Q: How long do credits last?**
A: Forever! No expiration.

**Q: Can I get a refund?**
A: Check their refund policy. Usually yes if unused.

**Q: Is it safe?**
A: Yes. Industry-standard payment processing.

---

## Summary

1. **Visit:** https://piapi.ai
2. **Sign up** (2 minutes)
3. **Add credits** ($5-10 recommended)
4. **Get API key** (copy it!)
5. **Add to .env** file
6. **Test:** `python test_full_flow.py`
7. **Start:** `./start.sh`
8. **Create videos!**

**Total time: 5 minutes**
**Cost: $5-10 (makes 500-1000 videos)**

---

🎬 **You're 5 minutes away from creating unlimited videos!**

