# Neilerdeck Hardware Specifications

## Overview
The Neilerdeck is a custom-built portable cyberdeck designed for hacking, development, and field operations.

## Core Components

### Computing
- **SBC**: Raspberry Pi 5 (8GB RAM) or CM4
  - Alternative: Orange Pi 5 Plus (16GB)
- **Storage**: 512GB NVMe SSD (M.2 2280)
- **MicroSD**: 128GB for boot/recovery

### Display
- **Primary**: 7" or 8" IPS touchscreen (1920x1200)
  - Options: Waveshare 7.9" QXGA, Elecrow 7" 1024x600
- **Secondary** (optional): 3.5" status display for system monitoring

### Input Devices
- **Keyboard**:
  - Option A: Mechanical split keyboard (Corne/Kyria layout)
  - Option B: Compact 60% mechanical keyboard
- **Pointing Device**:
  - Trackpoint module or trackball
  - Touchpad alternative

### Power System
- **Battery**:
  - 3S LiPo 5000-10000mAh (11.1V)
  - Or 18650 battery pack (4S configuration)
- **Power Management**:
  - PiSugar 3 or custom BMS
  - Voltage regulator (12V → 5V, 5A minimum)
- **Charging**: USB-C PD compatible (45W+)

### Connectivity
- **WiFi**: Built-in + external WiFi adapter for pentesting
  - Alfa AWUS036ACH or similar
- **Cellular**: Optional 4G/LTE HAT
- **Bluetooth**: Built-in BT 5.0+
- **Ethernet**: Gigabit Ethernet port
- **USB**: 4x USB-A 3.0, 2x USB-C
- **GPIO**: Exposed GPIO header for expansion

### Expansion Modules
- **SDR**: HackRF One or RTL-SDR
- **Storage**: Additional M.2 slot for expansion
- **LoRa**: Optional LoRa module for long-range comms

### Enclosure
- **Material**: 3D printed (PETG/ABS) or laser-cut acrylic
- **Form Factor**: Pelican case or custom design
- **Dimensions**: ~300mm x 200mm x 80mm (target)
- **Cooling**: Active cooling (40mm fans) + heatsinks

### Peripherals
- **Ports**: HDMI output, audio jack, microphone
- **LEDs**: Status indicators (power, activity, WiFi)
- **Switches**: Power switch, hardware kill switches

## Budget Estimate
- Core components: $200-300
- Display: $50-100
- Keyboard: $100-200
- Power system: $50-100
- Enclosure & misc: $50-100
- **Total**: $450-800 depending on options

## Power Consumption
- Idle: ~5W
- Normal use: ~10-15W
- Peak: ~25W
- Battery life: 4-8 hours (with 10000mAh battery)

## Performance Targets
- Boot time: < 30 seconds
- Operating temp: 0-40°C
- Weight: < 2kg
- Rugged enough for field use
