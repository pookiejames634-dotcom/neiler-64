# 🖥️ NeilerComputer - Custom CPU & GPU Architecture

> A fully functional 8-bit and 16-bit computer system with custom CPU, GPU, assembler, and emulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Features

### Neiler-8 (8-bit CPU)
- **8-bit data bus**
- **16-bit address bus** (64KB memory)
- **6 general-purpose registers** (A, B, C, D, X, Y)
- **Stack pointer** and **Program counter**
- **ALU operations**: ADD, SUB, AND, OR, XOR, SHL, SHR
- **40+ instructions**
- **Interrupt support**

### Neiler-16 (16-bit CPU)
- **16-bit data bus**
- **24-bit address bus** (16MB memory)
- **8 general-purpose 16-bit registers**
- **Floating-point support**
- **MMU (Memory Management Unit)**
- **80+ instructions**
- **Hardware multiply/divide**

### NeilerGPU
- **320x200 resolution** (8-bit mode) or **640x480** (16-bit mode)
- **256-color palette** (8-bit) or **65K colors** (16-bit)
- **Hardware sprites** (64 sprites)
- **Tile-based backgrounds**
- **Hardware scrolling**
- **Vertical blank interrupt**

---

## 📦 What's Included

```
NeilerComputer/
├── cpu/
│   ├── neiler8.py          # 8-bit CPU implementation
│   ├── neiler16.py         # 16-bit CPU implementation
│   └── specs/              # Architecture specifications
├── gpu/
│   ├── neilergpu.py        # GPU implementation
│   └── sprites.py          # Sprite engine
├── emulator/
│   ├── emulator.py         # Full system emulator
│   ├── debugger.py         # Built-in debugger
│   └── gui.py              # Pygame-based GUI
├── assembler/
│   ├── asm.py              # Assembler (assembly → machine code)
│   └── disasm.py           # Disassembler
├── examples/
│   ├── hello.asm           # Hello World
│   ├── snake.asm           # Snake game
│   ├── mandelbrot.asm      # Mandelbrot fractal
│   └── raycaster.asm       # 3D raycaster
└── docs/
    ├── ISA.md              # Instruction Set Architecture
    ├── PROGRAMMING.md      # Programming guide
    └── HARDWARE.md         # Hardware specifications
```

---

## 🎯 Quick Start

### Install Dependencies
```bash
pip install pygame numpy
```

### Assemble and Run
```bash
# Assemble example program
python assembler/asm.py examples/hello.asm -o hello.bin

# Run in emulator
python emulator/emulator.py hello.bin
```

### Try the Examples
```bash
# Snake game
python assembler/asm.py examples/snake.asm -o snake.bin
python emulator/emulator.py snake.bin

# Mandelbrot fractal
python assembler/asm.py examples/mandelbrot.asm -o mandelbrot.bin
python emulator/emulator.py mandelbrot.bin
```

---

## 📖 Instruction Set (Neiler-8)

### Data Movement
- `MOV dst, src` - Move data
- `LOAD addr` - Load from memory
- `STORE addr` - Store to memory
- `PUSH reg` - Push to stack
- `POP reg` - Pop from stack

### Arithmetic
- `ADD dst, src` - Addition
- `SUB dst, src` - Subtraction
- `INC reg` - Increment
- `DEC reg` - Decrement
- `MUL src` - Multiply (result in A)
- `DIV src` - Divide (result in A)

### Logic
- `AND dst, src` - Bitwise AND
- `OR dst, src` - Bitwise OR
- `XOR dst, src` - Bitwise XOR
- `NOT reg` - Bitwise NOT
- `SHL reg` - Shift left
- `SHR reg` - Shift right

### Control Flow
- `JMP addr` - Unconditional jump
- `JZ addr` - Jump if zero
- `JNZ addr` - Jump if not zero
- `CALL addr` - Call subroutine
- `RET` - Return from subroutine
- `HLT` - Halt CPU

### I/O
- `IN port` - Read from I/O port
- `OUT port` - Write to I/O port

---

## 🎮 GPU Programming

### Set Pixel
```asm
MOV A, 160      ; X coordinate
MOV B, 100      ; Y coordinate
MOV C, 0xFF     ; Color (red)
CALL SetPixel
```

### Draw Sprite
```asm
MOV A, 0        ; Sprite ID
MOV B, 50       ; X position
MOV C, 50       ; Y position
CALL DrawSprite
```

---

## 🔧 Architecture Details

### Memory Map (Neiler-8)
```
0x0000-0x00FF: Zero page (fast access)
0x0100-0x01FF: Stack
0x0200-0x7FFF: Program RAM
0x8000-0x9FFF: Video RAM
0xA000-0xBFFF: Sprite RAM
0xC000-0xFFFF: ROM/Program
```

### Registers
- **A, B**: Accumulator registers
- **C, D**: General purpose
- **X, Y**: Index registers
- **SP**: Stack pointer (0x0100-0x01FF)
- **PC**: Program counter
- **FLAGS**: Zero, Carry, Overflow, Negative

---

## 💡 Example Programs

### Hello World
```asm
; Print "Hello, World!" to screen
START:
    MOV X, 0            ; String index
LOOP:
    LOAD hello[X]       ; Load character
    CMP A, 0            ; Check for null terminator
    JZ END              ; If zero, end
    OUT 0x01            ; Output to terminal
    INC X               ; Next character
    JMP LOOP
END:
    HLT

hello: .str "Hello, World!\n"
```

### Counter (0-255)
```asm
START:
    MOV A, 0            ; Initialize counter
LOOP:
    OUT 0x02            ; Display on 7-segment
    CALL Delay          ; Wait
    INC A               ; Increment
    JMP LOOP

Delay:
    MOV B, 0xFF
DelayLoop:
    DEC B
    JNZ DelayLoop
    RET
```

---

## 🎨 GPU Capabilities

- **Resolution**: 320x200 @ 60Hz (8-bit) or 640x480 @ 60Hz (16-bit)
- **Colors**: 256 (8-bit palette) or 65,536 (16-bit true color)
- **Sprites**: 64 hardware sprites, 16x16 pixels each
- **Backgrounds**: 2 scrollable tile layers
- **Effects**: Transparency, flipping, rotation

---

## 🚀 Performance

- **CPU Speed**: Configurable (default 1MHz simulated)
- **Memory**: 64KB (8-bit) or 16MB (16-bit)
- **Instructions/sec**: ~1 million (emulated)

---

## 📚 Documentation

- [Full ISA Reference](docs/ISA.md)
- [Programming Guide](docs/PROGRAMMING.md)
- [Hardware Specs](docs/HARDWARE.md)
- [GPU Programming](docs/GPU.md)

---

## 🎯 Use Cases

- **Learn computer architecture** - Understand how CPUs work
- **Retro game development** - Make 8-bit/16-bit games
- **Compiler targets** - Backend for custom languages
- **Education** - Teach assembly programming
- **Emulation** - Study classic computer designs

---

## 🔮 Future Plans

- [ ] Neiler-32 (32-bit CPU)
- [ ] Sound processor
- [ ] Networking support
- [ ] FPGA implementation
- [ ] Physical hardware build

---

## 📜 License

MIT License - Build whatever you want!

---

**Built with ❤️ by pookiejames634-dotcom**

*Making computers from scratch since 2025*
