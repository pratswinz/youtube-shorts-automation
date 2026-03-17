#!/bin/bash
# Force stop all bot instances and clear Telegram state

echo "🛑 Force Stopping All Bot Instances"
echo "===================================="
echo ""

# 1. Kill ALL Python processes related to the bot
echo "1. Killing all bot-related processes..."
pkill -9 -f "python main.py" 2>/dev/null
pkill -9 -f "python.*main.py" 2>/dev/null
pkill -9 -f "telegram_bot" 2>/dev/null
sleep 2

# 2. Check for any remaining Python processes
echo "2. Checking for remaining processes..."
REMAINING=$(ps aux | grep -E "python.*main.py|telegram_bot" | grep -v grep | wc -l)
if [ "$REMAINING" -gt 0 ]; then
    echo "   ⚠️  Found $REMAINING remaining processes, force killing..."
    ps aux | grep -E "python.*main.py|telegram_bot" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
    sleep 2
else
    echo "   ✅ No remaining processes found"
fi

# 3. Remove PID file if exists
echo "3. Cleaning up PID files..."
rm -f bot.pid 2>/dev/null
echo "   ✅ PID files removed"

# 4. Clear Telegram webhook and pending updates
echo "4. Clearing Telegram state..."
cd "/Volumes/disc 2/coding/automation"
source venv/bin/activate
python clear_telegram.py

echo ""
echo "✅ All bot instances stopped and Telegram state cleared!"
echo ""
echo "⏰ IMPORTANT: Wait 5 minutes before starting the bot again."
echo "   This allows Telegram's servers to fully release the connection."
echo ""
echo "📱 Also make sure to:"
echo "   - Close Telegram app on your phone"
echo "   - Close Telegram Desktop on your computer"
echo "   - Close any Telegram Web tabs in your browser"
echo ""
echo "After 5 minutes, run: ./start_bot.sh"
