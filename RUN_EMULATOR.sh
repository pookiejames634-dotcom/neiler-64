#!/bin/bash
# Quick launcher for Neiler-64 Graphical Emulator

echo "================================================"
echo "   Neiler-64 Graphical Emulator"
echo "================================================"
echo ""

# Check if pygame is installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Error: pygame is not installed"
    echo "Install with: pip install pygame"
    echo ""
    exit 1
fi

cd computer/emulator

# Run emulator
python3 neiler_emulator.py "$@"
