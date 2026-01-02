# Neiler-OS

> A developer-focused operating system built for the Neiler-64 platform

## Overview

Neiler-OS is a custom Linux-based operating system optimized for developers working with the Neiler-64 hardware platform. It includes native support for Neiler CPU/GPU emulation, a complete development toolchain, and advanced system monitoring.

## Features

### Core System
- **Custom Linux Kernel** - Optimized for Neiler-64 architecture
- **Neiler Init** - Fast, dependency-based init system
- **NPM (Neiler Package Manager)** - Efficient package management
- **Neiler Shell (nsh)** - Enhanced developer shell

### Development Tools
- **Neiler Assembler** - Full Neiler-8/16 assembly support
- **Neiler C Compiler** - C to Neiler bytecode compilation
- **Neiler Debugger (ndb)** - Interactive debugging
- **Neiler Emulator** - Full system emulation
- **GPU Dev Kit** - Graphics programming tools

### System Services
- **SSH Server** - Secure remote access
- **Workload Simulator** - Benchmark and stress testing
- **System Monitor** - Real-time performance metrics
- **Web Dashboard** - Browser-based management

### Developer Features
- **Git integration** - Pre-installed with custom aliases
- **Docker support** - Container development
- **VS Code Server** - Browser-based IDE
- **Neiler LSP** - Language server for Neiler assembly

## Architecture

```
Neiler-OS
├── Kernel Layer
│   ├── Linux 6.6.x (custom patches)
│   ├── Neiler CPU driver
│   ├── Neiler GPU driver
│   └── Custom syscalls
│
├── System Layer
│   ├── neiler-init (PID 1)
│   ├── Service manager
│   ├── Package manager (npm)
│   └── System utilities
│
├── Development Layer
│   ├── Neiler toolchain
│   ├── Emulator framework
│   ├── Debugging tools
│   └── Libraries and SDKs
│
└── Application Layer
    ├── Web dashboard
    ├── Workload simulator
    ├── System monitor
    └── Developer applications
```

## Quick Start

### Boot Neiler-OS Server
```bash
cd /home/neil/neiler-64/server
docker-compose up -d neiler-os
```

### SSH into System
```bash
ssh dev@neiler-os.local
# Password: neiler64
```

### Run Neiler Programs
```bash
# Assemble Neiler-8 program
nasm my_program.asm -o program.nbin

# Run in emulator
neiler-emu program.nbin

# Debug interactively
ndb program.nbin
```

### Package Management
```bash
# Update package list
sudo npm update

# Install package
sudo npm install neiler-games

# Search packages
npm search gpu
```

## System Requirements

### Hardware (Physical)
- Neiler-64 motherboard with CPU/GPU
- 256MB+ RAM
- 4GB+ storage
- Network adapter

### Hardware (Emulated)
- x86_64 host system
- 2GB+ RAM allocated
- 10GB+ storage
- Docker or QEMU

## Building from Source

```bash
# Clone repository
git clone https://github.com/neiler-64/neiler-os
cd neiler-os

# Build kernel
cd kernel
make neiler_defconfig
make -j$(nproc)

# Build userspace
cd ../userspace
./build.sh

# Create bootable image
cd ../image
./create-image.sh
```

## Development

### Creating Services
```ini
# /etc/neiler/services/myservice.service
[Service]
Name=myservice
Description=My Custom Service
ExecStart=/usr/bin/myservice
Restart=always
User=neiler
```

### Writing Drivers
```c
// Neiler kernel module
#include <linux/module.h>
#include <neiler/cpu.h>

static int __init neiler_custom_init(void) {
    printk(KERN_INFO "Neiler custom module loaded\n");
    return 0;
}

module_init(neiler_custom_init);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Neiler Project");
```

## Configuration

### System Config
- **Location**: `/etc/neiler/neiler.conf`
- **CPU Settings**: `/etc/neiler/cpu.conf`
- **GPU Settings**: `/etc/neiler/gpu.conf`
- **Network**: `/etc/neiler/network.conf`

### User Config
- **Shell**: `~/.nshrc`
- **Emulator**: `~/.neiler/emu.conf`
- **Debugger**: `~/.neiler/ndb.conf`

## Networking

Neiler-OS includes advanced networking:
- **neiler-os.local** - mDNS hostname
- **Static IP**: Configurable via /etc/neiler/network.conf
- **Firewall**: Built-in iptables configuration
- **VPN**: WireGuard support

## Security

- **SELinux** - Enforcing mode (configurable)
- **SSH Keys** - RSA/ED25519 support
- **User Isolation** - Proper permission management
- **Secure Boot** - Optional UEFI secure boot

## Performance

### Benchmarks
- **Boot Time**: < 5 seconds
- **Package Install**: < 2 seconds avg
- **CPU Emulation**: 10M+ instructions/sec
- **GPU Rendering**: 60 FPS @ 640x480

## Troubleshooting

### Boot Issues
```bash
# Check boot logs
neiler-boot-log

# Repair boot
sudo neiler-repair-boot
```

### Performance Issues
```bash
# Run system diagnostics
neiler-diag

# Monitor resources
neiler-top
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

Neiler-OS is open source under the MIT License.

## Links

- **Documentation**: https://docs.neiler-os.dev
- **Forum**: https://forum.neiler-os.dev
- **GitHub**: https://github.com/neiler-64/neiler-os
- **Discord**: https://discord.gg/neiler64

---

Built with ❤️ by the Neiler Project Team
