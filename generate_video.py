#!/usr/bin/env python3
"""
Standalone video generator (no Telegram required)
Use this to generate videos directly while troubleshooting Telegram
"""
import asyncio
import sys
from pathlib import Path
from core.video_generator import VideoGenerator
from core.job_queue import VideoJob, JobQueue

async def generate_video(prompt: str, language: str = "auto"):
    """Generate a video from a prompt"""
    print(f"\n🎬 YouTube Shorts Generator")
    print("=" * 60)
    print(f"Prompt: {prompt}")
    print(f"Language: {language}")
    print("=" * 60)
    print()
    
    # Create job
    job_queue = JobQueue()
    job_id = job_queue.generate_job_id()
    
    # Progress callback
    async def notify(message: str):
        print(f"  {message}")
    
    job = VideoJob(
        job_id=job_id,
        user_id=0,
        prompt=prompt,
        duration=60,
        style="engaging",
        notification_callback=notify
    )
    
    if language != "auto":
        job.metadata["language"] = language
    
    print(f"Job ID: {job_id}\n")
    
    # Generate video
    video_gen = VideoGenerator()
    
    try:
        print("Starting video generation...\n")
        result = await video_gen.generate_video(job)
        
        if result and result.exists():
            size_mb = result.stat().st_size / (1024 * 1024)
            print(f"\n{'=' * 60}")
            print(f"✅ SUCCESS! Video generated!")
            print(f"{'=' * 60}")
            print(f"Path: {result}")
            print(f"Size: {size_mb:.2f} MB")
            print(f"Job ID: {job_id}")
            
            # Show thumbnail if exists
            if job.thumbnail_path and Path(job.thumbnail_path).exists():
                print(f"Thumbnail: {job.thumbnail_path}")
            
            print(f"\n🎉 Video ready to upload to YouTube!")
            return result
        else:
            print(f"\n❌ FAILED: No video generated")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python generate_video.py '<prompt>' [language]")
        print("\nExamples:")
        print("  python generate_video.py 'benefits of eggs in hindi'")
        print("  python generate_video.py 'funny cat moments' english")
        print("  python generate_video.py 'healthy breakfast ideas'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    asyncio.run(generate_video(prompt, language))

if __name__ == "__main__":
    main()
