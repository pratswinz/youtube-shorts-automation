# 🎨 Reference Image Feature

## What It Does

Upload your own image and ALL generated images will match its style!

**Perfect for:**
- Brand consistency (use your logo/brand colors)
- Character consistency (same person in all scenes)
- Art style matching (cartoon, realistic, anime, etc.)
- Color palette matching

---

## How It Works

1. **Upload Reference Image**
   - Send any image to the bot
   - Bot saves it as your style reference

2. **Create Videos**
   - All images will match your reference style
   - Same colors, same art style, same mood

3. **Manage Reference**
   - `/style` - View current reference
   - `/clearstyle` - Remove reference
   - Send new image - Replace reference

---

## Quick Start

### Step 1: Upload Reference Image

In Telegram:
1. Send an image to the bot
2. Bot confirms: "Style Reference Saved!"

### Step 2: Create Video

```
Create a video about meditation
```

All 5 images will match your reference style!

### Step 3: Manage

```
/style         - Check current reference
/clearstyle    - Remove reference
```

---

## Examples

### Example 1: Brand Colors

**Reference:** Your brand logo (blue/orange)
**Result:** All video images use blue/orange palette

### Example 2: Character Consistency

**Reference:** Photo of a person
**Result:** Same person appears in all scenes

### Example 3: Art Style

**Reference:** Cartoon image
**Result:** All images in cartoon style

### Example 4: Product Videos

**Reference:** Your product photo
**Result:** Product featured in all scenes

---

## How Strong is the Match?

**Strength:** 70% (default)
- 0% = Completely different
- 50% = Moderate influence
- 70% = Strong influence (default)
- 100% = Almost identical

The system uses 70% to balance:
- ✅ Matching your style
- ✅ Following the scene prompts

---

## Technical Details

### Supported Formats:
- JPG, PNG, WebP
- Any resolution (auto-resized)
- Max file size: 20MB

### How It Works:
1. You upload image → Saved as reference
2. Bot generates video → Uses image-to-image AI
3. Each scene → Starts from your reference + applies prompt
4. Result → Consistent style across all scenes

### Provider Support:
- ✅ **PiAPI** - Full support (image-to-image)
- ⚠️ **HuggingFace** - Limited support
- ❌ **Pollinations** - Not supported

**Recommendation:** Use PiAPI for best results ($0.008/video)

---

## Use Cases

### 1. Personal Branding
```
Reference: Your headshot
Videos: All feature you in different scenarios
```

### 2. Product Marketing
```
Reference: Product photo
Videos: Product in different use cases
```

### 3. Educational Content
```
Reference: Textbook illustration style
Videos: Consistent educational visuals
```

### 4. Entertainment
```
Reference: Anime character
Videos: Character in different situations
```

### 5. Real Estate
```
Reference: Property photo
Videos: Property in different lighting/angles
```

---

## Tips for Best Results

### ✅ DO:
- Use high-quality images
- Use clear, well-lit photos
- Use images with your desired style
- Test different references

### ❌ DON'T:
- Use blurry images
- Use images with text overlays
- Use copyrighted characters (unless you own rights)
- Expect 100% identical copies

---

## Commands

```bash
# Upload reference
[Send image to bot]

# Check status
/style

# Clear reference
/clearstyle

# Create video with reference
Create a video about [topic]
```

---

## Pricing

**With Reference Image:**
- Same cost as without: $0.008/video (PiAPI)
- No extra charge for image-to-image

**Free Providers:**
- Reference images not supported
- Use PiAPI for this feature

---

## Example Workflow

```
1. Send image to bot
   → "✅ Style Reference Saved!"

2. /style
   → "🎨 Style Reference Active"

3. Create a video about morning routine
   → Bot generates 5 images matching your style

4. /clearstyle
   → "✅ Style reference cleared!"

5. Create another video
   → Bot uses default AI generation
```

---

## FAQ

**Q: Can I use celebrity photos?**
A: Only if you own the rights. Don't use copyrighted images.

**Q: Will it look exactly like my reference?**
A: 70% similar. It balances your style with scene requirements.

**Q: Can I change the strength?**
A: Not via bot commands yet. Default is 70%.

**Q: Does it work with free providers?**
A: No. Use PiAPI ($0.008/video) for this feature.

**Q: Can I use multiple references?**
A: One at a time. Upload new image to replace.

**Q: Does it slow down generation?**
A: No. Same speed as regular generation.

---

## Troubleshooting

### "Reference image not found"
- Upload image again
- Check `/style` to confirm

### "Images don't match my reference"
- Make sure you're using PiAPI
- Check image quality
- Try different reference

### "Feature not working"
- Requires PiAPI provider
- Check: `IMAGE_PROVIDER=piapi` in .env

---

## Advanced: API Usage

If using the API directly:

```python
from pathlib import Path

reference_image = Path("my_brand_image.jpg")

image_results = await image_provider.generate_batch(
    prompts=["Scene 1", "Scene 2"],
    output_dir=Path("output"),
    reference_image=reference_image,
    strength=0.7  # 0.0 to 1.0
)
```

---

**Create videos that match YOUR style! 🎨**

