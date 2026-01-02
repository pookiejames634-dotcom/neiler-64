# Getting Started with Neiler-64

Welcome to the Neiler-64 project! This guide will help you get up and running with the complete Neiler-64 ecosystem.

## Project Overview

Neiler-64 is a complete computing platform including:
- **Custom CPU/GPU Architecture** - Neiler-8 (8-bit) and Neiler-16 (16-bit) processors
- **Hardware Designs** - Complete PCB schematics, 3D models, and manufacturing files
- **Neiler-OS** - Developer-focused operating system
- **Development Tools** - Assembler, emulator, debugger
- **Physical Hardware** - Neilerdeck portable cyberdeck

## Quick Start: Neiler-OS Server

The fastest way to experience Neiler-64 is to run the Neiler-OS server:

### 1. Start the Server

```bash
cd server
chmod +x START_SERVER.sh
./START_SERVER.sh
```

This will:
- Build the Neiler-OS Docker image
- Start the server with all services
- Expose SSH on port 2222
- Start workload simulators

### 2. Connect via SSH

```bash
ssh dev@localhost -p 2222
# Password: neiler64
```

### 3. Try Some Commands

Once logged in:

```bash
# Get help
neiler-help

# Assemble a program
echo "MOV A, 42" > test.asm
echo "HLT" >> test.asm
nasm test.asm -o test.nbin

# Run in emulator
neiler-emu test.nbin

# Check system status
neiler-status

# Run benchmarks
neiler-benchmark
```

## Hardware Design Files

### View 3D Models

The hardware/3d-models/openscad/ directory contains parametric 3D models:

```bash
cd computer/hardware/3d-models/openscad

# View CPU chip (requires OpenSCAD)
openscad neiler_cpu_chip.scad

# View GPU chip
openscad neiler_gpu_chip.scad

# View RAM module
openscad neiler_ram_module.scad

# View complete motherboard
openscad neiler_motherboard.scad

# View power supply
openscad neiler_psu.scad
```

### Export STL for 3D Printing

```bash
# Export CPU chip to STL
openscad -o neiler_cpu.stl neiler_cpu_chip.scad

# Export complete assembly
openscad -o motherboard.stl neiler_motherboard.scad
```

### PCB Design

KiCad project files are in `computer/hardware/kicad/`:

```bash
cd computer/hardware/kicad

# Open in KiCad (if installed)
kicad neiler8_cpu.kicad_pro
```

Footprints for custom components are in `computer/hardware/footprints/`:
- `Neiler_CPU_PLCC64.kicad_mod` - CPU footprint
- `Neiler_GPU_TQFP128.kicad_mod` - GPU footprint (to be created)
- `Neiler_RAM_DIMM.kicad_mod` - RAM module footprint (to be created)

## Development

### Assemble Programs

```bash
cd computer

# Assemble example
python3 assembler/asm.py examples/hello.asm -o hello.bin

# Run in emulator
python3 cpu/neiler8.py  # Interactive mode
```

### Run CPU Simulation

```python
from cpu.neiler8 import Neiler8CPU

cpu = Neiler8CPU()
program = [
    0x01, 0x0A,  # MOV A, 10
    0x41, 0x05,  # ADD A, 5
    0xFF         # HLT
]

cpu.load_program(program)
cpu.run()
print(f"Result: A = {cpu.A}")  # Should be 15
```

### GPU Programming

```python
from gpu.neilergpu import NeilerGPU

gpu = NeilerGPU()
gpu.set_mode(640, 480)

# Draw a pixel
gpu.set_pixel(320, 240, (255, 0, 0))  # Red pixel at center

# Draw a sprite
gpu.load_sprite(0, sprite_data)
gpu.draw_sprite(0, 100, 100)

gpu.render()
```

## Hardware Build Guide

### For Neiler-8 CPU Board

1. **Order PCB**
   - Use Gerber files in `computer/hardware/gerbers/`
   - Recommended: JLCPCB, PCBWay, or OSH Park
   - Specifications: 2-layer, 1.6mm thickness

2. **Order Components**
   - See BOM in `computer/hardware/bom/neiler8_bom.csv`
   - Sources: Mouser, Digi-Key, LCSC
   - Estimated cost: ~$60

