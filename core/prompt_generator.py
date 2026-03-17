"""
Prompt Generator
Generates and inspects image prompts for video scenes
"""
from typing import List, Dict, Any
from loguru import logger
from groq import AsyncGroq
from config.settings import settings


class PromptGenerator:
    """Generates and refines image prompts using AI"""
    
    def __init__(self):
        pass
    
    async def generate_prompts(self, user_prompt: str, scenes: List[Dict], 
                              language: str, visual_strategy: Dict[str, Any]) -> List[str]:
        """
        Generate contextual image prompts using AI based on narration
        
        Args:
            user_prompt: Original user prompt
            scenes: List of scene dictionaries with 'text' and 'timestamp'
            language: Target language for narration
            visual_strategy: Visual strategy from ContentAnalyzer
        
        Returns:
            List of image prompts (in English)
        """
        # Build context from scenes
        scene_texts = "\n".join([f"{i+1}. {scene['text']}" for i, scene in enumerate(scenes)])
        
        prompt = f"""You are an expert visual director for short-form videos.

USER WANTS TO CREATE: {user_prompt}

NARRATION SCRIPT (what will be spoken):
{scene_texts}

VISUAL STRATEGY:
- Main Subject: {visual_strategy.get('main_subject', 'N/A')}
- Category: {visual_strategy.get('visual_category', 'N/A')}
- Style: {visual_strategy.get('photography_style', 'N/A')}
- Mood: {visual_strategy.get('mood', 'N/A')}

YOUR TASK:
Generate SPECIFIC, DETAILED image prompts in ENGLISH for each scene that:
1. Directly visualize what's being said in that scene
2. Feature the main subject prominently (e.g., if it's about guava, show actual guava fruit)
3. Maintain consistent visual style across all scenes
4. Use concrete, specific descriptions (NOT abstract concepts)
5. Are optimized for AI image generation (Flux model)

RULES:
- Image prompts MUST be in ENGLISH (even if narration is in {language})
- Be SPECIFIC: "fresh guava fruit cut in half showing pink flesh" NOT "fruit on table"
- Show the ACTUAL subject: "guava" means show guava, not generic fruit
- Maintain VISUAL CONSISTENCY: use "same lighting", "same style", "same background"
- Each prompt should be 15-25 words, detailed and concrete

Output JSON format:
{{
    "image_prompts": [
        "detailed prompt for scene 1",
        "detailed prompt for scene 2",
        ...
    ]
}}"""

        try:
            client = AsyncGroq(api_key=settings.groq_api_key)
            response = await client.chat.completions.create(
                model=settings.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            prompts = result.get("image_prompts", [])
            
            # Add style prefix to each prompt
            style_prefix = visual_strategy.get('style_prefix', '')
            if style_prefix:
                prompts = [f"{style_prefix}, {p}" for p in prompts]
            
            logger.info(f"Generated {len(prompts)} image prompts")
            return prompts
        except Exception as e:
            logger.warning(f"AI image prompt generation failed: {e}, using fallback")
            # Fallback: create simple prompts from scene text
            style_prefix = visual_strategy.get('style_prefix', 'professional photography')
            return [f"{style_prefix}, {scene.get('text', '')[:50]}" for scene in scenes]
    
    async def inspect_and_refine(self, prompts: List[str], user_prompt: str, 
                                scenes: List[Dict]) -> Dict[str, Any]:
        """
        Inspector layer: validates and refines image prompts before generation
        
        Args:
            prompts: List of generated prompts
            user_prompt: Original user prompt
            scenes: List of scene dictionaries
        
        Returns:
            dict with keys: prompts (refined), inspection (details), quality (score)
        """
        # Build inspection context
        prompts_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(prompts)])
        scenes_text = "\n".join([f"{i+1}. {s['text'][:80]}" for i, s in enumerate(scenes)])
        
        inspection_prompt = f"""You are a quality control inspector for AI-generated image prompts.

USER WANTS: {user_prompt}

NARRATION SCENES:
{scenes_text}

GENERATED IMAGE PROMPTS:
{prompts_text}

YOUR TASK:
Inspect each prompt and ensure it will generate the EXACT image needed. Check for:

1. SPECIFICITY: Is the subject specific enough? (e.g., "guava fruit" not "fruit")
2. RELEVANCE: Does it match what's being said in that scene?
3. VISUAL CLARITY: Will an AI image model understand this clearly?
4. CONSISTENCY: Do all prompts maintain the same visual style?
5. COMPLETENESS: Are important details included (lighting, composition, etc.)?

For each prompt, either:
- APPROVE: If it's perfect as-is
- REFINE: If it needs improvement (provide refined version)

Output JSON format:
{{
    "inspection_results": [
        {{
            "scene": 1,
            "status": "approved" or "refined",
            "original": "original prompt",
            "refined": "refined prompt (if status is refined, otherwise same as original)",
            "reason": "why it was approved or what was improved"
        }},
        ...
    ],
    "overall_quality": "excellent/good/needs_improvement",
    "main_issues_fixed": ["issue 1", "issue 2"]
}}

Be strict - only approve if the prompt will generate EXACTLY what's needed."""

        try:
            client = AsyncGroq(api_key=settings.groq_api_key)
            response = await client.chat.completions.create(
                model=settings.groq_model,
                messages=[{"role": "user", "content": inspection_prompt}],
                temperature=0.3,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Extract refined prompts
            refined_prompts = [
                item['refined'] for item in result['inspection_results']
            ]
            
            # Log inspection results
            quality = result.get('overall_quality', 'unknown')
            issues_fixed = result.get('main_issues_fixed', [])
            
            logger.info(f"Prompt Inspector: Quality={quality}, Issues fixed={len(issues_fixed)}")
            for issue in issues_fixed:
                logger.info(f"  Fixed: {issue}")
            
            return {
                'prompts': refined_prompts,
                'inspection': result,
                'quality': quality
            }
            
        except Exception as e:
            logger.warning(f"Prompt inspection failed: {e}, using original prompts")
            return {
                'prompts': prompts,
                'inspection': None,
                'quality': 'not_inspected'
            }
