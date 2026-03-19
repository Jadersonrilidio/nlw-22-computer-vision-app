#!/bin/bash

# --- Vision Gesture Pro: Git Quick-Amend Script ---
# This script automates the process of adding changes and 'squashing' them 
# into your very last commit without changing the commit message.

# Stop the script if any command fails
set -e

# 1. Verify if we are inside a Git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "❌ Error: This folder is not a Git repository!"
    exit 1
fi

# 2. Stage all current changes
echo "📦 Staging all changes (git add .)..."
git add .

# 3. Amend the last commit
# --no-edit: keeps the previous commit message
echo "🔨 Amending last commit (git commit --amend --no-edit)..."
git commit --amend --no-edit

# 4. Show the updated log (last 5 entries)
echo "📜 Updated commit history:"
git log --oneline -n 5

echo "✅ Success! Your changes were merged into the last commit."
