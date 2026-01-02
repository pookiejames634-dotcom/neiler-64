#!/bin/bash
# Neiler-64 Professional GUI Launcher

echo "================================================"
echo "   Neiler-64 Professional Emulator"
echo "   Full System Visualization"
echo "================================================"
echo ""

# Check pygame
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Error: pygame not installed"
    echo "Install: pip install pygame"
    exit 1
fi

echo "Starting Professional GUI..."
echo ""

cd computer/emulator
python3 neiler_gui_pro.py "$@"
