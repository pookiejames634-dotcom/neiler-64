# Neilerdeck

A custom cyberdeck built for security research, development, and portable computing.

## Features

- **Portable**: Lightweight and rugged design for field work
- **Powerful**: Raspberry Pi 5 with 8GB RAM, NVMe storage
- **Versatile**: Built-in SDR, WiFi pentesting, 4G connectivity
- **Expandable**: Multiple USB ports, GPIO access, expansion slots
- **Long Battery Life**: 8+ hours of runtime with 10000mAh battery
- **AI-Assisted**: Helper agents for component research, config generation, and documentation

## Quick Links

- [Hardware Specifications](hardware/SPECS.md)
- [Component Shopping List](hardware/COMPONENTS.md)
- [Software Setup](software/OS-SETUP.md)
- [3D Models](3d-models/README.md)
- [Quick Start Guide](docs/QUICK-START.md)

## Project Structure

```
neilerdeck/
├── hardware/          # Hardware specs and component lists
│   ├── SPECS.md
│   └── COMPONENTS.md
├── software/          # OS configs and software setup
│   ├── OS-SETUP.md
│   └── install.sh
├── 3d-models/         # Case designs and STL files
│   └── README.md
├── ai-agents/         # Helper scripts and automation
│   ├── component-researcher.py
│   ├── config-generator.py
│   └── doc-writer.py
├── docs/              # Documentation and guides
│   └── QUICK-START.md
├── build-log/         # Build progress and notes
└── README.md          # This file
```

## Build Overview

### 1. Order Components
Total cost: ~$670 (see [COMPONENTS.md](hardware/COMPONENTS.md))

### 2. 3D Print Enclosure
Print time: ~24 hours (see [3d-models/](3d-models/))

### 3. Assemble Hardware
Assembly time: 2-4 hours

### 4. Install Software
```bash
chmod +x software/install.sh
sudo ./software/install.sh
```

### 5. Configure and Customize
Follow [QUICK-START.md](docs/QUICK-START.md)

## AI Agents

This project includes helper AI agents to assist with the build:

### Component Researcher
```bash
python3 ai-agents/component-researcher.py
```
Finds and compares components, checks availability, suggests alternatives

### Config Generator
```bash
python3 ai-agents/config-generator.py
```
Auto-generates system configs based on your hardware choices

### Doc Writer
```bash
python3 ai-agents/doc-writer.py
```
Maintains documentation and generates guides

## Capabilities

- **Development**: Code on the go with full dev environment
- **Security Testing**: WiFi auditing, network pentesting, SDR hacking
- **Remote Access**: 4G/LTE connectivity, VPN support
- **Hardware Hacking**: GPIO access, I2C/SPI, expansion modules
- **Radio**: SDR for signal analysis, LoRa for long-range comms
- **Offline Operation**: Long battery life, local storage

## Use Cases

- Penetration testing and security audits
- Field development and debugging
- IoT and hardware hacking
- Radio frequency analysis
- Emergency communications
- Off-grid computing
- Educational projects

## Technical Specs Summary

- **CPU**: Raspberry Pi 5 (Cortex-A76, 2.4GHz quad-core)
- **RAM**: 8GB LPDDR4
- **Storage**: 512GB NVMe SSD
- **Display**: 7-8" IPS touchscreen
- **Battery**: 10000mAh LiPo (8+ hours runtime)
- **Connectivity**: WiFi, Bluetooth, 4G/LTE, Ethernet
- **Expansion**: USB 3.0, GPIO, SDR, GPS
- **Weight**: <2kg
- **Dimensions**: 300x200x80mm

## Getting Started

1. **Read the specs**: Start with [SPECS.md](hardware/SPECS.md)
2. **Order parts**: Use [COMPONENTS.md](hardware/COMPONENTS.md)
3. **Print case**: Check [3d-models/](3d-models/)
4. **Build it**: Follow assembly guide
5. **Install OS**: Run [install.sh](software/install.sh)
6. **Hack away**: See [QUICK-START.md](docs/QUICK-START.md)

## Contributing

This is a personal project, but feel free to:
- Fork and adapt for your own build
- Submit issues or suggestions
- Share your modifications
- Improve the AI agents

## License

MIT License - Feel free to use, modify, and distribute

## Credits

Designed and built by Neil - 2025

Inspired by the cyberdeck community at r/cyberDeck

## Safety Notice

- LiPo batteries can be dangerous if mishandled
- Use proper ESD protection
- Monitor temperature during operation
- Follow local laws regarding radio equipment and security testing
- Only test on networks you own or have permission to test

## Contact

- GitHub: (add your repo link)
- Twitter: (add your handle)
- Email: (add your email)

---

**Status**: Design complete, ready to build!

Happy hacking!
