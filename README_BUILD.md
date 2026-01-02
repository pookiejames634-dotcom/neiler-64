# Neiler-64 Complete Build Guide

## Overview

This repository contains everything needed to build a complete Neiler-64 system, from hardware PCBs to a fully functional operating system with SSH access.

## What's Included

### 🔧 Hardware Design
- **3D Models** (OpenSCAD format)
  - Neiler-8 CPU chip (`computer/3d-models/openscad/neiler_cpu_chip.scad`)
  - NeilerGPU chip (`computer/3d-models/openscad/neiler_gpu_chip.scad`)
  - RAM modules (`computer/3d-models/openscad/neiler_ram_module.scad`)
  - PSU board (`computer/3d-models/openscad/neiler_psu_board.scad`)
  - Complete motherboard (`computer/3d-models/openscad/neiler_motherboard.scad`)

- **KiCad PCB Files**
  - CPU footprint (`computer/hardware/kicad/footprints/Neiler_CPU_PLCC68.kicad_mod`)
  - GPU footprint (`computer/hardware/kicad/footprints/Neiler_GPU_TQFP100.kicad_mod`)
  - Complete schematics and layouts in `computer/hardware/kicad/`

- **Bill of Materials**
  - Complete BOM with DigiKey part numbers
  - CPU BOM: `computer/hardware/bom/NEILER8_BOM_DIGIKEY.csv`
  - GPU BOM: `computer/hardware/bom/NEILER_GPU_BOM_DIGIKEY.csv`
  - **Total Cost: ~$110 (CPU) + $200 (GPU) = $310**

### 💻 Neiler-OS Operating System
- **Kernel** (`neiler-os/kernel/neiler_kernel.c`)
  - Preemptive multitasking
  - Virtual memory management
  - Device drivers
  - Network stack

- **Bootloader** (`neiler-os/bootloader/neiler_boot.asm`)
  - BIOS boot support
  - Protected mode transition
  - Kernel loading

- **Package Manager** (`neiler-os/packages/npkg`)
  - Install/remove packages
  - Dependency resolution
  - Package search

- **System Tools**
  - System monitor (`neiler-os/bin/sysmon.py`)
  - Workload simulator (`neiler-os/bin/workload-sim.py`)

### 🌐 Neiler-64 Server
- **Docker Container** (`server/docker/Dockerfile`)
  - Complete development environment
  - SSH server pre-configured
  - All development tools included

- **Easy Deployment** (`server/docker/docker-compose.yml`)
  - One-command startup
  - Network services
  - Monitoring dashboards

## Quick Start

### 1. Hardware Build

#### View 3D Models
```bash
# Install OpenSCAD
sudo apt install openscad  # Linux
brew install openscad      # macOS

# View CPU model
openscad computer/3d-models/openscad/neiler_cpu_chip.scad

# View complete motherboard
openscad computer/3d-models/openscad/neiler_motherboard.scad
```

#### Order PCBs
1. Open KiCad project: `computer/hardware/kicad/neiler8_cpu.kicad_pro`
2. Generate Gerber files
3. Upload to PCB manufacturer (JLCPCB, PCBWay, OSH Park)
4. Order components from DigiKey using BOMs in `computer/hardware/bom/`

### 2. Software/Server Setup

#### Start Neiler-64 Server
```bash
cd server/docker
./start-server.sh
```

This will:
- Build Docker container with Neiler-OS
- Start SSH server on port 2222
- Launch monitoring services
- Start workload simulators

#### Connect to Server
```bash
# From local machine
ssh neiler@localhost -p 2222
# Password: neiler123

# From network
ssh neiler@<your-ip> -p 2222
```

#### Use Package Manager
```bash
# Update package lists
npkg update

# Search for packages
npkg search python

# Install package
npkg install gcc-neiler

# List installed packages
npkg list
```

#### Run Workload Simulator
```bash
# Inside the server
/opt/neiler-os/bin/workload-sim.py
```

This simulates:
- Neiler-8 CPU executing instructions
- NeilerGPU rendering frames at 60 FPS
- Real-time performance statistics

#### Monitor System
```bash
# One-time stats
/opt/neiler-os/bin/sysmon.py --once

# Continuous monitoring
/opt/neiler-os/bin/sysmon.py
```

