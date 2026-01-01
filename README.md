# Neiler 64 - Custom Workstation Platform

> A complete hardware/software platform featuring custom CPU/GPU architecture and a portable cyberdeck workstation

---

## Overview

The Neiler 64 project encompasses a fully custom computing platform designed from the ground up:

- **Custom CPU Architecture**: Neiler-8 (8-bit) and Neiler-16 (16-bit) processors with complete instruction sets
- **Custom GPU**: NeilerGPU with hardware sprites, tile-based graphics, and multiple display modes
- **Physical Hardware**: PCB designs, schematics, and bill of materials for building real hardware
- **Portable Workstation**: Neilerdeck cyberdeck for field operations, security research, and development

---

## Project Structure

```
neiler-64/
├── computer/           # Custom CPU/GPU computer system
│   ├── cpu/           # CPU implementations (Neiler-8, Neiler-16)
│   ├── gpu/           # GPU implementation and graphics engine
│   ├── assembler/     # Assembly language tools
│   ├── emulator/      # System emulator
│   ├── examples/      # Example programs
│   ├── hardware/      # PCB designs, schematics, BOM
│   └── docs/          # Architecture documentation
│
├── deck/              # Neilerdeck portable workstation
│   ├── hardware/      # Hardware specs and component lists
│   ├── software/      # OS setup and configurations
│   ├── 3d-models/     # Case designs and 3D printable parts
│   ├── ai-agents/     # Helper automation scripts
│   └── build-log/     # Build progress and notes
│
└── shared/            # Shared resources and tools
    ├── docs/          # Cross-project documentation
    └── tools/         # Utilities and scripts
```

---

## Quick Start

### Neiler Computer

Explore the custom CPU/GPU architecture:

```bash
cd computer

# Assemble example program
python assembler/asm.py examples/hello.asm -o hello.bin

# Run in emulator
python emulator/emulator.py hello.bin
```

See [computer/README.md](computer/README.md) for full details.

### Neilerdeck

Build the portable cyberdeck workstation:

1. Review [deck/hardware/SPECS.md](deck/hardware/SPECS.md)
2. Order components from [deck/hardware/COMPONENTS.md](deck/hardware/COMPONENTS.md)
3. 3D print case from [deck/3d-models/](deck/3d-models/)
4. Follow build guide in [deck/docs/QUICK-START.md](deck/docs/QUICK-START.md)

See [deck/README.md](deck/README.md) for full details.

---

## Features

### Neiler Computer System

**CPU (Neiler-8)**
- 8-bit data bus, 16-bit address bus
- 64KB addressable memory
- 6 general-purpose registers
- 40+ instructions
- Hardware interrupts

**CPU (Neiler-16)**
- 16-bit data bus, 24-bit address bus
- 16MB addressable memory
- 8 general-purpose registers
- Floating-point support
- Memory Management Unit (MMU)
- 80+ instructions

**GPU (NeilerGPU)**
- 320x200 or 640x480 resolution
- 256-color palette (8-bit) or 65K colors (16-bit)
- 64 hardware sprites (16x16 pixels)
- Tile-based backgrounds
- Hardware scrolling
- VBlank interrupts

**Hardware**
- Complete PCB schematics
- Bill of materials (~$60 build cost)
- Assembly instructions
- Expansion slot support

### Neilerdeck Portable Workstation

**Computing**
- Raspberry Pi 5 (8GB RAM)
- 512GB NVMe SSD
- 7-8" touchscreen display

**Connectivity**
- WiFi pentesting adapter
- 4G/LTE cellular
- SDR (Software Defined Radio)
- GPS module

**Power**
- 10000mAh battery
- 8+ hours runtime
- USB-C PD charging

**Capabilities**
- Security testing and pentesting
- Field development
- Hardware hacking
- Radio frequency analysis
- Off-grid computing

---

## Build Costs

- **Neiler Computer**: ~$60 for PCBs and components
- **Neilerdeck**: ~$670 for complete build

---

## Technical Highlights

### Custom Silicon Design
- Complete instruction set architecture (ISA)
- Custom assembly language
- Hardware schematics using 74-series logic ICs
- Buildable on breadboard or custom PCB

### Software Stack
- Custom assembler and disassembler
- Full system emulator with debugger
- Example programs (games, fractals, demos)
- Python implementation for prototyping

### Hardware Design
- KiCad PCB designs
- 3D printable enclosures (OpenSCAD, Blender)
- Laser cutting templates (Inkscape)
- Component sourcing guide

---

## Use Cases

- **Education**: Learn computer architecture from the ground up
- **Retro Computing**: Build and program custom 8/16-bit systems
- **Security Research**: Portable pentesting platform
- **Hardware Hacking**: GPIO access, expansion modules
- **Game Development**: Retro game programming
- **Field Work**: Portable development and debugging

---

## Documentation

- [Computer Architecture Docs](computer/docs/)
- [Hardware Specifications](computer/hardware/schematics/)
- [Deck Build Guide](deck/docs/QUICK-START.md)
- [Component Lists](deck/hardware/COMPONENTS.md)

---

## Contributing

This is a personal project, but contributions are welcome:
- Fork and adapt for your own builds
- Submit issues and suggestions
- Share your modifications
- Improve documentation

---

## Future Plans

- [ ] Neiler-32 (32-bit CPU architecture)
- [ ] Sound processor chip
- [ ] FPGA implementation
- [ ] Physical hardware production run
- [ ] Networking support
- [ ] Operating system development

---

## License

MIT License - Build whatever you want!

---

## Credits

Designed and built by Neil (pookiejames634-dotcom) - 2025

Inspired by:
- Ben Eater's 8-bit computer
- The cyberdeck community at r/cyberDeck
- Classic 8-bit and 16-bit computer architectures

---

## Safety & Legal

- Use proper ESD protection when building
- LiPo batteries require careful handling
- Only perform security testing on authorized systems
- Follow local laws regarding radio equipment
- Adult supervision recommended for hardware assembly

---

**Status**: Active development - Ready to build!

Happy hacking!
