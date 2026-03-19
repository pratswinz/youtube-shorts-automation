"""
Real-time Context Fetcher
Detects if a topic needs fresh info and fetches it from the web via DuckDuckGo
"""
from typing import Optional
from loguru import logger
from groq import AsyncGroq
from config.settings import settings


# Topics that almost always need latest/real-time info
REALTIME_KEYWORDS = [
    # Sports
    'ipl', 'cricket', 'rcb', 'csk', 'mi ', 'kkr', 'srh', 'dc ', 'pbks', 'rr ',
    'world cup', 'champions trophy', 'fifa', 'nfl', 'nba', 'football', 'match',
    'tournament', 'series', 'season', 'league', 'standings', 'score',
    # Current events
    'news', 'latest', '2025', '2026', 'today', 'recent', 'current', 'new ',
    'election', 'budget', 'government', 'policy', 'law', 'bill',
    # Entertainment
    'movie', 'film', 'box office', 'award', 'oscar', 'grammy', 'bollywood',
    'series', 'web series', 'ott', 'netflix', 'release',
    # Tech
    'launch', 'new phone', 'iphone', 'samsung', 'ai model', 'chatgpt', 'gemini',
    # Finance
    'stock', 'market', 'sensex', 'nifty', 'crypto', 'bitcoin', 'price',
]


async def needs_realtime_info(prompt: str) -> bool:
    """Detect if the prompt topic needs real-time/recent information"""
    prompt_lower = prompt.lower()
    for keyword in REALTIME_KEYWORDS:
        if keyword in prompt_lower:
            logger.info(f"Real-time info needed - keyword matched: '{keyword.strip()}'")
            return True
    return False


async def fetch_realtime_context(prompt: str, max_results: int = 5) -> Optional[str]:
    """
    Search the web for recent context about the topic.
    Returns a formatted string of recent facts to inject into script generation.
    """
    try:
        from duckduckgo_search import DDGS

        logger.info(f"Fetching real-time context for: {prompt}")

        # Build a clean search query
        search_query = _build_search_query(prompt)
        logger.info(f"Search query: {search_query}")

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(search_query, max_results=max_results):
                results.append({
                    'title': r.get('title', ''),
                    'body': r.get('body', '')
                })

        if not results:
            logger.warning("No search results found")
            return None

        # Format into context string
        context_lines = ["=== LATEST REAL-WORLD FACTS (use these, ignore older training data) ==="]
        for i, r in enumerate(results, 1):
            if r['body']:
                context_lines.append(f"{i}. {r['title']}: {r['body'][:200]}")

        context = "\n".join(context_lines)
        logger.info(f"Fetched {len(results)} real-time results")
        return context

    except Exception as e:
        logger.warning(f"Real-time context fetch failed: {e}")
        return None


def _build_search_query(prompt: str) -> str:
    """Build an optimized search query from the user prompt"""
    # Remove language/format instructions, keep the topic
    noise_words = [
        'create', 'make', 'video', 'hindi', 'english', 'short', 'reel',
        'about', 'on', 'regarding', 'please', 'a ', 'the ', 'for'
    ]
    query = prompt.lower()
    for word in noise_words:
        query = query.replace(word, ' ')

    # Clean up extra spaces
    query = ' '.join(query.split())

    # Add "2025" to get latest results if not already present
    if '2025' not in query and '2026' not in query:
        query = f"{query} 2025"

    return query.strip()
