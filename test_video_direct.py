#!/usr/bin/env python3
"""Direct video generation test (bypasses Telegram)"""
import asyncio
from pathlib import Path
from core.video_generator import VideoGenerator
from core.job_queue import JobQueue, VideoJob
from config.settings import settings

async def test_video():
    print("🎬 Testing video generation directly...")
    print(f"Image Provider: {settings.image_provider}")
    print(f"TTS Provider: {settings.tts_provider}")
    print()
    
    # Create job queue and video generator
    job_queue = JobQueue()
    video_gen = VideoGenerator()
    
    # Create a test job
    prompt = "Benefits of egg in English"
    user_id = 123456
    job_id = job_queue.generate_job_id()
    
    print(f"Creating video for: {prompt}")
    print(f"Job ID: {job_id}")
    print()
    
    try:
        # Create VideoJob object
        job = VideoJob(
            job_id=job_id,
            prompt=prompt,
            user_id=user_id
        )
        
        # Generate video
        result = await video_gen.generate_video(job)
        
        if result:
            print(f"\n✅ SUCCESS! Video generated:")
            print(f"   Path: {result}")
            if result.exists():
                size_mb = result.stat().st_size / (1024 * 1024)
                print(f"   Size: {size_mb:.2f} MB")
        else:
            print("\n❌ FAILED: No video generated")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_video())
