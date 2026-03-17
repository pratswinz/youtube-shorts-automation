# Fixing Telegram "Conflict: terminated by other getUpdates request"

## What This Error Means

This error occurs when **multiple connections** are trying to receive updates from Telegram at the same time. Telegram's API only allows **ONE active connection** per bot token.

## Common Causes

1. ✅ **Multiple bot instances running locally** (most common)
2. ✅ **Bot running on multiple machines** (e.g., local + server)
3. ✅ **Webhook enabled while using polling**
4. ✅ **Telegram app open on multiple devices**
5. ✅ **Stale connections on Telegram's servers**

## Solution: Complete Reset

### Step 1: Force Stop Everything

Run the force stop script:

```bash
cd "/Volumes/disc 2/coding/automation"
./force_stop_all.sh
```

This will:
- Kill all bot processes
- Remove PID files
- Clear Telegram webhook
- Clear pending updates

### Step 2: Close Telegram Everywhere

**CRITICAL:** Close Telegram on ALL devices:

- ❌ Close Telegram on your **phone**
- ❌ Close Telegram **Desktop** app
- ❌ Close all **Telegram Web** browser tabs
- ❌ Close any **Telegram Mini Apps**

### Step 3: Wait 5 Minutes

This is **NOT optional**. Telegram's servers need time to:
- Release the old connection
- Clear internal state
- Reset rate limits

Set a timer for **5 minutes** and wait.

### Step 4: Start the Bot

After 5 minutes:

```bash
./start_bot.sh
```

## Manual Troubleshooting

### Check for Running Processes

```bash
# Check for bot processes
ps aux | grep "python main.py"

# Kill specific PID
kill -9 <PID>

# Kill all Python processes (careful!)
pkill -9 python
```

### Check for Webhook

```bash
# Clear webhook manually
source venv/bin/activate
python clear_telegram.py
```

### Check PID File

```bash
# Remove stale PID file
rm -f bot.pid
```

### Verify Only One Instance

```bash
# Count running instances
ps aux | grep "python main.py" | grep -v grep | wc -l
# Should return: 0 (when stopped) or 1 (when running)
```

## Prevention Tips

### 1. Always Use the Startup Script

```bash
./start_bot.sh
```

This script handles:
- Stopping old instances
- Clearing Telegram state
- Waiting for release
- Starting cleanly

### 2. Don't Run Multiple Instances

❌ **DON'T:**
- Run `python main.py` multiple times
- Run bot on multiple machines with same token
- Mix webhook and polling modes

✅ **DO:**
- Use one bot instance at a time
- Use the provided scripts
- Wait for proper shutdown

### 3. Proper Shutdown

Always stop the bot properly:

```bash
# Press Ctrl+C in the terminal
# OR
./force_stop_all.sh
```

### 4. Monitor the Bot

Check if bot is running:

```bash
# Check process
ps aux | grep "python main.py"

# Check PID file
cat bot.pid
```

## Advanced: Webhook vs Polling

### Current Setup: Polling (Recommended)

- ✅ Simpler to manage
- ✅ Works behind firewalls
- ✅ No server configuration needed
- ❌ Less efficient for high traffic

### If You Want to Use Webhook

1. Set up a public HTTPS endpoint
2. Configure webhook URL in Telegram
3. Disable polling in code
4. Handle incoming POST requests

**Note:** Stick with polling unless you have specific needs.

## Still Having Issues?

### Check Telegram Bot Status

```bash
# Test bot connection
source venv/bin/activate
python -c "
from telegram import Bot
from config.settings import settings
import asyncio

async def test():
    bot = Bot(token=settings.telegram_bot_token)
    me = await bot.get_me()
    print(f'Bot: @{me.username}')
    print(f'ID: {me.id}')

asyncio.run(test())
"
```

### Check for Webhook

```bash
# Check if webhook is set
python -c "
from telegram import Bot
from config.settings import settings
import asyncio

async def check():
    bot = Bot(token=settings.telegram_bot_token)
    info = await bot.get_webhook_info()
    print(f'Webhook URL: {info.url}')
    print(f'Pending updates: {info.pending_update_count}')

asyncio.run(check())
"
```

### Reset Everything (Nuclear Option)

If nothing else works:

```bash
# 1. Stop everything
./force_stop_all.sh

# 2. Reboot your computer
sudo reboot

# 3. Wait 10 minutes after reboot

# 4. Start fresh
./start_bot.sh
```

## Error Messages Explained

### "Conflict: terminated by other getUpdates request"
- **Cause:** Multiple polling connections
- **Fix:** Stop all instances, wait 5 minutes

### "NetworkError: Connection refused"
- **Cause:** Bot not running or wrong port
- **Fix:** Check if bot is running

### "Unauthorized"
- **Cause:** Invalid bot token
- **Fix:** Check TELEGRAM_BOT_TOKEN in .env

### "Bad Request: wrong file identifier"
- **Cause:** File ID expired or invalid
- **Fix:** Regenerate the file

## Quick Reference

```bash
# Stop everything
./force_stop_all.sh

# Wait 5 minutes
sleep 300

# Start bot
./start_bot.sh

# Check if running
ps aux | grep "python main.py"

# View logs
tail -f logs/bot.log
```

## Contact

If you're still having issues after following this guide:

1. Check the bot logs in the terminal
2. Look for specific error messages
3. Verify your API keys in `.env`
4. Ensure you have internet connectivity
5. Try rebooting your computer

---

**Remember:** The key to avoiding conflicts is:
1. ✅ Only one bot instance at a time
2. ✅ Use the provided scripts
3. ✅ Wait 5 minutes after stopping
4. ✅ Close Telegram on all devices
