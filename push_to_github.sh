#!/bin/bash

echo "🚀 Push to GitHub"
echo "================="
echo ""
echo "First, create a new repository on GitHub:"
echo "  1. Go to: https://github.com/new"
echo "  2. Repository name: youtube-shorts-automation"
echo "  3. Description: AI-powered YouTube Shorts automation via Telegram"
echo "  4. Public or Private (your choice)"
echo "  5. DO NOT initialize with README"
echo "  6. Click 'Create repository'"
echo ""
read -p "Press ENTER after creating the repository on GitHub..."
echo ""

# Set repository name
REPO_NAME="youtube-shorts-automation"
GITHUB_USER="pratswinz"

echo "📡 Adding remote..."
git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git" 2>/dev/null || \
git remote set-url origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "✅ Remote added: https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo ""

echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Your code is now on GitHub!"
    echo ""
    echo "🔗 View your repository:"
    echo "   https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo ""
else
    echo ""
    echo "❌ Push failed. You may need to:"
    echo "   1. Generate a Personal Access Token: https://github.com/settings/tokens"
    echo "   2. Use the token as your password when prompted"
    echo ""
    echo "Or try again with:"
    echo "   git push -u origin main"
fi
