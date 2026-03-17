#!/usr/bin/env python3
"""Aggressively clear Telegram bot state with multiple retries"""
import asyncio
import sys
from telegram import Bot
from telegram.error import Conflict, NetworkError
from config.settings import settings

async def aggressive_clear():
    print("🔧 Aggressively clearing Telegram bot state...")
    print("=" * 60)
    bot = Bot(token=settings.telegram_bot_token)
    
    try:
        # Step 1: Delete webhook
        print("\n1. Deleting webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        print("   ✅ Webhook deleted")
        
        # Step 2: Try to get updates with offset -1 to clear queue
        print("\n2. Clearing update queue with offset -1...")
        try:
            await bot.get_updates(offset=-1, timeout=1)
            print("   ✅ Update queue cleared")
        except Conflict:
            print("   ⚠️  Conflict detected (expected)")
        
        # Step 3: Wait a bit
        print("\n3. Waiting 10 seconds...")
        await asyncio.sleep(10)
        
        # Step 4: Try multiple times with increasing offsets
        print("\n4. Attempting to clear with multiple offsets...")
        for offset in [-1, 0, 1]:
            try:
                print(f"   Trying offset {offset}...")
                result = await bot.get_updates(offset=offset, timeout=1, allowed_updates=[])
                print(f"   ✅ Got {len(result)} updates with offset {offset}")
                if result:
                    # Get the last update ID and clear everything after it
                    last_id = result[-1].update_id
                    print(f"   Last update ID: {last_id}, clearing...")
                    await bot.get_updates(offset=last_id + 1, timeout=1)
            except Conflict as e:
                print(f"   ⚠️  Conflict at offset {offset}: {e}")
                continue
            except Exception as e:
                print(f"   ℹ️  {type(e).__name__}: {e}")
                continue
        
        # Step 5: Verify bot connection
        print("\n5. Verifying bot connection...")
        me = await bot.get_me()
        print(f"   ✅ Bot connected: @{me.username} (ID: {me.id})")
        
        # Step 6: Check webhook status
        print("\n6. Checking webhook status...")
        webhook_info = await bot.get_webhook_info()
        print(f"   Webhook URL: {webhook_info.url or 'None'}")
        print(f"   Pending updates: {webhook_info.pending_update_count}")
        
        print("\n" + "=" * 60)
        print("✅ Aggressive clear completed!")
        print("\n⏰ CRITICAL: Wait at least 10 MINUTES before starting the bot.")
        print("   Telegram's servers need time to fully release the connection.")
        print("\n💡 If conflict persists:")
        print("   1. Wait 10 minutes (not 5)")
        print("   2. Reboot your computer")
        print("   3. Wait another 5 minutes after reboot")
        print("   4. Then run: ./start_bot.sh")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(aggressive_clear())
