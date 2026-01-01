#!/bin/bash
# Neilerdeck Automated Setup Script

set -e

echo "=== Neilerdeck Setup Starting ==="

# Update system
echo "[1/8] Updating system..."
sudo apt update && sudo apt upgrade -y

# Install base tools
echo "[2/8] Installing base tools..."
sudo apt install -y build-essential git vim tmux htop curl wget

# Install development tools
echo "[3/8] Installing development tools..."
sudo apt install -y python3 python3-pip python3-venv nodejs npm golang-go

# Install security tools
echo "[4/8] Installing security tools..."
sudo apt install -y nmap wireshark aircrack-ng hydra john hashcat sqlmap

# Install SDR tools
echo "[5/8] Installing SDR tools..."
sudo apt install -y rtl-sdr hackrf gqrx gnuradio

# Install networking tools
echo "[6/8] Installing networking tools..."
sudo apt install -y openvpn wireguard tor proxychains4

# Hardware support
echo "[7/8] Installing hardware tools..."
sudo apt install -y i2c-tools python3-smbus python3-rpi.gpio

# Configure services
echo "[8/8] Configuring services..."
sudo systemctl enable ssh
sudo ufw enable
sudo ufw allow ssh

# Python packages
pip3 install --user requests beautifulsoup4 scapy matplotlib numpy

echo "=== Setup Complete! ==="
echo "Please reboot the system."
