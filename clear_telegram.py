#!/usr/bin/env python3
"""
Clear Telegram bot state (webhook and pending updates)
"""
import asyncio
from telegram import Bot
from config.settings import settings


async def clear_state():
    """Clear Telegram bot state"""
    print("Clearing Telegram bot state...")
    
    bot = Bot(token=settings.telegram_bot_token)
    
    # Delete webhook and clear pending updates
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Get bot info to verify connection
    me = await bot.get_me()
    
    print(f"✅ Cleared webhook and pending updates")
    print(f"✅ Bot connected: @{me.username}")
    print()
    print("✅ Done! Now run: ./start.sh")
    print()


if __name__ == "__main__":
    asyncio.run(clear_state())
