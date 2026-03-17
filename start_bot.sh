#!/bin/bash
# Startup script for YouTube Shorts Automation Bot

echo "🤖 YouTube Shorts Automation Bot - Startup"
echo "=========================================="
echo ""

# Kill any existing bot processes
echo "1. Stopping any existing bot processes..."
pkill -9 -f "python main.py" 2>/dev/null
sleep 2

# Clear Telegram state
echo "2. Clearing Telegram bot state..."
source venv/bin/activate
python clear_telegram.py

# Wait for Telegram to release
echo "3. Waiting 3 minutes for Telegram to release connection..."
echo "   (Close Telegram on all devices now if you haven't already)"
sleep 180

# Start the bot
echo "4. Starting bot..."
python main.py

echo ""
echo "✅ Bot started! Check the output above for any errors."
