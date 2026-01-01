# Neilerdeck Build Log - Day 1

**Date**: 2025-12-09
**Status**: Planning & Design Phase

## Accomplishments Today

### Project Setup
- Created project structure
- Defined hardware specifications
- Compiled component shopping list
- Designed software stack
- Created AI helper agents

### Design Decisions

#### Hardware Platform
- Chose Raspberry Pi 5 (8GB) for main compute
- Selected 7.9" display for good balance of size/resolution
- Decided on 3S LiPo 10000mAh for 8+ hour battery life
- Alfa WiFi adapter for pentesting capabilities

#### Software Approach
- Kali Linux ARM64 as base OS
- Automated setup script for quick deployment
- Modular configuration system

#### AI Agents Created
1. **component-researcher.py**: Helps find best prices and alternatives
2. **config-generator.py**: Auto-generates system configs
3. **doc-writer.py**: Maintains documentation

### Next Steps

#### Immediate (This Week)
- [ ] Finalize 3D case design in FreeCAD
- [ ] Order components from list
- [ ] Set up development environment for testing configs
- [ ] Start printing case parts

#### Short Term (Next 2 Weeks)
- [ ] Receive and inventory components
- [ ] Test fit components in 3D printed case
- [ ] Begin assembly
- [ ] Test power system thoroughly

#### Medium Term (Next Month)
- [ ] Complete hardware assembly
- [ ] Install and configure OS
- [ ] Run automated setup script
- [ ] Test all subsystems (WiFi, SDR, GPS, etc.)
- [ ] Create detailed photo build guide

### Questions to Resolve
- Mechanical keyboard: Build custom or buy compact?
- Battery placement: Top or bottom of case?
- Cooling: Passive or active (fans)?
  - **Decision**: Active cooling for sustained performance
- Display: 7" or 8"?
  - **Leaning towards**: 7.9" Waveshare

### Budget Status
- Estimated total: $670
- Allocated: $0
- Remaining to purchase: $670

### Notes
- Keep weight under 2kg for portability
- Ensure all ports accessible without disassembly
- Design for easy battery replacement
- Consider adding hardware kill switches for privacy

### Ideas for Future Iterations
- Add e-ink display for low-power status screen
- Integrate thermal camera module
- Add hardware keylogger detection
- Built-in Proxmark3 for RFID work
- Flipper Zero integration

### Resources Used
- r/cyberDeck community examples
- Pi 5 official documentation
- Kali Linux ARM documentation
- Various component datasheets

## Tomorrow's Goals
1. Create detailed 3D case design
2. Generate BOM with supplier links
3. Test AI agents functionality
4. Start component ordering

## Photos
(Will add photos as build progresses)

---

**Total Time Today**: 3 hours planning
**Mood**: Excited to start building!
