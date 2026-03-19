"""
Telegram Bot
Handles user interactions and video generation requests
"""
import asyncio
from pathlib import Path
from typing import Optional
from loguru import logger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from config.settings import settings
from config.constants import JobStatus
from core.video_generator import VideoGenerator, VideoJob
from core.job_queue import job_queue


class TelegramBot:
    """Telegram bot for video generation"""
    
    def __init__(self, token: str):
        self.token = token
        # Simple builder like it was on Sunday
        self.app = Application.builder().token(token).build()
        self.video_generator = VideoGenerator()
        
        # Register handlers
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("switch", self.cmd_switch))
        self.app.add_handler(CommandHandler("cancel", self.cmd_cancel))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_prompt))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_text = """🎬 Welcome to YouTube Shorts Generator!

I can create professional short-form videos from your prompts.

**How to use:**
1. Send me a prompt (e.g., "Create a video about meditation benefits")
2. I'll generate a 60-second video with:
   - AI-generated script
   - Professional voiceover
   - Relevant images
   - Smooth transitions

**Commands:**
/help - Show help
/status - Check job status
/switch - Switch AI providers
/cancel - Cancel current job

**Supported languages:**
English, Hindi, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic

Just mention the language in your prompt!

Ready? Send me your first prompt! 🚀"""
        
        await update.message.reply_text(welcome_text)
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """📚 **Help Guide**

**Basic Usage:**
Simply send a text prompt describing the video you want to create.

**Examples:**
• "Create a video about benefits of meditation"
• "Make a hindi video about guava health benefits"
• "Create a workout motivation video"

**Advanced Options:**
• Specify language: "Create hindi video about..."
• Specify duration: "Create 45 second video about..."
• Specify style: "Create energetic video about..."

**Commands:**
/start - Welcome message
/help - This help message
/status <job_id> - Check job status
/switch <provider> <type> - Switch AI provider
/cancel <job_id> - Cancel a job

**Provider Switching:**
/switch image piapi - Better images ($0.008/video)
/switch tts elevenlabs - Premium voice ($0.05/video)
/switch script openai - Better scripts ($0.01/video)

**Current Setup:**
Script: {script_provider}
Voice: {tts_provider}
Images: {image_provider}

Need help? Just ask!"""
        
        await update.message.reply_text(
            help_text.format(
                script_provider=settings.script_provider,
                tts_provider=settings.tts_provider,
                image_provider=settings.image_provider
            )
        )
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        if not context.args:
            await update.message.reply_text("Usage: /status <job_id>")
            return
        
        job_id = context.args[0]
        status = job_queue.get_job_status(job_id)
        
        if not status:
            await update.message.reply_text(f"Job {job_id} not found")
            return
        
        status_text = f"""📊 **Job Status**

Job ID: {job_id}
Status: {status['status']}
Progress: {status['progress']}%

Created: {status['created_at']}
"""
        
        if status.get('error'):
            status_text += f"\n❌ Error: {status['error']}"
        
        if status.get('output_path'):
            status_text += f"\n✅ Video ready!"
        
        await update.message.reply_text(status_text)
    
    async def cmd_switch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /switch command"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "Usage: /switch <type> <provider>\n\n"
                "Examples:\n"
                "/switch image piapi\n"
                "/switch tts elevenlabs\n"
                "/switch script openai"
            )
            return
        
        provider_type = context.args[0]
        provider_name = context.args[1]
        
        try:
            if provider_type == "script":
                self.video_generator.switch_script_provider(provider_name)
            elif provider_type == "tts":
                self.video_generator.switch_tts_provider(provider_name)
            elif provider_type == "image":
                self.video_generator.switch_image_provider(provider_name)
            else:
                await update.message.reply_text(
                    f"Unknown provider type: {provider_type}\n"
                    "Valid types: script, tts, image"
                )
                return
            
            await update.message.reply_text(
                f"✅ Switched {provider_type} provider to: {provider_name}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to switch provider: {e}")
    
    async def cmd_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cancel command"""
        if not context.args:
            await update.message.reply_text("Usage: /cancel <job_id>")
            return
        
        job_id = context.args[0]
        success = job_queue.cancel_job(job_id)
        
        if success:
            await update.message.reply_text(f"✅ Job {job_id} cancelled")
        else:
            await update.message.reply_text(f"❌ Failed to cancel job {job_id}")
    
    async def handle_prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text prompts"""
        user_id = update.effective_user.id
        prompt = update.message.text
        
        logger.info(f"Received prompt from user {user_id}: {prompt}")
        
        # Create notification callback
        async def notify(message: str):
            try:
                await update.message.reply_text(message)
            except Exception as e:
                logger.warning(f"Failed to send notification: {e}")
        
        # Create job
        job = VideoJob(
            job_id=job_queue.generate_job_id(),
            user_id=user_id,
            prompt=prompt,
            duration=60,  # Default 60 seconds
            style="engaging",
            status=JobStatus.PENDING,
            notification_callback=notify
        )
        
        # Add to queue
        await job_queue.add_job(job)
        
        # Send confirmation
        await update.message.reply_text(
            f"✅ Video generation started!\n\n"
            f"Job ID: {job.job_id}\n"
            f"Prompt: {prompt}\n\n"
            f"I'll send you the video when it's ready (usually 60-90 seconds).\n\n"
            f"Use /status {job.job_id} to check progress."
        )
        
        # Monitor job in background
        asyncio.create_task(self._monitor_job(job.job_id, update))
    
    async def _monitor_job(self, job_id: str, update: Update):
        """Monitor job progress and send updates"""
        last_progress = 0
        
        while True:
            await asyncio.sleep(5)
            
            status = job_queue.get_job_status(job_id)
            if not status:
                break
            
            # Send progress updates
            progress = status['progress']
            if progress > last_progress and progress % 25 == 0:
                await update.message.reply_text(
                    f"⏳ Progress: {progress}%\n{status['status']}"
                )
                last_progress = progress
            
            # Check if completed
            if status['status'] == JobStatus.COMPLETED:
                await self._send_completed_video(job_id, update)
                break
            
            # Check if failed
            if status['status'] == JobStatus.FAILED:
                await update.message.reply_text(
                    f"❌ Video generation failed\n\n"
                    f"Error: {status.get('error', 'Unknown error')}\n\n"
                    f"Please try again or contact support."
                )
                break
    
    async def _send_completed_video(self, job_id: str, update: Update):
        """Send completed video to user"""
        status = job_queue.get_job_status(job_id)
        
        if not status or not status.get('output_path'):
            await update.message.reply_text("❌ Video file not found")
            return
        
        video_path = Path(status['output_path'])
        
        if not video_path.exists():
            await update.message.reply_text("❌ Video file not found")
            return
        
        try:
            # Send video
            await update.message.reply_video(
                video=open(video_path, 'rb'),
                caption=f"✅ Your video is ready!\n\n"
                        f"Job ID: {job_id}\n"
                        f"Duration: {status.get('duration', 'N/A')}s",
                supports_streaming=True
            )
            
            # Send thumbnail if available
            thumbnail_path = status.get('thumbnail_path')
            if thumbnail_path and Path(thumbnail_path).exists():
                await update.message.reply_photo(
                    photo=open(thumbnail_path, 'rb'),
                    caption="📸 Thumbnail"
                )
            
            logger.success(f"Video sent to user for job {job_id}")
        except Exception as e:
            logger.error(f"Failed to send video: {e}")
            await update.message.reply_text(
                f"❌ Failed to send video: {e}\n\n"
                f"Video is saved at: {video_path}"
            )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline buttons"""
        query = update.callback_query
        await query.answer()
        
        # Handle different callback actions here
        # (Can be extended for future features)
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        logger.success("Bot starting with polling...")
        self.app.run_polling(drop_pending_updates=True)


def start_bot():
    """Start the bot (entry point)"""
    bot = TelegramBot(settings.telegram_bot_token)
    bot.run()
