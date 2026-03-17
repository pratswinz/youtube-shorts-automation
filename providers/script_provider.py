"""
Script generation providers
Supports multiple AI providers: Groq, OpenAI, Anthropic
"""
import json
from typing import Dict, Any
from dataclasses import dataclass
from loguru import logger
from groq import AsyncGroq
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic


@dataclass
class ScriptResult:
    """Result from script generation"""
    script: str
    title: str
    description: str
    tags: list
    metadata: Dict[str, Any]


class GroqScriptProvider:
    """Script generation using Groq (Llama models)"""
    
    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    async def generate_script(self, prompt: str, duration: int, style: str, language: str) -> ScriptResult:
        """Generate video script"""
        system_prompt = f"""You are an expert video script writer for short-form content (YouTube Shorts, Instagram Reels, TikTok).

Create an engaging {duration}-second video script in {language} language.

Requirements:
1. Hook viewers in first 2 seconds
2. Clear, concise narration
3. Break into scenes (5-10 seconds each)
4. Natural pacing for {language} speakers
5. Engaging and informative

Output JSON format:
{{
    "title": "Catchy video title in {language}",
    "script": "Complete narration script in {language}",
    "description": "Video description in {language}",
    "tags": ["tag1", "tag2", "tag3"],
    "scenes": [
        {{
            "text": "Scene narration in {language}",
            "timestamp": 0,
            "duration": 5
        }}
    ]
}}"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return ScriptResult(
                script=result.get("script", ""),
                title=result.get("title", ""),
                description=result.get("description", ""),
                tags=result.get("tags", []),
                metadata={"scenes": result.get("scenes", [])}
            )
        except Exception as e:
            logger.error(f"Groq script generation failed: {e}")
            raise


class OpenAIScriptProvider:
    """Script generation using OpenAI (GPT models)"""
    
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    async def generate_script(self, prompt: str, duration: int, style: str, language: str) -> ScriptResult:
        """Generate video script"""
        system_prompt = f"""You are an expert video script writer for short-form content.

Create an engaging {duration}-second video script in {language} language.

Requirements:
1. Hook viewers in first 2 seconds
2. Clear, concise narration
3. Break into scenes (5-10 seconds each)
4. Natural pacing for {language} speakers
5. Engaging and informative

Output JSON format:
{{
    "title": "Catchy video title in {language}",
    "script": "Complete narration script in {language}",
    "description": "Video description in {language}",
    "tags": ["tag1", "tag2", "tag3"],
    "scenes": [
        {{
            "text": "Scene narration in {language}",
            "timestamp": 0,
            "duration": 5
        }}
    ]
}}"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return ScriptResult(
                script=result.get("script", ""),
                title=result.get("title", ""),
                description=result.get("description", ""),
                tags=result.get("tags", []),
                metadata={"scenes": result.get("scenes", [])}
            )
        except Exception as e:
            logger.error(f"OpenAI script generation failed: {e}")
            raise


class AnthropicScriptProvider:
    """Script generation using Anthropic (Claude models)"""
    
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def generate_script(self, prompt: str, duration: int, style: str, language: str) -> ScriptResult:
        """Generate video script"""
        system_prompt = f"""You are an expert video script writer for short-form content.

Create an engaging {duration}-second video script in {language} language.

Requirements:
1. Hook viewers in first 2 seconds
2. Clear, concise narration
3. Break into scenes (5-10 seconds each)
4. Natural pacing for {language} speakers
5. Engaging and informative

Output JSON format:
{{
    "title": "Catchy video title in {language}",
    "script": "Complete narration script in {language}",
    "description": "Video description in {language}",
    "tags": ["tag1", "tag2", "tag3"],
    "scenes": [
        {{
            "text": "Scene narration in {language}",
            "timestamp": 0,
            "duration": 5
        }}
    ]
}}"""

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = json.loads(response.content[0].text)
            
            return ScriptResult(
                script=result.get("script", ""),
                title=result.get("title", ""),
                description=result.get("description", ""),
                tags=result.get("tags", []),
                metadata={"scenes": result.get("scenes", [])}
            )
        except Exception as e:
            logger.error(f"Anthropic script generation failed: {e}")
            raise
