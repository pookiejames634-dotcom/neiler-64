# Neiler-8 CPU Hardware Schematic

## Overview
Complete hardware design for building a physical 8-bit computer!

---

## Main Components

### 1. Central Processing Unit (CPU Core)
**IC: 74LS181 (4-bit ALU) x2** - for 8-bit operations
- Price: $2.50 each
- Function: Arithmetic and Logic operations
- Pins: 24-pin DIP

**IC: 74LS377 (Octal D Flip-Flop) x6** - for registers
- Price: $1.50 each
- Function: Store register values (A, B, C, D, X, Y)
- Pins: 20-pin DIP

### 2. Memory System
**SRAM: AS6C4008 (512KB)** - Main RAM
- Price: $8.00
- Capacity: 512KB (way more than 64KB needed!)
- Speed: 55ns
- Pins: 32-pin DIP

**EEPROM: AT28C256 (32KB)** - ROM for bootloader
- Price: $4.50
- Capacity: 32KB
- Pins: 28-pin DIP

### 3. Address & Data Bus
**IC: 74LS245 (Bus Transceiver) x3** - for data bus
- Price: $0.75 each
- Function: Bidirectional data transfer
- Pins: 20-pin DIP

**IC: 74LS373 (Latch) x2** - for address bus
- Price: $0.80 each
- Function: Hold address values
- Pins: 20-pin DIP

### 4. Clock & Timing
**Crystal Oscillator: 1 MHz**
- Price: $1.00
- Frequency: 1 MHz (adjustable up to 8 MHz!)
- Package: DIP-4

**IC: 74LS04 (Hex Inverter)** - clock conditioning
- Price: $0.50
- Pins: 14-pin DIP

### 5. Control Logic
**IC: 74LS138 (3-to-8 Decoder) x2** - instruction decoder
- Price: $0.60 each
- Function: Decode opcodes

**IC: 74LS32 (Quad OR Gate)**
- Price: $0.45

**IC: 74LS08 (Quad AND Gate)**
- Price: $0.45

---

## Pin Connections

### Data Bus (8-bit)
```
D0 ----[74LS245]---- RAM D0
D1 ----[74LS245]---- RAM D1
D2 ----[74LS245]---- RAM D2
D3 ----[74LS245]---- RAM D3
D4 ----[74LS245]---- RAM D4
D5 ----[74LS245]---- RAM D5
D6 ----[74LS245]---- RAM D6
D7 ----[74LS245]---- RAM D7
```

### Address Bus (16-bit)
```
A0-A15 ----[74LS373]---- RAM Address
```

### Control Signals
```
/RD  (Read)
/WR  (Write)
/CS  (Chip Select)
CLK  (Clock)
/RST (Reset)
```

---

## Power Supply Design

### Requirements
- **+5V @ 2A** - Main logic power
- **+12V @ 0.5A** - For optional peripherals
- **-12V @ 0.1A** - For RS-232 if needed

### Voltage Regulator
**IC: LM7805 (5V regulator)**
- Input: 7-12V DC
- Output: 5V @ 1.5A
- With heatsink!

**Decoupling Capacitors**
- 100nF ceramic x20 (one per IC)
- 10uF electrolytic x5 (power rails)

---

## I/O Ports

### Serial Port (UART)
**IC: 16550 UART**
- Price: $3.50
- Speed: Up to 115200 baud
- Connector: DB9 Female

### Parallel Port
**IC: 74LS374 (Octal Latch)**
- 8-bit parallel output
- Connector: 25-pin D-Sub

### GPIO Header
**40-pin header** - General purpose I/O
- Compatible with breadboard
- 5V logic levels

---

## Reset Circuit

```
        +5V
         |
        [10K]
         |
    ----+---- /RST (active low)
         |
    [Switch to GND]
         |
        GND
```

With 100nF capacitor for debouncing!

---

## LED Indicators

- **Power LED** - Green (system on)
- **HLT LED** - Red (CPU halted)
- **Activity LED** - Yellow (data bus activity)
- **Clock LED** - Blue (clock signal - slowed down!)

---

## PCB Layout Specifications

### Board Dimensions
- **Size**: 10cm x 15cm (Eurocard size)
- **Layers**: 2-layer PCB
- **Thickness**: 1.6mm

### Trace Specifications
- **Power traces**: 0.5mm width minimum
- **Signal traces**: 0.25mm width
- **Clearance**: 0.25mm minimum

