#!/usr/bin/env python3
"""
Main entry point for the video automation system
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

from config.settings import settings
from core.job_queue import JobQueue
from bot.telegram_bot import TelegramBot


class BotLock:
    """Simple file-based lock to prevent multiple instances"""
    
    def __init__(self, lock_file: Path = Path("bot.pid")):
        self.lock_file = lock_file
        self.pid = None
    
    def acquire(self) -> bool:
        """Acquire lock by writing PID to file"""
        import os
        
        if self.lock_file.exists():
            try:
                old_pid = int(self.lock_file.read_text().strip())
                # Check if process is still running
                os.kill(old_pid, 0)
                logger.error(f"Bot already running with PID {old_pid}")
                return False
            except (ProcessLookupError, ValueError):
                # Process not running or invalid PID, remove stale lock
                self.lock_file.unlink()
        
        self.pid = os.getpid()
        self.lock_file.write_text(str(self.pid))
        logger.success(f"Bot instance locked (PID: {self.pid})")
        return True
    
    def release(self):
        """Release lock by removing PID file"""
        if self.lock_file.exists():
            self.lock_file.unlink()
            logger.info("Bot instance lock released")


def validate_config():
    """Validate critical configuration"""
    errors = []
    
    # Check Telegram token
    if not settings.telegram_bot_token or settings.telegram_bot_token == "your_telegram_bot_token_here":
        errors.append("TELEGRAM_BOT_TOKEN not set in .env")
    
    # Check Groq API key
    if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
        errors.append("GROQ_API_KEY not set in .env")
    
    # Check image provider
    if settings.image_provider == "piapi":
        if not settings.piapi_api_key or settings.piapi_api_key == "your_piapi_key_here":
            errors.append("PIAPI_API_KEY not set but IMAGE_PROVIDER=piapi")
    
    if errors:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        logger.info("\nPlease update your .env file and try again.")
        return False
    
    logger.success("Configuration validated")
    return True


def main():
    """Main application entry point"""
    
    # Validate configuration
    if not validate_config():
        sys.exit(1)
    
    # Acquire bot lock
    lock = BotLock()
    if not lock.acquire():
        sys.exit(1)
    
    try:
        # Log startup info
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"Script Provider: {settings.script_provider}")
        logger.info(f"TTS Provider: {settings.tts_provider}")
        logger.info(f"Image Provider: {settings.image_provider}")
        logger.info(f"Video Format: {settings.video_format}")
        logger.info(f"Redis Queue: {'Enabled' if settings.use_redis else 'Disabled (in-memory)'}")
        
        logger.success("System ready! Starting Telegram bot...")
        
        # Initialize and run Telegram bot
        bot = TelegramBot(settings.telegram_bot_token)
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        lock.release()


if __name__ == "__main__":
    main()