### 3. Development

#### Run Neiler-8 CPU Emulator
```bash
cd computer/cpu
python3 neiler8.py
```

#### Assemble and Run Programs
```bash
cd computer/assembler
python3 asm.py ../examples/hello.asm -o hello.bin
python3 ../cpu/neiler8.py hello.bin
```

## Project Structure

```
neiler-64/
├── computer/              # CPU/GPU computer system
│   ├── cpu/              # CPU implementations
│   ├── gpu/              # GPU implementation
│   ├── assembler/        # Assembly tools
│   ├── 3d-models/        # 3D models (OpenSCAD)
│   ├── hardware/         # PCB designs, BOMs
│   │   ├── kicad/       # KiCad project files
│   │   ├── bom/         # Bills of Materials
│   │   └── gerbers/     # Manufacturing files
│   └── examples/         # Example programs
│
├── neiler-os/            # Operating system
│   ├── kernel/          # OS kernel
│   ├── bootloader/      # Boot code
│   ├── packages/        # Package manager
│   └── bin/             # System utilities
│
├── server/               # Server infrastructure
│   └── docker/          # Docker container
│
└── deck/                 # Portable cyberdeck
    ├── hardware/        # Deck hardware specs
    ├── software/        # Deck software
    └── 3d-models/       # Case designs
```

## Hardware Specifications

### Neiler-8 CPU
- **Architecture**: 8-bit data bus, 16-bit address bus
- **Memory**: 64KB addressable
- **Registers**: 6 general-purpose (A, B, C, D, X, Y)
- **Instructions**: 40+ opcodes
- **Speed**: 1-8 MHz (configurable)
- **Package**: 68-pin PLCC

### NeilerGPU
- **Resolution**: 320x200 or 640x480
- **Colors**: 256-color palette or 65K true color
- **Sprites**: 64 hardware sprites (16x16)
- **VRAM**: 1MB
- **Output**: VGA, Composite, S-Video
- **Package**: 100-pin TQFP

### Motherboard
- **Form Factor**: ATX (305mm x 244mm)
- **RAM Slots**: 4x DIMM (up to 32MB)
- **Expansion**: 4x custom slots
- **I/O**: Serial, Parallel, PS/2, VGA, Audio
- **Power**: ATX 24-pin + 8-pin

## Software Features

### Neiler-OS
- Modern Unix-like operating system
- Developer-focused design
- Package management (npkg)
- Network stack
- Virtual memory
- Preemptive multitasking

### Development Tools
- GCC cross-compiler
- Python 3.14
- Node.js 25
- Rust, Go compilers
- GDB debugger
- System profilers

## Server Ports

- **2222**: SSH
- **8080**: HTTP
- **8443**: HTTPS
- **3000**: Node.js dev server
- **3001**: Grafana monitoring
- **5000**: Flask applications
- **9090**: Prometheus metrics

## Docker Management

```bash
# View logs
docker-compose logs -f

# Stop server
docker-compose down

# Restart server
docker-compose restart

# Shell access
docker exec -it neiler-64 bash

# Rebuild
docker-compose build --no-cache
```

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Neiler-8 CPU PCB + Parts | $110 |
| NeilerGPU PCB + Parts | $200 |
| RAM Modules (4x 8MB) | $80 |
| Motherboard PCB + Parts | $150 |
| PSU Components | $50 |
| Enclosure/Case | $75 |
| **Total Hardware** | **$665** |
|  |  |
| Neiler-OS (Software) | Free |
| Development Tools | Free |
| Server Infrastructure | Free |

## Resources

- **Documentation**: `computer/docs/`
- **Examples**: `computer/examples/`
- **Datasheets**: `computer/hardware/datasheets/`
- **3D Models**: `computer/3d-models/`

## Support

- File issues on GitHub
- Check documentation in `/docs`
- Join community discussions

## License

MIT License - Build whatever you want!

## Credits

Designed by Neil (pookiejames634-dotcom) - 2025

Inspired by:
- Ben Eater's 8-bit computer
- Classic 8-bit/16-bit architectures
- The cyberdeck community

---

**Ready to build your own computer from scratch!**

*Last updated: 2026-01-02*
