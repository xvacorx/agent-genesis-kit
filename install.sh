#!/usr/bin/env bash
# Agent Genesis Kit — One-Liner Installer for Linux & macOS
# Architected by Viktor (Vik) - Viklabs (https://viklabs.pages.dev/)
# Usage: curl -fsSL https://raw.githubusercontent.com/xvacorx/agent-genesis-kit/main/install.sh | bash

set -e

echo ""
echo -e "\033[0;36m==========================================================\033[0m"
echo -e "\033[0;36m  ⚡ AGENT GENESIS KIT — Bootstrap & Onboarding Matrix   \033[0m"
echo -e "\033[0;90m  Architected by Viktor (Vik) — viklabs.pages.dev              \033[0m"
echo -e "\033[0;36m==========================================================\033[0m"
echo ""

REPO_URL="https://github.com/xvacorx/agent-genesis-kit"
ZIP_URL="https://github.com/xvacorx/agent-genesis-kit/archive/refs/heads/main.zip"
TARGET_DIR="$(pwd)/agent-genesis-kit"

if command -v git &> /dev/null; then
    echo -e "\033[0;32m📦 Git detected! Cloning repository...\033[0m"
    if [ -d "$TARGET_DIR" ]; then
        echo -e "\033[0;33mℹ️  Folder 'agent-genesis-kit' already exists. Updating...\033[0m"
        git -C "$TARGET_DIR" pull
    else
        git clone "$REPO_URL" "$TARGET_DIR"
    fi
else
    echo -e "\033[0;33m🌐 Git not found. Downloading release package directly...\033[0m"
    TEMP_DIR=$(mktemp -d)
    curl -fsSL "$ZIP_URL" -o "$TEMP_DIR/genesis.zip"
    unzip -q "$TEMP_DIR/genesis.zip" -d "$TEMP_DIR"
    mkdir -p "$TARGET_DIR"
    cp -r "$TEMP_DIR/agent-genesis-kit-main/"* "$TARGET_DIR/"
    rm -rf "$TEMP_DIR"
fi

echo ""
echo -e "\033[0;32m==========================================================\033[0m"
echo -e "\033[0;32m  ✅ INSTALLATION COMPLETE!                               \033[0m"
echo -e "\033[0;32m==========================================================\033[0m"
echo ""
echo -e "\033[1;37m🚀 Next Steps to start your AI assistant:\033[0m"
echo -e "  1. Open Antigravity IDE, Claude Code, or Cursor."
echo -e "  2. Open the folder: \033[0;36m$TARGET_DIR\033[0m"
echo -e "  3. Open the chat and type: \033[0;33m/setup\033[0m"
echo ""
echo -e "\033[0;90m✨ Created by Viktor (Vik) at Viklabs — https://viklabs.pages.dev/\033[0m"
echo ""
