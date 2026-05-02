#!/bin/bash
# Cross-platform build script for Linux/macOS

echo "=== AbaoSplitZip Build (Linux/macOS) ==="
echo ""

# Ensure we're in the script's directory
cd "$(dirname "$0")"

APP_NAME=$(python3 -c "from core.version import APP_NAME; print(APP_NAME)")

echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "Building executable..."
python3 -m PyInstaller build.spec --clean --noconfirm

echo ""
echo "Done! The executable is located in dist/${APP_NAME}"
