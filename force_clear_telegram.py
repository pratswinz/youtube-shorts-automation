#!/usr/bin/env python3
"""Force clear Telegram bot state with aggressive cleanup"""
import asyncio
import sys
from telegram import Bot
from config.settings import settings

async def force_clear():
    print("🔧 Force clearing Telegram bot state...")
    bot = Bot(token=settings.telegram_bot_token)
    
    try:
        # Delete webhook
        print("  → Deleting webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Get updates with high offset to clear queue
        print("  → Clearing update queue...")
        await bot.get_updates(offset=-1, timeout=1)
        
        # Verify connection
        me = await bot.get_me()
        print(f"\n✅ Bot cleared and connected: @{me.username}")
        print("✅ All pending updates dropped")
        print("\n⏳ Wait 3-5 minutes before starting the bot")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(force_clear())
