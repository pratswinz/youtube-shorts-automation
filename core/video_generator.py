"""
Main video generation orchestrator
Coordinates all providers to create the final video

Architecture: Orchestrator Pattern
- VideoGenerator: Main orchestrator coordinating all components
- ContentAnalyzer: Analyzes prompts and extracts metadata
- PromptGenerator: Generates and inspects image prompts
- Providers: Script, TTS, Image generation
- VideoAssembler: Final video assembly
"""
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger

from providers import get_script_provider, get_tts_provider, get_image_provider
from config.settings import settings
from config.constants import JobStatus
from core.content_analyzer import ContentAnalyzer
from core.prompt_generator import PromptGenerator
from core.job_queue import VideoJob


class VideoGenerator:
    """
    Main video generation orchestrator
    
    Orchestrates the complete video generation pipeline:
    1. Content analysis (language, subject, style)
    2. Script generation (narration)
    3. Audio generation (TTS)
    4. Image prompt generation and inspection
    5. Image generation
    6. Video assembly
    """
    
    def __init__(self):
        # Core providers
        self.script_provider = get_script_provider()
        self.tts_provider = get_tts_provider()
        self.image_provider = get_image_provider()
        
        # AI analysis components
        self.content_analyzer = ContentAnalyzer()
        self.prompt_generator = PromptGenerator()
    
    async def generate_video(self, job: VideoJob) -> Path:
        """
        Generate complete video from prompt
        
        Steps:
        1. Generate script with AI
        2. Generate voiceover with TTS
        3. Generate images for each scene
        4. Assemble video with FFmpeg
        5. Add subtitles
        6. Return final video path
        """
        try:
            logger.info(f"Starting video generation for job {job.job_id}")
            
            # Create temp directory for this job
            job_dir = Path(settings.temp_dir) / job.job_id
            job_dir.mkdir(parents=True, exist_ok=True)
            
            # Step 1: Analyze content and detect language
            job.status = JobStatus.GENERATING_SCRIPT
            job.progress = 10
            
            language = self.content_analyzer.detect_language(
                job.prompt, 
                job.metadata.get('language', settings.default_language)
            )
            logger.info(f"Detected language: {language}")
            
            # Analyze prompt for visual strategy
            prompt_analysis = await self.content_analyzer.analyze_prompt(job.prompt, job.style)
            logger.info(f"Visual strategy: {prompt_analysis['main_subject']} ({prompt_analysis['visual_category']})")
            
            # Step 2: Generate script
            logger.info(f"Generating script for: {job.prompt}")
            if job.notification_callback:
                await job.notification_callback("📝 Step 1/5: Generating script...")
            
            script_result = await self.script_provider.generate_script(
                prompt=job.prompt,
                duration=job.duration,
                style=job.style,
                language=language
            )
            
            logger.info(f"Script generated: {len(script_result.script)} chars, {len(script_result.metadata.get('scenes', []))} scenes")
            
            job.metadata["script"] = script_result.script
            job.metadata["title"] = script_result.title
            job.metadata["description"] = script_result.description
            job.metadata["tags"] = script_result.tags
            job.metadata["scenes"] = script_result.metadata.get("scenes", [])
            job.metadata["language"] = language
            job.progress = 30
            
            # Step 3: Generate voiceover
            job.status = JobStatus.GENERATING_VOICE
            logger.info(f"Generating voiceover in {language}")
            if job.notification_callback:
                await job.notification_callback("🎙️ Step 2/5: Generating voiceover...")
            
            audio_path = job_dir / "voiceover.mp3"
            tts_result = await self.tts_provider.generate_speech(
                text=script_result.script,
                output_path=audio_path,
                language=language
            )
            
            job.metadata["audio_path"] = str(audio_path)
            job.metadata["audio_duration"] = tts_result.duration_seconds
            job.progress = 40
            
            # Step 4: Generate and refine image prompts
            job.status = JobStatus.GENERATING_IMAGES
            logger.info(f"Generating image prompts for {len(job.metadata['scenes'])} scenes")
            if job.notification_callback:
                await job.notification_callback(f"🎨 Step 3/5: Generating {len(job.metadata['scenes'])} images...")
            
            images_dir = job_dir / "images"
            images_dir.mkdir(exist_ok=True)
            
            # Generate AI-powered image prompts
            image_prompts = await self.prompt_generator.generate_prompts(
                user_prompt=job.prompt,
                scenes=job.metadata["scenes"],
                language=language,
                visual_strategy=prompt_analysis
            )
            
            # Inspect and refine prompts
            refined_result = await self.prompt_generator.inspect_and_refine(
                prompts=image_prompts,
                user_prompt=job.prompt,
                scenes=job.metadata["scenes"]
            )
            
            final_prompts = refined_result['prompts']
            quality = refined_result['quality']
            logger.info(f"Prompt inspection complete: Quality={quality}")
            
            job.metadata['prompt_quality'] = quality
            job.metadata['inspection'] = refined_result.get('inspection')
            job.progress = 50
            
            # Save prompts for review
            prompts_file = job_dir / "image_prompts.txt"
            self._save_prompts_log(prompts_file, job, prompt_analysis, refined_result, final_prompts)
            
            # Step 5: Generate images
            try:
                reference_image = self._get_reference_image(job.metadata)
                
                image_results = await self.image_provider.generate_batch(
                    prompts=final_prompts,
                    output_dir=images_dir,
                    width=settings.video_width,
                    height=settings.video_height,
                    reference_image=reference_image
                )
                
                if not all(hasattr(img, 'image_path') for img in image_results):
                    raise Exception("Image generation failed - some images could not be created")
                
                job.metadata["images"] = [str(img.image_path) for img in image_results]
            except Exception as e:
                logger.error(f"Image generation failed: {e}")
                raise Exception(f"Image generation failed. Try switching provider: /switch image piapi")
            
            job.progress = 70
            
            # Step 6: Assemble video
            job.status = JobStatus.ASSEMBLING_VIDEO
            logger.info("Assembling final video")
            if job.notification_callback:
                await job.notification_callback("🎬 Step 4/5: Assembling video with FFmpeg...")
            
            from core.video_assembler import VideoAssembler
            assembler = VideoAssembler()
            
            final_video_path = job_dir / f"{job.job_id}_final.mp4"
            await assembler.assemble_video(
                audio_path=audio_path,
                images=[img.image_path for img in image_results],
                scenes=job.metadata["scenes"],
                output_path=final_video_path,
                duration=tts_result.duration_seconds
            )
            
            job.output_path = final_video_path
            job.progress = 90
            
            # Step 7: Generate thumbnail
            logger.info("Generating thumbnail")
            if job.notification_callback:
                await job.notification_callback("🖼️ Step 5/5: Generating thumbnail...")
            thumbnail_path = job_dir / f"{job.job_id}_thumbnail.jpg"
            await assembler.generate_thumbnail(
                title=script_result.title,
                background_image=image_results[0].image_path,
                output_path=thumbnail_path
            )
            
            job.metadata["thumbnail_path"] = str(thumbnail_path)
            job.progress = 100
            job.status = JobStatus.COMPLETED
            
            logger.success(f"Video generation completed: {final_video_path}")
            return final_video_path
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            job.status = JobStatus.FAILED
            job.error = str(e)
            raise
    
    def _get_reference_image(self, metadata: dict) -> Optional[Path]:
        """Get reference image if available"""
        if 'reference_image' in metadata:
            reference_image = Path(metadata['reference_image'])
            if reference_image.exists():
                logger.info(f"Using reference image: {reference_image}")
                return reference_image
            else:
                logger.warning(f"Reference image not found: {reference_image}")
        return None
    
    def _save_prompts_log(self, prompts_file: Path, job: VideoJob, prompt_analysis: dict, 
                          refined_result: dict, final_prompts: list):
        """Save detailed prompts log for review"""
        with open(prompts_file, 'w', encoding='utf-8') as f:
            f.write(f"USER PROMPT: {job.prompt}\n")
            f.write(f"LANGUAGE: {job.metadata.get('language', 'unknown')}\n\n")
            f.write("="*80 + "\n")
            f.write("AI PROMPT ANALYSIS\n")
            f.write("="*80 + "\n")
            f.write(f"Main Subject: {prompt_analysis.get('main_subject', 'N/A')}\n")
            f.write(f"Visual Category: {prompt_analysis.get('visual_category', 'N/A')}\n")
            f.write(f"Photography Style: {prompt_analysis.get('photography_style', 'N/A')}\n")
            f.write(f"Mood: {prompt_analysis.get('mood', 'N/A')}\n")
            f.write(f"Style Prefix: {prompt_analysis.get('style_prefix', 'N/A')}\n\n")
            f.write("="*80 + "\n")
            f.write("QUALITY INSPECTION\n")
            f.write("="*80 + "\n")
            f.write(f"Overall Quality: {refined_result.get('quality', 'unknown').upper()}\n\n")
            
            for i, prompt in enumerate(final_prompts, 1):
                f.write(f"SCENE {i}\n")
                f.write(f"{'─'*80}\n")
                if i <= len(job.metadata.get('scenes', [])):
                    f.write(f"Narration: {job.metadata['scenes'][i-1]['text']}\n\n")
                f.write(f"Final Prompt:\n{prompt}\n")
                f.write(f"{'='*80}\n\n")
        
        logger.info(f"Image prompts saved to: {prompts_file}")
    
    def switch_script_provider(self, provider_name: str):
        """Switch script generation provider at runtime"""
        self.script_provider = get_script_provider(provider_name)
        logger.info(f"Switched script provider to: {provider_name}")
    
    def switch_tts_provider(self, provider_name: str):
        """Switch TTS provider at runtime"""
        self.tts_provider = get_tts_provider(provider_name)
        logger.info(f"Switched TTS provider to: {provider_name}")
    
    def switch_image_provider(self, provider_name: str):
        """Switch image provider at runtime"""
        self.image_provider = get_image_provider(provider_name)
        logger.info(f"Switched image provider to: {provider_name}")