3. **Assembly**
   - Follow guide in `computer/hardware/ASSEMBLY.md`
   - Use IC sockets (don't solder ICs directly!)
   - Test power supply first

4. **Programming**
   - Burn bootloader to EEPROM
   - Connect via UART for programming
   - Use provided programmer software

### For Neilerdeck

1. **3D Print Case**
   - Files in `deck/3d-models/`
   - Material: PETG or ABS
   - Print time: ~20 hours

2. **Order Electronics**
   - See `deck/hardware/COMPONENTS.md`
   - Raspberry Pi 5 recommended
   - Total cost: ~$670

3. **Assemble**
   - Follow `deck/docs/QUICK-START.md`
   - Install Neiler-OS on Pi
   - Configure networking

## Server Management

### Docker Commands

```bash
# View logs
docker-compose logs -f neiler-os

# Stop server
docker-compose down

# Restart services
docker-compose restart

# Shell access (bypass SSH)
docker exec -it neiler-os-server /usr/bin/nsh

# View workload statistics
docker exec -it neiler-os-server cat /var/log/neiler/benchmark_results.json
```

### Service Management

Inside the server:

```bash
# Check service status
sudo neiler-service status

# Restart a service
sudo neiler-service restart workload-sim

# View service logs
tail -f /var/log/neiler/workload-sim.log
```

## Web Interfaces

Once the server is running:

- **Web Dashboard**: http://localhost:8080
  - System monitoring
  - CPU/GPU status
  - Performance metrics

- **Workload Monitor**: http://localhost:8081
  - Live workload visualization
  - Benchmark results
  - Resource usage

- **System Monitor API**: http://localhost:8082/api/stats
  - JSON API for system statistics
  - Real-time metrics

## Architecture Documentation

### CPU Architecture

- **Neiler-8**: 8-bit data, 16-bit address, 64KB RAM
  - 6 registers (A, B, C, D, X, Y)
  - 40+ instructions
  - 8MHz clock (adjustable)
  - Details: `computer/docs/NEILER8_ISA.md`

- **Neiler-16**: 16-bit data, 24-bit address, 16MB RAM
  - 8 registers
  - 80+ instructions
  - Hardware floating-point
  - Details: `computer/docs/NEILER16_ISA.md`

### GPU Architecture

- **NeilerGPU**: Custom graphics processor
  - 640x480 @ 60Hz (or 320x200 mode)
  - 65K colors (16-bit) or 256 colors (8-bit)
  - 64 hardware sprites
  - 2 tile layers
  - Details: `computer/docs/GPU_PROGRAMMING.md`

## Manufacturing Files

### PCB Fabrication

Gerber files ready for manufacturing in `computer/hardware/gerbers/`:
- `neiler8_cpu-F_Cu.gbr` - Top copper
- `neiler8_cpu-B_Cu.gbr` - Bottom copper
- `neiler8_cpu-F_Mask.gbr` - Top soldermask
- `neiler8_cpu-B_Mask.gbr` - Bottom soldermask
- `neiler8_cpu-Edge_Cuts.gbr` - Board outline
- `neiler8_cpu.drl` - Drill file

### Assembly Files

For PCBA services:
- `neiler8_cpu_bom.csv` - Bill of Materials
- `neiler8_cpu_cpl.csv` - Component Placement List (pick-and-place)

### 3D Files

For mechanical design:
- STEP files in `computer/hardware/3d-models/step/`
- STL files in `computer/hardware/3d-models/stl/`

## Troubleshooting

### Server Won't Start

```bash
# Check Docker status
docker ps -a

# View error logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### SSH Connection Refused

```bash
# Check if SSH service is running
docker exec neiler-os-server pgrep sshd

# Restart SSH manually
docker exec neiler-os-server /usr/sbin/sshd

# Check port forwarding
netstat -an | grep 2222
```

### Workload Simulator Not Running

```bash
# Check logs
docker exec neiler-os-server tail -f /var/log/neiler/workload-sim.log

# Restart simulator
docker exec neiler-os-server pkill -f simulator.py
docker exec neiler-os-server python3 /opt/neiler/workload-sim/simulator.py &
```

## Performance Tuning

### Adjust CPU Speed

Edit `docker-compose.yml`:

```yaml
environment:
  - NEILER_CPU_SPEED=16000000  # 16MHz (2x faster)
```

### Increase Memory

```yaml
environment:
  - NEILER_RAM_SIZE=134217728  # 128MB
```

### Enable Debug Mode

```yaml
environment:
  - NEILER_DEBUG=1  # Verbose logging
```

## Community & Support

- **Documentation**: Full docs in each subdirectory
- **Issues**: Report bugs via GitHub issues
- **Discord**: Join the Neiler-64 community server
- **Forum**: https://forum.neiler-os.dev

## Next Steps

1. **Explore Examples**: Check `computer/examples/` for sample programs
2. **Write Code**: Try writing your own Neiler assembly programs
3. **Run Benchmarks**: Test system performance
4. **Build Hardware**: Order PCBs and build a physical system
5. **Contribute**: Improve docs, add features, share your builds

## License

Neiler-64 is open source under the MIT License. Build, modify, and share freely!

---

**Happy Hacking!**

Built with ❤️ by the Neiler Project Team - 2025
