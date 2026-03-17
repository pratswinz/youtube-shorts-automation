"""
Content Analyzer
Analyzes user prompts to extract language, subject, and visual strategy
"""
import re
from typing import Dict, Any
from loguru import logger
from groq import AsyncGroq
from config.settings import settings


class ContentAnalyzer:
    """Analyzes content prompts for language, subject, and visual strategy"""
    
    def __init__(self):
        self.language_keywords = {
            'hindi': ['hindi', 'हिंदी', 'हिन्दी', 'devanagari'],
            'spanish': ['spanish', 'español', 'espanol'],
            'french': ['french', 'français', 'francais'],
            'german': ['german', 'deutsch'],
            'italian': ['italian', 'italiano'],
            'portuguese': ['portuguese', 'português', 'portugues'],
            'russian': ['russian', 'русский'],
            'japanese': ['japanese', '日本語', 'nihongo'],
            'korean': ['korean', '한국어', 'hangul'],
            'chinese': ['chinese', '中文', 'mandarin'],
            'arabic': ['arabic', 'عربي'],
            'english': ['english']
        }
    
    def detect_language(self, prompt: str, default: str = 'english') -> str:
        """
        Detect language from prompt
        
        Checks for explicit language mentions in the prompt
        """
        prompt_lower = prompt.lower()
        
        for language, keywords in self.language_keywords.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    logger.info(f"Detected language from keyword '{keyword}': {language}")
                    return language
        
        logger.info(f"No language detected, using default: {default}")
        return default
    
    async def analyze_prompt(self, prompt: str, style: str) -> Dict[str, Any]:
        """
        Analyze prompt with AI to extract visual strategy
        
        Returns:
            dict with keys: main_subject, visual_category, photography_style, mood, style_prefix
        """
        analysis_prompt = f"""Analyze this video creation prompt and extract key information for visual consistency.

USER PROMPT: {prompt}
VIDEO STYLE: {style}

Extract:
1. MAIN SUBJECT: The core topic/subject that should appear in all images (be specific, e.g., "guava fruit" not "fruit")
2. VISUAL CATEGORY: The type of content (food, fitness, tech, nature, lifestyle, education, business, etc.)
3. PHOTOGRAPHY STYLE: Appropriate photography style for this subject
4. MOOD: Visual mood/atmosphere (vibrant, calm, energetic, professional, etc.)

Output JSON format:
{{
    "main_subject": "specific subject name",
    "visual_category": "category",
    "photography_style": "style description",
    "mood": "mood description",
    "style_prefix": "Complete style instruction for image generation"
}}

Example 1:
Prompt: "Create hindi video about benefits of guava"
Output:
{{
    "main_subject": "guava fruit",
    "visual_category": "food",
    "photography_style": "professional food photography",
    "mood": "fresh, healthy, vibrant",
    "style_prefix": "guava fruit prominently featured, professional food photography, clean composition, soft natural lighting, fresh and vibrant mood, sharp focus, consistent visual style"
}}

Example 2:
Prompt: "Create video about morning workout routine"
Output:
{{
    "main_subject": "person exercising",
    "visual_category": "fitness",
    "photography_style": "professional fitness photography",
    "mood": "energetic, motivational, dynamic",
    "style_prefix": "person exercising prominently featured, professional fitness photography, dynamic composition, natural lighting, energetic and motivational mood, sharp focus, consistent visual style"
}}

Be specific and create a comprehensive style_prefix that will ensure visual consistency."""

        try:
            client = AsyncGroq(api_key=settings.groq_api_key)
            response = await client.chat.completions.create(
                model=settings.groq_model,
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            logger.info(f"AI Analysis - Subject: {result['main_subject']}, Category: {result['visual_category']}")
            return result
        except Exception as e:
            logger.warning(f"AI prompt analysis failed: {e}, using fallback")
            # Fallback to simple extraction
            return {
                "main_subject": prompt.split("about")[-1].strip() if "about" in prompt else "topic",
                "visual_category": "general",
                "photography_style": "professional photography",
                "mood": "engaging",
                "style_prefix": "professional photography, clean composition, natural lighting, sharp focus, consistent visual style"
            }
    
    def extract_metadata(self, prompt: str) -> Dict[str, Any]:
        """Extract additional metadata from prompt"""
        metadata = {
            'has_duration': False,
            'has_style': False,
            'has_language': False,
            'extracted_duration': None,
            'extracted_style': None,
            'extracted_language': None
        }
        
        # Extract duration (e.g., "60 seconds", "1 minute")
        duration_match = re.search(r'(\d+)\s*(second|sec|minute|min)', prompt.lower())
        if duration_match:
            value = int(duration_match.group(1))
            unit = duration_match.group(2)
            if 'min' in unit:
                value *= 60
            metadata['has_duration'] = True
            metadata['extracted_duration'] = value
        
        # Extract style mentions
        style_keywords = ['shorts', 'reel', 'tiktok', 'youtube', 'instagram', 'viral', 'trending']
        for keyword in style_keywords:
            if keyword in prompt.lower():
                metadata['has_style'] = True
                metadata['extracted_style'] = keyword
                break
        
        # Extract language
        language = self.detect_language(prompt)
        if language != 'english':
            metadata['has_language'] = True
            metadata['extracted_language'] = language
        
        return metadata
