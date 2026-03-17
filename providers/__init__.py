"""
Provider factory functions
"""
from config.settings import settings


def get_script_provider():
    """Get configured script provider"""
    if settings.script_provider == "groq":
        from providers.script_provider import GroqScriptProvider
        return GroqScriptProvider(settings.groq_api_key)
    elif settings.script_provider == "openai":
        from providers.script_provider import OpenAIScriptProvider
        return OpenAIScriptProvider(settings.openai_api_key)
    elif settings.script_provider == "anthropic":
        from providers.script_provider import AnthropicScriptProvider
        return AnthropicScriptProvider(settings.anthropic_api_key)
    else:
        raise ValueError(f"Unknown script provider: {settings.script_provider}")


def get_tts_provider():
    """Get configured TTS provider"""
    if settings.tts_provider == "edge":
        from providers.tts_provider import EdgeTTSProvider
        return EdgeTTSProvider()
    elif settings.tts_provider == "google":
        from providers.tts_provider import GoogleTTSProvider
        return GoogleTTSProvider(
            settings.google_credentials_path,
            settings.google_project_id
        )
    elif settings.tts_provider == "elevenlabs":
        from providers.tts_provider import ElevenLabsTTSProvider
        return ElevenLabsTTSProvider(settings.elevenlabs_api_key)
    else:
        raise ValueError(f"Unknown TTS provider: {settings.tts_provider}")


def get_image_provider():
    """Get configured image provider"""
    if settings.image_provider == "piapi":
        from providers.image_provider import PiAPIProvider
        return PiAPIProvider(settings.piapi_api_key)
    elif settings.image_provider == "huggingface":
        from providers.image_provider import HuggingFaceProvider
        return HuggingFaceProvider(settings.huggingface_api_key)
    elif settings.image_provider == "pollinations":
        from providers.image_provider import PollinationsProvider
        return PollinationsProvider()
    else:
        raise ValueError(f"Unknown image provider: {settings.image_provider}")
