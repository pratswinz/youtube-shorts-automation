"""
Video Assembler
Assembles final video from audio, images, and subtitles using FFmpeg
"""
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
from config.settings import settings


class VideoAssembler:
    """Assembles video from components using FFmpeg"""
    
    def __init__(self):
        self.ffmpeg_path = settings.ffmpeg_path
    
    async def assemble_video(self, audio_path: Path, images: List[Path], scenes: List[Dict],
                            output_path: Path, duration: float) -> Path:
        """
        Assemble final video from components
        
        Args:
            audio_path: Path to audio file
            images: List of image paths (one per scene)
            scenes: List of scene dicts with text, timestamp, duration
            output_path: Output video path
            duration: Total video duration in seconds
        
        Returns:
            Path to assembled video
        """
        try:
            logger.info(f"Assembling video with {len(images)} images")
            
            # Calculate duration per image
            if len(scenes) > 0:
                scene_durations = [scene.get('duration', 5) for scene in scenes]
            else:
                scene_durations = [duration / len(images)] * len(images)
            
            # Create video from images with transitions
            temp_video = output_path.parent / f"{output_path.stem}_temp.mp4"
            
            # Build FFmpeg filter complex for smooth transitions
            filter_parts = []
            inputs = []
            
            for i, (img, dur) in enumerate(zip(images, scene_durations)):
                inputs.extend(['-loop', '1', '-t', str(dur), '-i', str(img)])
                # Simple scale without zoompan (much faster)
                filter_parts.append(
                    f"[{i}:v]scale={settings.video_width}:{settings.video_height}:force_original_aspect_ratio=increase,"
                    f"crop={settings.video_width}:{settings.video_height}[v{i}]"
                )
            
            # Concatenate all videos
            concat_input = ''.join([f"[v{i}]" for i in range(len(images))])
            filter_complex = ';'.join(filter_parts) + f";{concat_input}concat=n={len(images)}:v=1:a=0[outv]"
            
            cmd = [
                self.ffmpeg_path,
                *inputs,
                '-filter_complex', filter_complex,
                '-map', '[outv]',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-r', '30',
                '-y',
                str(temp_video)
            ]
            
            logger.info("Running FFmpeg to create video from images...")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                raise Exception(f"FFmpeg failed with code {process.returncode}")
            
            logger.info("Video created from images")
            
            # Add audio to video
            cmd = [
                self.ffmpeg_path,
                '-i', str(temp_video),
                '-i', str(audio_path),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                str(output_path)
            ]
            
            logger.info("Adding audio to video...")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                raise Exception(f"FFmpeg failed with code {process.returncode}")
            
            # Clean up temp file
            if temp_video.exists():
                temp_video.unlink()
            
            logger.success(f"Video assembled: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video assembly failed: {e}")
            raise
    
    async def generate_thumbnail(self, title: str, background_image: Path, 
                                output_path: Path) -> Path:
        """
        Generate thumbnail for video
        
        Args:
            title: Video title
            background_image: Background image path
            output_path: Output thumbnail path
        
        Returns:
            Path to generated thumbnail
        """
        try:
            logger.info("Generating thumbnail")
            
            # Open background image
            img = Image.open(background_image)
            img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
            
            # Add semi-transparent overlay
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 128))
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            
            # Add title text
            draw = ImageDraw.Draw(img)
            
            # Try to load a nice font
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            words = title.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] > 900:  # Max width
                    current_line.pop()
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text centered
            y = 800
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (1080 - text_width) / 2
                
                # Draw text with outline
                for offset_x in [-2, 0, 2]:
                    for offset_y in [-2, 0, 2]:
                        draw.text((x + offset_x, y + offset_y), line, 
                                fill=(0, 0, 0), font=font)
                
                draw.text((x, y), line, fill=(255, 255, 255), font=font)
                y += 100
            
            # Convert back to RGB and save
            img = img.convert('RGB')
            img.save(output_path, quality=95)
            
            logger.info(f"Thumbnail generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
            # Create simple fallback thumbnail
            img = Image.new('RGB', (1080, 1920), color=(50, 50, 100))
            img.save(output_path)
            return output_path
