#!/usr/bin/env python3
"""Test PiAPI image generation"""
import asyncio
from pathlib import Path
from providers import get_image_provider
from config.settings import settings

async def test_piapi():
    print("🎨 Testing PiAPI image generation...")
    print(f"API Key: {settings.piapi_api_key[:20]}...")
    print()
    
    provider = get_image_provider()
    print(f"Provider: {provider.__class__.__name__}")
    print()
    
    # Test prompt
    prompt = "A fresh egg on a white plate, professional food photography, clean composition, soft natural lighting"
    output_path = Path("temp/test_piapi_image.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating image with prompt:")
    print(f"  {prompt}")
    print()
    
    try:
        result = await provider.generate_image(
            prompt=prompt,
            output_path=output_path,
            width=720,
            height=1280
        )
        
        if result and result.image_path.exists():
            size_kb = result.image_path.stat().st_size / 1024
            print(f"\n✅ SUCCESS!")
            print(f"   Image: {result.image_path}")
            print(f"   Size: {size_kb:.1f} KB")
            print(f"   Provider: {result.provider}")
        else:
            print("\n❌ FAILED: No image generated")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_piapi())