### Components Placement
```
Top View:
+----------------------------------+
|  [CPU Area]     [RAM]     [ROM]  |
|                                  |
|  [Registers]                     |
|                                  |
|  [Clock]    [I/O Ports]          |
|                                  |
|  [Power]    [Headers]            |
+----------------------------------+
```

---

## Bill of Materials (BOM)

| Component | Quantity | Price Each | Total |
|-----------|----------|------------|-------|
| 74LS181 ALU | 2 | $2.50 | $5.00 |
| 74LS377 Register | 6 | $1.50 | $9.00 |
| AS6C4008 RAM | 1 | $8.00 | $8.00 |
| AT28C256 ROM | 1 | $4.50 | $4.50 |
| 74LS245 Bus | 3 | $0.75 | $2.25 |
| 74LS373 Latch | 2 | $0.80 | $1.60 |
| Crystal 1MHz | 1 | $1.00 | $1.00 |
| 74LS138 Decoder | 2 | $0.60 | $1.20 |
| 74LS32 OR | 1 | $0.45 | $0.45 |
| 74LS08 AND | 1 | $0.45 | $0.45 |
| LM7805 Regulator | 1 | $1.50 | $1.50 |
| Capacitors | 25 | $0.10 | $2.50 |
| LEDs | 4 | $0.20 | $0.80 |
| PCB | 1 | $15.00 | $15.00 |
| Connectors | - | - | $5.00 |
| Misc (wire, switches) | - | - | $3.00 |
| **TOTAL** | | | **$61.25** |

---

## Assembly Instructions

### Step 1: Install Power Components
1. Solder LM7805 regulator with heatsink
2. Add power capacitors
3. Test voltage outputs!

### Step 2: Install ICs (smallest to largest)
1. IC sockets first (ALWAYS use sockets!)
2. 74LS series chips
3. Memory chips last

### Step 3: Connect Buses
1. Data bus connections
2. Address bus connections
3. Control signals

### Step 4: Add Peripherals
1. Clock circuit
2. Reset button
3. LEDs
4. I/O connectors

### Step 5: Testing
1. Power on test (check voltage!)
2. Clock signal test (use oscilloscope)
3. Load test program to ROM
4. Run first program!

---

## Testing & Debugging

### Required Tools
- **Multimeter** - voltage testing ($20)
- **Logic Probe** - signal testing ($15)
- **Oscilloscope** (optional but helpful!) ($100-300)

### Common Issues
1. **No power** - Check regulator and capacitors
2. **No clock** - Check crystal oscillator
3. **Random behavior** - Check decoupling caps
4. **Memory errors** - Check address/data bus connections

---

## Expansion Options

### Future Upgrades
- **Sound chip** (AY-3-8910) - $5
- **Video output** (TMS9918) - $8
- **SD card reader** - $3
- **Keyboard interface** (PS/2) - $2
- **Real-time clock** (DS1307) - $2

### Expansion Slots
- **2x 40-pin headers** for expansion cards
- Compatible with custom GPU board!

---

## Safety Notes

⚠️ **Important Safety Tips!**
- Always unplug before touching components
- Use ESD protection (anti-static wrist strap)
- Double-check polarity on capacitors
- Don't touch components while powered
- Adult supervision recommended for soldering!

---

## Where to Buy Components

### Online Stores
- **Mouser Electronics** - mouser.com
- **Digi-Key** - digikey.com
- **Jameco** - jameco.com
- **eBay** - Used/surplus components (cheaper!)

### Local Options
- Electronics hobby stores
- University surplus sales
- Maker spaces

---

## Software to Design PCBs

### Free Tools
- **KiCad** - Professional, open source
- **EasyEDA** - Browser-based, simple
- **Fritzing** - Great for beginners!

### PCB Manufacturing
- **JLCPCB** - $2 for 5 PCBs!
- **PCBWay** - Good quality
- **OSH Park** - USA-based

---

## Success Stories

Build your own computer and:
- ✅ Learn how CPUs really work
- ✅ Program in pure assembly
- ✅ Show off at science fair!
- ✅ Put it in your college application
- ✅ Start a YouTube channel about it
- ✅ Sell kits to other makers

---

**This is a REAL, buildable computer!**

Total cost: **~$60**

Build time: **2-3 weekends**

Difficulty: **Intermediate** (with adult help!)

---

*Design by pookiejames634-dotcom, 2025*
