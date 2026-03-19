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
        
        prompt = f"""Visual director for {user_prompt}. Create {len(scenes)} image prompts in ENGLISH.

SCENES: {scene_texts}

SUBJECT: {visual_strategy.get('main_subject')} ({visual_strategy.get('visual_category')})
STYLE: {visual_strategy.get('photography_style')}, {visual_strategy.get('mood')} mood

RULES:
- Show actual subject prominently and realistically
- 15-20 words each, specific and concrete
- Use real-world knowledge: correct anatomy, realistic object usage, physically possible scenes
- For any human or animal: always specify realistic anatomy (correct limb count, proportions)
- For any action: describe exactly how it looks in reality (e.g., how a person actually holds/uses something)
- NO text, NO words, NO letters, NO captions, NO subtitles, NO watermarks
- English prompts only
- End each prompt with: "no text, no words, clean photorealistic image"

JSON: {{"image_prompts": ["prompt1", "prompt2", ...]}}"""

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
        
        inspection_prompt = f"""You are an expert visual QC inspector for AI image generation prompts. Topic: {user_prompt}

PROMPTS TO INSPECT:
{prompts_text}

SCENE NARRATION CONTEXT:
{scenes_text}

YOUR TASK: For each prompt, reason about what the AI image generator will actually produce.
Fix any prompt that would generate a physically impossible, anatomically wrong, or irrelevant image.

THINK through these questions for each prompt:
- Does this scene involve a real person/animal? → Verify correct number of limbs, body parts, realistic anatomy
- Does this involve physical objects? → Verify realistic object counts (can a person hold that many? does that exist?)
- Does this involve action/sport? → Verify the action is physically possible and equipment is used correctly
- Is the scene relevant to what the narration says?
- Could any part of this prompt cause text/words to appear in the image?

FIX RULES:
- Use your real-world knowledge to determine what is physically correct
- Be specific and explicit (e.g., don't say "player with bat" - say exactly what a realistic scene looks like)
- Add "anatomically correct, realistic human proportions" whenever humans are depicted
- Always end every refined prompt with: "no text, no words, no captions, clean photorealistic image"

Output JSON:
{{
    "inspection_results": [
        {{
            "scene": 1,
            "status": "approved/refined",
            "original": "...",
            "refined": "corrected realistic prompt, anatomically correct, no text, no words, no captions, clean photorealistic image",
            "reason": "what was wrong and how you fixed it"
        }}
    ],
    "overall_quality": "excellent/good/needs_improvement",
    "main_issues_fixed": ["issue1", "issue2"]
}}"""

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
            
            # Extract refined prompts with safety checks
            refined_prompts = []
            for i, item in enumerate(result['inspection_results']):
                refined = item.get('refined')
                # Fallback to original if refined is None or empty
                if not refined or refined.strip() == '':
                    refined = item.get('original', prompts[i] if i < len(prompts) else '')
                refined_prompts.append(refined)
            
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
