# Neiler-64 Graphical Emulator

A complete graphical emulator for the Neiler-64 system with visual display, CPU state monitoring, and memory viewer.

## Features

- **Visual Display**: 320x200 pixel Neiler screen with 2x scaling
- **CPU State**: Real-time register and flag display
- **Memory Viewer**: Scrollable hex dump of system memory
- **Interactive Controls**: Pause, step, reset, and speed control
- **Performance Monitoring**: Cycle count, FPS, and speed metrics

## Requirements

```bash
pip install pygame
```

## Quick Start

```bash
# Run with demo program (colorful pixel pattern)
python3 neiler_emulator.py

# Run with custom program
python3 neiler_emulator.py myprogram.bin

# Run with custom speed
python3 neiler_emulator.py --speed 5000
```

## Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume execution |
| **S** | Toggle step mode |
| **N** | Execute next instruction (when paused) |
| **R** | Reset emulator and reload program |
| **+/-** | Increase/decrease CPU speed |
| **↑/↓** | Scroll memory viewer |
| **PgUp/PgDn** | Scroll memory faster |
| **ESC** | Quit emulator |

## Display Layout

```
┌──────────────────────────────────────────────────────────────┐
│  ┌─────────────────┐                                         │
│  │                 │  CPU STATE                              │
│  │  Neiler-64      │    A: 0x2A (42)                        │
│  │  Display        │    B: 0x00 (0)                         │
│  │  320x200        │    C: 0x01 (1)                         │
│  │                 │    ...                                  │
│  │                 │    PC: 0x0206                          │
│  │                 │    Flags: Z:0 C:0 N:0 O:0              │
│  └─────────────────┘                                         │
│                       MEMORY VIEWER                          │
│                         0200: 01 00 02 00 03 01 91 80 ...   │
│                         0210: 44 44 61 40 72 02 06 01 ...   │
│                         ...                                  │
├──────────────────────────────────────────────────────────────┤
│ Status: RUNNING | Cycles: 1,234,567 | Speed: 1000 cyc/frame │
│ [SPACE] Pause | [S] Step | [N] Next | [R] Reset | [ESC] Quit│
└──────────────────────────────────────────────────────────────┘
```

## Writing Programs for the Emulator

### GPU Output

The emulator supports GPU pixel drawing via I/O ports:

- **Port 0x80**: X coordinate (0-319)
- **Port 0x81**: Y coordinate (0-199)
- **Port 0x82**: Draw pixel (color value)

### Example: Draw a Red Pixel

```asm
MOV A, 160      ; X = 160 (center)
OUT 0x80, A     ; Set X position
MOV A, 100      ; Y = 100 (center)
OUT 0x81, A     ; Set Y position
MOV A, 255      ; Color = 255 (reddish)
OUT 0x82, A     ; Draw pixel
HLT
```

### Example: Draw a Line

```asm
MOV A, 0        ; X = 0
MOV B, 100      ; Y = 100

LOOP:
    OUT 0x80, A  ; Set X
    MOV C, B
    OUT 0x81, C  ; Set Y
    MOV C, 255
    OUT 0x82, C  ; Draw pixel

    INC A        ; Next X
    CMP A, 320
    JNZ LOOP

    HLT
```

## Performance

- **Default Speed**: 1,000 cycles/frame @ 60 FPS = ~60,000 instructions/second
- **Adjustable**: 1 - 10,000 cycles/frame
- **Typical Programs**: 1,000 - 5,000 cycles/frame works well
- **Demos**: 5,000+ cycles/frame for smooth graphics

## Demo Program

The default demo program draws a colorful pattern across the screen:
- Scans every pixel from left to right, top to bottom
- Uses incrementing color values
- Loops continuously when finished

## Troubleshooting

### "Could not import Neiler CPU/GPU modules"
Make sure `neiler8.py` exists in `../cpu/` directory.

### Black screen
- Program may not be writing to GPU ports
- Try pressing **R** to reset
- Check that program uses ports 0x80-0x82

### Slow performance
- Decrease speed with **-** key
- Target 30-60 FPS for smooth operation

### Memory viewer shows zeros
- Program hasn't modified that memory region yet
- Scroll with **↑/↓** to see program code around 0x0200

## Advanced Usage

### Load Custom Programs

```bash
# Assemble your program first
cd ../assembler
python3 asm.py myprogram.asm -o myprogram.bin

# Run in emulator
cd ../emulator
python3 neiler_emulator.py ../assembler/myprogram.bin
```

### Debugging

1. Run emulator with your program
2. Press **SPACE** to pause
3. Press **S** to enable step mode
4. Press **N** to step through instructions
5. Watch registers and memory change in real-time

## Examples

See `../examples/` for sample programs:
- `hello.asm` - Text output demo
- `fibonacci.asm` - Fibonacci calculator
- `graphics_demo.asm` - Pixel drawing patterns

## Technical Details

- **Resolution**: 320x200 @ 60 Hz
- **Display Scale**: 2x (640x400 on screen)
- **CPU**: Neiler-8 (8-bit)
- **Memory**: 64KB addressable
- **Registers**: A, B, C, D, X, Y, PC, SP
- **Instruction Set**: 40+ opcodes

## License

MIT License - Part of the Neiler-64 project
