"""
Image generation providers
Supports: PiAPI (FLUX), Pollinations (free), Hugging Face
"""
import asyncio
import time
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from loguru import logger
import httpx
from PIL import Image, ImageDraw, ImageFont
import io


@dataclass
class ImageResult:
    """Result from image generation"""
    image_path: Path
    prompt: str
    provider: str


class PiAPIProvider:
    """PiAPI - FLUX model (best quality/price ratio)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.piapi.ai/api/v1/task"
    
    async def generate_image(self, prompt: str, output_path: Path, width: int = 1080, 
                            height: int = 1920, reference_image: Optional[Path] = None) -> ImageResult:
        """Generate single image"""
        try:
            # Validate prompt
            if not prompt or not prompt.strip():
                raise ValueError("Prompt cannot be empty or None")
            
            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            # PiAPI expects specific format based on their API docs
            # Use flux1-schnell for cost efficiency ($0.002/image vs $0.015 for dev)
            # Max resolution: 1024x1024 pixels (width*height <= 1048576)
            data = {
                "model": "Qubico/flux1-schnell",
                "task_type": "txt2img",
                "input": {
                    "prompt": prompt.strip(),
                    "width": width,
                    "height": height
                }
            }
            
            if reference_image and reference_image.exists():
                import base64
                with open(reference_image, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode()
                data["task_type"] = "img2img"
                data["input"]["image"] = f"data:image/jpeg;base64,{image_data}"
                data["input"]["strength"] = 0.7
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Submit task
                response = await client.post(self.base_url, json=data, headers=headers)
                if response.status_code != 200:
                    error_detail = response.text
                    logger.error(f"PiAPI request failed. Status: {response.status_code}, Response: {error_detail}")
                    logger.error(f"Request data: {data}")
                response.raise_for_status()
                task_id = response.json()["data"]["task_id"]
                
                # Poll for result
                for _ in range(60):
                    await asyncio.sleep(2)
                    status_response = await client.get(
                        f"{self.base_url}/{task_id}",
                        headers=headers
                    )
                    status_response.raise_for_status()
                    result = status_response.json()
                    
                    status = result["data"]["status"].lower()
                    if status == "completed":
                        image_url = result["data"]["output"]["image_url"]
                        
                        # Download image
                        img_response = await client.get(image_url)
                        img_response.raise_for_status()
                        
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                        
                        logger.info(f"Image generated: {output_path.name}")
                        return ImageResult(
                            image_path=output_path,
                            prompt=prompt,
                            provider="piapi"
                        )
                    elif status == "failed":
                        raise Exception(f"Image generation failed: {result['data'].get('error', 'Unknown error')}")
                
                raise Exception("Image generation timeout")
        except Exception as e:
            logger.error(f"PiAPI image generation failed: {e}")
            raise
    
    async def generate_batch(self, prompts: List[str], output_dir: Path, width: int = 1080,
                            height: int = 1920, reference_image: Optional[Path] = None) -> List[ImageResult]:
        """Generate multiple images"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        tasks = []
        for i, prompt in enumerate(prompts):
            output_path = output_dir / f"scene_{i+1}.png"
            tasks.append(self.generate_image(prompt, output_path, width, height, reference_image))
        
        return await asyncio.gather(*tasks)


class PollinationsProvider:
    """Pollinations.ai - Free image generation"""
    
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt"
    
    async def generate_image(self, prompt: str, output_path: Path, width: int = 1080,
                            height: int = 1920, reference_image: Optional[Path] = None) -> ImageResult:
        """Generate single image"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # URL encode prompt
                import urllib.parse
                encoded_prompt = urllib.parse.quote(prompt)
                url = f"{self.base_url}/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true"
                
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.get(url)
                    
                    if response.status_code == 429:
                        logger.warning(f"Pollinations attempt {attempt+1}/{max_retries} failed: 429")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(retry_delay)
                            continue
                        else:
                            # Fallback to alternative
                            logger.info("Falling back to alternative image service...")
                            return await self._generate_fallback(prompt, output_path, width, height)
                    
                    response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    logger.info(f"Image generated: {output_path.name}")
                    return ImageResult(
                        image_path=output_path,
                        prompt=prompt,
                        provider="pollinations"
                    )
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Pollinations attempt {attempt+1}/{max_retries} failed: {e}")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"Pollinations failed after {max_retries} attempts")
                    return await self._generate_fallback(prompt, output_path, width, height)
    
    async def _generate_fallback(self, prompt: str, output_path: Path, width: int, height: int) -> ImageResult:
        """Generate placeholder image as fallback"""
        try:
            # Create a simple colored image with text
            img = Image.new('RGB', (width, height), color=(50, 50, 100))
            draw = ImageDraw.Draw(img)
            
            # Add text
            text = prompt[:100] + "..." if len(prompt) > 100 else prompt
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            except:
                font = ImageFont.load_default()
            
            # Center text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) / 2
            y = (height - text_height) / 2
            
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            img.save(output_path)
            logger.warning(f"Generated fallback image: {output_path.name}")
            
            return ImageResult(
                image_path=output_path,
                prompt=prompt,
                provider="fallback"
            )
        except Exception as e:
            logger.error(f"Fallback image generation failed: {e}")
            raise
    
    async def generate_batch(self, prompts: List[str], output_dir: Path, width: int = 1080,
                            height: int = 1920, reference_image: Optional[Path] = None) -> List[ImageResult]:
        """Generate multiple images"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        tasks = []
        for i, prompt in enumerate(prompts):
            output_path = output_dir / f"scene_{i+1}.png"
            tasks.append(self.generate_image(prompt, output_path, width, height))
        
        return await asyncio.gather(*tasks)


class HuggingFaceProvider:
    """Hugging Face Inference API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "black-forest-labs/FLUX.1-schnell"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
    
    async def generate_image(self, prompt: str, output_path: Path, width: int = 1080,
                            height: int = 1920, reference_image: Optional[Path] = None) -> ImageResult:
        """Generate single image"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {"inputs": prompt}
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.api_url, headers=headers, json=data)
                response.raise_for_status()
                
                # Resize image to target dimensions
                img = Image.open(io.BytesIO(response.content))
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                img.save(output_path)
                
                logger.info(f"Image generated: {output_path.name}")
                return ImageResult(
                    image_path=output_path,
                    prompt=prompt,
                    provider="huggingface"
                )
        except Exception as e:
            logger.error(f"HuggingFace image generation failed: {e}")
            raise
    
    async def generate_batch(self, prompts: List[str], output_dir: Path, width: int = 1080,
                            height: int = 1920, reference_image: Optional[Path] = None) -> List[ImageResult]:
        """Generate multiple images"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        tasks = []
        for i, prompt in enumerate(prompts):
            output_path = output_dir / f"scene_{i+1}.png"
            tasks.append(self.generate_image(prompt, output_path, width, height))
        
        return await asyncio.gather(*tasks)
