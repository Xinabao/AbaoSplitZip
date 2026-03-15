#!/bin/bash
# Cross-platform build script for Linux/macOS

echo "=== AbaoZip Build (Linux/macOS) ==="
echo ""

# Ensure we're in the script's directory
cd "$(dirname "$0")"

echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "Building executable..."
python3 -m PyInstaller build.spec --clean --noconfirm

echo ""
echo "Done! The executable is located in dist/AbaoZip"
