"""
Real Image Fetcher
Detects real-world entities (people, places, objects) in prompts
and fetches their actual images from the web to use as PiAPI reference images.
"""
import asyncio
import hashlib
from pathlib import Path
from typing import Optional, List, Dict
from loguru import logger
import httpx
from groq import AsyncGroq
from config.settings import settings


# Cache directory for downloaded reference images
CACHE_DIR = Path(settings.temp_dir) / "ref_cache"


async def detect_real_entities(prompt: str, scenes: List[Dict]) -> Optional[Dict]:
    """
    Use AI to detect if the prompt contains real-world identifiable entities
    (celebrities, athletes, politicians, famous places, branded products).

    Returns dict with entity info or None if no real entities found.
    """
    all_text = prompt + " " + " ".join(s.get("text", "") for s in scenes[:3])

    detection_prompt = f"""Analyze this video topic and detect real-world identifiable entities.

TOPIC: {all_text}

Identify if there are:
1. REAL PEOPLE: celebrities, athletes, politicians, historical figures (e.g., "Virat Kohli", "Elon Musk", "Modi")
2. REAL PLACES: famous landmarks, cities, stadiums (e.g., "Wankhede Stadium", "Eiffel Tower")
3. REAL BRANDS/OBJECTS: specific branded products, logos (e.g., "iPhone 15", "Royal Enfield Bullet")

Output JSON:
{{
    "has_real_entity": true/false,
    "entities": [
        {{
            "name": "exact name to search",
            "type": "person/place/object",
            "search_query": "optimized image search query",
            "relevance": "why this is central to the video"
        }}
    ],
    "primary_entity": "most important entity name or null"
}}

Examples:
- "RCB video" → {{"has_real_entity": true, "entities": [{{"name": "RCB team", "type": "object", "search_query": "RCB Royal Challengers Bangalore IPL 2025 team photo"}}], "primary_entity": "RCB team"}}
- "benefits of guava" → {{"has_real_entity": false, "entities": [], "primary_entity": null}}
- "Virat Kohli batting" → {{"has_real_entity": true, "entities": [{{"name": "Virat Kohli", "type": "person", "search_query": "Virat Kohli batting cricket 2025 photo"}}], "primary_entity": "Virat Kohli"}}
"""

    try:
        client = AsyncGroq(api_key=settings.groq_api_key)
        response = await client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": detection_prompt}],
            temperature=0.1,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        import json
        result = json.loads(response.choices[0].message.content)

        if result.get("has_real_entity") and result.get("entities"):
            logger.info(f"Real entities detected: {[e['name'] for e in result['entities']]}")
            return result
        return None

    except Exception as e:
        logger.warning(f"Entity detection failed: {e}")
        return None


async def fetch_reference_image(entity: Dict, output_dir: Path) -> Optional[Path]:
    """
    Search DuckDuckGo images for the entity and download the best match.
    Returns path to downloaded image or None if failed.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    search_query = entity.get("search_query", entity.get("name", ""))
    entity_name = entity.get("name", "entity")

    # Use cached image if available
    cache_key = hashlib.md5(search_query.encode()).hexdigest()[:12]
    cache_path = CACHE_DIR / f"{cache_key}.jpg"
    if cache_path.exists():
        logger.info(f"Using cached reference image for: {entity_name}")
        return cache_path

    try:
        from duckduckgo_search import DDGS
        logger.info(f"Searching for real image: {search_query}")

        image_urls = []
        with DDGS() as ddgs:
            for r in ddgs.images(
                search_query,
                max_results=10,
                type_image="photo",
                size="Medium"
            ):
                url = r.get("image", "")
                if url and url.startswith("http") and any(
                    ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]
                ):
                    image_urls.append(url)

        if not image_urls:
            logger.warning(f"No images found for: {search_query}")
            return None

        # Try downloading images until one works
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            for url in image_urls[:5]:
                try:
                    resp = await client.get(url)
                    if resp.status_code == 200 and len(resp.content) > 10000:
                        # Validate it's a real image
                        from PIL import Image
                        import io
                        img = Image.open(io.BytesIO(resp.content))
                        img = img.convert("RGB")

                        # Save to cache
                        img.save(cache_path, "JPEG", quality=85)
                        logger.info(f"Downloaded reference image for: {entity_name} ({img.size})")
                        return cache_path
                except Exception as e:
                    logger.debug(f"Failed to download {url}: {e}")
                    continue

        logger.warning(f"Could not download any image for: {entity_name}")
        return None

    except Exception as e:
        logger.warning(f"Reference image fetch failed for {entity_name}: {e}")
        return None


async def get_reference_images_for_scenes(
    prompt: str,
    scenes: List[Dict],
    output_dir: Path
) -> Dict[int, Optional[Path]]:
    """
    Main entry point. Detects entities and fetches reference images.
    Returns a dict mapping scene_index -> reference_image_path (or None).

    If a primary entity is found, uses same reference for all scenes.
    """
    result = {i: None for i in range(len(scenes))}

    entity_info = await detect_real_entities(prompt, scenes)
    if not entity_info or not entity_info.get("has_real_entity"):
        logger.info("No real entities detected - using pure text-to-image")
        return result

    entities = entity_info.get("entities", [])
    if not entities:
        return result

    # Fetch the primary entity image
    primary = entities[0]
    ref_image = await fetch_reference_image(primary, output_dir)

    if ref_image:
        # Apply to all scenes
        for i in range(len(scenes)):
            result[i] = ref_image
        logger.info(f"Reference image '{primary['name']}' applied to all {len(scenes)} scenes")
    else:
        logger.warning(f"Could not get reference image for '{primary['name']}' - using text-to-image")

    return result
