# Neilerdeck OS & Software Configuration

## Base OS
**Recommended**: Kali Linux ARM64 or Arch Linux ARM

## Installation Steps
1. Flash OS to NVMe SSD
2. Boot configuration for Pi 5
3. Enable NVMe boot in bootloader

## Essential Packages
```bash
# System
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git vim tmux htop

# Development
sudo apt install -y python3 python3-pip nodejs npm go rust

# Security Tools
sudo apt install -y nmap wireshark aircrack-ng hydra metasploit-framework
sudo apt install -y hashcat john sqlmap burpsuite

# SDR Tools
sudo apt install -y gqrx hackrf gnuradio

# Networking
sudo apt install -y openvpn wireguard tor proxychains

# Hardware
sudo apt install -y i2c-tools gpio-utils
```

## Configuration Files

### /boot/config.txt
```
dtparam=i2c_arm=on
dtparam=spi=on
gpu_mem=128
```

### ~/.bashrc additions
```bash
export PATH=$PATH:~/.local/bin
alias ll='ls -lah'
alias update='sudo apt update && sudo apt upgrade -y'
```

## Services to Enable
- SSH (with key auth only)
- UFW firewall
- Fail2ban
- Auto-mounting for external drives

## Power Management
```bash
# CPU governor for battery life
sudo apt install -y cpufrequtils
echo 'GOVERNOR="powersave"' | sudo tee /etc/default/cpufrequtils
```
