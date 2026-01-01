# Neilerdeck Quick Start Guide

## Getting Your Neilerdeck Running in 30 Minutes

### Prerequisites
- Neilerdeck fully assembled
- MicroSD card (32GB+) or NVMe SSD
- Power supply or charged battery
- WiFi network access

### Step 1: Flash OS (10 min)

```bash
# Download Raspberry Pi Imager
# Flash Kali Linux ARM64 or Raspberry Pi OS

# Or use dd:
sudo dd if=kali-linux-arm64.img of=/dev/sdX bs=4M status=progress
```

### Step 2: First Boot (5 min)

1. Insert SD card or NVMe
2. Power on the Neilerdeck
3. Wait for boot (30-60 seconds)
4. Default login:
   - Username: `kali` or `pi`
   - Password: `kali` or `raspberry`

### Step 3: Basic Setup (10 min)

```bash
# Change password
passwd

# Update system
sudo apt update && sudo apt upgrade -y

# Set hostname
sudo hostnamectl set-hostname neilerdeck

# Configure WiFi
sudo nmtui

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh
```

### Step 4: Run Setup Script (5 min)

```bash
# Clone neilerdeck repo
git clone https://github.com/yourusername/neilerdeck.git
cd neilerdeck

# Run automated setup
chmod +x software/install.sh
sudo ./software/install.sh
```

### Step 5: Test Everything

```bash
# Check WiFi
iwconfig

# Check USB devices
lsusb

# Check SDR (if installed)
rtl_test

# Check GPIO
gpio readall

# Monitor system
htop
```

## Essential Commands

```bash
# System info
neofetch

# Battery status (if using PiSugar)
echo get battery | nc -q 0 127.0.0.1 8423

# Temperature
vcgencmd measure_temp

# Update everything
sudo apt update && sudo apt upgrade -y

# Reboot
sudo reboot
```

## Common Tasks

### Connect to WiFi
```bash
nmcli device wifi list
nmcli device wifi connect "SSID" password "password"
```

### Start Pentesting
```bash
# Put WiFi adapter in monitor mode
sudo airmon-ng start wlan1

# Scan for networks
sudo airodump-ng wlan1mon
```

### Use SDR
```bash
# Start GQRX
gqrx

# Or command line
rtl_fm -f 433.92M -M am - | aplay
```

### Access from Another Computer
```bash
# SSH into neilerdeck
ssh kali@neilerdeck.local

# Copy files
scp file.txt kali@neilerdeck.local:~/
```

## Troubleshooting

### No WiFi
```bash
sudo systemctl restart NetworkManager
```

### Display Issues
```bash
# Edit boot config
sudo nano /boot/config.txt
# Add: hdmi_force_hotplug=1
```

### Performance Issues
```bash
# Check CPU frequency
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq

# Set performance mode
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

## Next Steps

- Read [ASSEMBLY.md](ASSEMBLY.md) for hardware details
- Check [OS-SETUP.md](../software/OS-SETUP.md) for advanced configuration
- Explore AI agents in `ai-agents/` directory
- Join the community (forums/discord link)

## Safety Reminders

- Monitor temperature during heavy use
- Don't discharge LiPo battery below 3.3V per cell
- Keep ventilation clear
- Use ESD protection when opening case

Happy hacking!
