"""
Application settings loaded from environment variables
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    environment: str = Field(default="development", description="Environment (development/production)")
    
    # Telegram
    telegram_bot_token: str = Field(..., description="Telegram bot token")
    
    # AI Providers
    script_provider: str = Field(default="groq", description="Script generation provider")
    groq_api_key: str = Field(default="", description="Groq API key")
    openai_api_key: str = Field(default="", description="OpenAI API key")
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    
    # TTS Providers
    tts_provider: str = Field(default="edge", description="TTS provider (edge/google/elevenlabs)")
    google_credentials_path: str = Field(default="config/credentials/google-tts.json", description="Google TTS credentials")
    google_project_id: str = Field(default="", description="Google Cloud project ID")
    elevenlabs_api_key: str = Field(default="", description="ElevenLabs API key")
    
    # Image Providers
    image_provider: str = Field(default="piapi", description="Image provider (piapi/huggingface/pollinations)")
    piapi_api_key: str = Field(default="", description="PiAPI key")
    huggingface_api_key: str = Field(default="", description="Hugging Face API key")
    
    # Video Settings
    video_format: str = Field(default="shorts", description="Video format (shorts/reels)")
    video_width: int = Field(default=1080, description="Video width")
    video_height: int = Field(default=1920, description="Video height")
    video_fps: int = Field(default=30, description="Video FPS")
    video_duration: int = Field(default=60, description="Target video duration in seconds")
    enable_subtitles: bool = Field(default=False, description="Enable text subtitles on video")
    
    # Queue Settings
    use_redis: bool = Field(default=False, description="Use Redis for job queue")
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database")
    
    # Paths
    output_dir: Path = Field(default=Path("output"), description="Output directory")
    temp_dir: Path = Field(default=Path("temp"), description="Temporary files directory")
    assets_dir: str = Field(default="assets", description="Assets directory")
    
    # FFmpeg
    ffmpeg_path: str = Field(default="ffmpeg", description="Path to FFmpeg binary")
    video_provider: str = Field(default="ffmpeg", description="Video provider")
    
    # Additional Settings
    default_video_duration: int = Field(default=60, description="Default video duration")
    default_language: str = Field(default="english", description="Default language")
    groq_model: str = Field(default="llama-3.3-70b-versatile", description="Groq model")
    
    # Debug & Logging
    debug: bool = Field(default=True, description="Debug mode")
    log_level: str = Field(default="INFO", description="Log level")
    
    # Database
    database_url: str = Field(default="sqlite:///automation.db", description="Database URL")
    
    # YouTube
    youtube_upload_enabled: bool = Field(default=False, description="Enable YouTube upload")
    google_cloud_key_path: str = Field(default="config/credentials/google_cloud_key.json", description="Google Cloud key path")
    youtube_oauth_path: str = Field(default="config/credentials/youtube_oauth.json", description="YouTube OAuth path")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"  # Allow extra fields from .env


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.output_dir.mkdir(exist_ok=True)
settings.temp_dir.mkdir(exist_ok=True)
