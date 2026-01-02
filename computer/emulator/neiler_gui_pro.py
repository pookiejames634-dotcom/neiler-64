#!/usr/bin/env python3
"""
Neiler-64 Professional GUI
Advanced emulator with complete visualization of CPU, GPU, Memory, and more
"""

import sys
import os
import pygame
import time
from pathlib import Path
from collections import deque

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'cpu'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'gpu'))

try:
    from neiler8 import Neiler8CPU
except ImportError:
    print("Error: Could not import Neiler CPU module")
    sys.exit(1)

# Display constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Layout
PANEL_MARGIN = 10
PANEL_PADDING = 15

# Neiler display
NEILER_WIDTH = 320
NEILER_HEIGHT = 200
NEILER_SCALE = 3

# Colors - Professional dark theme
BG_COLOR = (20, 20, 25)
PANEL_BG = (30, 30, 35)
PANEL_BORDER = (60, 60, 70)
TEXT_COLOR = (220, 220, 230)
TEXT_DIM = (140, 140, 150)
ACCENT_COLOR = (0, 180, 255)
SUCCESS_COLOR = (0, 220, 100)
WARNING_COLOR = (255, 180, 0)
ERROR_COLOR = (255, 80, 80)
HIGHLIGHT_COLOR = (80, 80, 100)

# Opcode names for disassembly
OPCODE_NAMES = {
    0x00: 'NOP', 0x01: 'MOV A,imm', 0x02: 'MOV B,imm', 0x03: 'MOV C,imm',
    0x04: 'MOV D,imm', 0x05: 'MOV X,imm', 0x06: 'MOV Y,imm',
    0x10: 'MOV A,B', 0x11: 'MOV A,C', 0x12: 'MOV B,A', 0x13: 'MOV C,A',
    0x20: 'LOAD A,[addr]', 0x21: 'LOAD B,[addr]',
    0x22: 'STORE A,[addr]', 0x23: 'STORE B,[addr]',
    0x24: 'LOAD A,[X]', 0x25: 'LOAD A,[Y]',
    0x26: 'STORE A,[X]', 0x27: 'STORE A,[Y]',
    0x30: 'PUSH A', 0x31: 'PUSH B', 0x32: 'POP A', 0x33: 'POP B',
    0x40: 'ADD A,B', 0x41: 'ADD A,imm', 0x42: 'SUB A,B', 0x43: 'SUB A,imm',
    0x44: 'INC A', 0x45: 'INC B', 0x46: 'INC X', 0x47: 'INC Y',
    0x48: 'DEC A', 0x49: 'DEC B', 0x4A: 'DEC X', 0x4B: 'DEC Y',
    0x50: 'AND A,B', 0x51: 'OR A,B', 0x52: 'XOR A,B', 0x53: 'NOT A',
    0x54: 'SHL A', 0x55: 'SHR A',
    0x60: 'CMP A,B', 0x61: 'CMP A,imm',
    0x70: 'JMP addr', 0x71: 'JZ addr', 0x72: 'JNZ addr',
    0x73: 'JC addr', 0x74: 'JNC addr', 0x75: 'JN addr',
    0x80: 'CALL addr', 0x81: 'RET',
    0x90: 'IN A,port', 0x91: 'OUT port,A',
    0xFF: 'HLT'
}


class Panel:
    """Base panel class"""
    def __init__(self, x, y, width, height, title=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.surface = pygame.Surface((width, height))

    def draw_border(self, screen):
        """Draw panel border and background"""
        # Background
        pygame.draw.rect(screen, PANEL_BG, self.rect)
        # Border
        pygame.draw.rect(screen, PANEL_BORDER, self.rect, 2)

        # Title bar
        if self.title:
            font = pygame.font.Font(None, 24)
            title_surf = font.render(self.title, True, ACCENT_COLOR)
            screen.blit(title_surf, (self.rect.x + PANEL_PADDING, self.rect.y + PANEL_PADDING))


class NeilerGUIPro:
    """Professional Neiler-64 GUI"""

    def __init__(self):
        pygame.init()

        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neiler-64 Professional Emulator - Full System View")

        # Fonts
        self.font_large = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_mono = pygame.font.SysFont('courier', 18)

        # Create CPU and surfaces
        self.cpu = Neiler8CPU()
        self.neiler_display = pygame.Surface((NEILER_WIDTH, NEILER_HEIGHT))
        self.neiler_display.fill((0, 0, 0))

        # State
        self.running = True
        self.paused = False
        self.step_mode = False
        self.clock = pygame.time.Clock()

        # Performance
        self.cycles_per_frame = 500
        self.total_cycles = 0
        self.fps = 60
        self.cycle_history = deque(maxlen=100)
        self.fps_history = deque(maxlen=100))

        # Memory/stack viewing
        self.memory_offset = 0x0200  # Start at program
        self.stack_offset = 0x01FF

        # Breakpoints
        self.breakpoints = set()

        # History
        self.instruction_history = deque(maxlen=50)

        # Layout panels
        self.create_panels()

        # Load demo
        self.load_demo_program()

    def create_panels(self):
        """Create UI panels"""
        # Main display (top left) - GPU output
        self.display_panel = Panel(
            PANEL_MARGIN, PANEL_MARGIN,
            NEILER_WIDTH * NEILER_SCALE + 40,
            NEILER_HEIGHT * NEILER_SCALE + 80,
            "GPU DISPLAY (320x200)"
        )

        # CPU State (top middle)
        display_end = self.display_panel.rect.right + PANEL_MARGIN
        self.cpu_panel = Panel(
            display_end, PANEL_MARGIN,
            400, 480,
            "CPU STATE"
        )

        # Memory Viewer (top right)
        cpu_end = self.cpu_panel.rect.right + PANEL_MARGIN
        self.memory_panel = Panel(
            cpu_end, PANEL_MARGIN,
            SCREEN_WIDTH - cpu_end - PANEL_MARGIN,
            480,
            "MEMORY VIEWER"
        )

        # Stack Viewer (middle left)
        display_bottom = self.display_panel.rect.bottom + PANEL_MARGIN
        self.stack_panel = Panel(
            PANEL_MARGIN, display_bottom,
            400, 300,
            "STACK"
        )

        # Disassembly (middle center)
        stack_end = self.stack_panel.rect.right + PANEL_MARGIN
        self.disasm_panel = Panel(
            stack_end, display_bottom,
            600, 300,
            "DISASSEMBLY"
        )

        # I/O Ports (middle right)
        disasm_end = self.disasm_panel.rect.right + PANEL_MARGIN
        self.io_panel = Panel(
            disasm_end, display_bottom,
            SCREEN_WIDTH - disasm_end - PANEL_MARGIN,
            300,
            "I/O PORTS"
        )

        # Performance Graph (bottom left)
        stack_bottom = self.stack_panel.rect.bottom + PANEL_MARGIN
        self.perf_panel = Panel(
            PANEL_MARGIN, stack_bottom,
            800, 250,
            "PERFORMANCE"
        )

        # Control Panel (bottom right)
        perf_end = self.perf_panel.rect.right + PANEL_MARGIN
        self.control_panel = Panel(
            perf_end, stack_bottom,
            SCREEN_WIDTH - perf_end - PANEL_MARGIN,
            250,
            "CONTROLS"
        )

    def load_demo_program(self):
        """Load demo program"""
        program = [
            0x01, 0x00,        # MOV A, 0
            0x02, 0x00,        # MOV B, 0
            0x03, 0x01,        # MOV C, 1
            # LOOP:
            0x91, 0x80,        # OUT 0x80, A (X)
            0x91, 0x81,        # OUT 0x81, B (Y)
            0x91, 0x82,        # OUT 0x82, C (Color)
            0x44,              # INC A
            0x44,              # INC C
            0x61, 0x40,        # CMP A, 64
            0x72, 0x02, 0x06,  # JNZ LOOP
            0x01, 0x00,        # MOV A, 0
            0x45,              # INC B
            0x61, 0xC8,        # CMP B, 200
            0x72, 0x02, 0x06,  # JNZ LOOP
            0x70, 0x02, 0x00,  # JMP start
        ]
        self.cpu.load_program(program)

    def handle_input(self):
        """Handle input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_s:
                    self.step_mode = not self.step_mode
                elif event.key == pygame.K_n and (self.paused or self.step_mode):
                    self.cpu.step()
                    self.total_cycles += 1
                elif event.key == pygame.K_r:
                    self.cpu = Neiler8CPU()
                    self.load_demo_program()
                    self.total_cycles = 0
                    self.instruction_history.clear()
                elif event.key == pygame.K_UP:
                    self.memory_offset = max(0, self.memory_offset - 16)
                elif event.key == pygame.K_DOWN:
                    self.memory_offset = min(0xFF00, self.memory_offset + 16)
                elif event.key == pygame.K_EQUALS:
                    self.cycles_per_frame = min(10000, self.cycles_per_frame + 50)
                elif event.key == pygame.K_MINUS:
                    self.cycles_per_frame = max(1, self.cycles_per_frame - 50)

    def update_cpu(self):
        """Update CPU"""
        if not self.paused and not self.step_mode and not self.cpu.halted:
            for _ in range(self.cycles_per_frame):
                if self.cpu.halted:
                    break

                # Record instruction
                pc = self.cpu.PC
                opcode = self.cpu.memory[pc] if pc < len(self.cpu.memory) else 0

                self.cpu.step()
                self.total_cycles += 1

                # Track instruction
                self.instruction_history.append((pc, opcode))

                # Handle GPU
                if self.cpu.io_ports[0x82] != 0:
                    x = self.cpu.io_ports[0x80] % NEILER_WIDTH
                    y = self.cpu.io_ports[0x81] % NEILER_HEIGHT
                    color = self.cpu.io_ports[0x82]

                    r = (color * 37) % 256
                    g = (color * 73) % 256
                    b = (color * 109) % 256

                    self.neiler_display.set_at((x, y), (r, g, b))
                    self.cpu.io_ports[0x82] = 0

    def draw_display_panel(self):
        """Draw GPU display panel"""
        self.display_panel.draw_border(self.screen)

        # Scale and draw Neiler display
        scaled = pygame.transform.scale(
            self.neiler_display,
            (NEILER_WIDTH * NEILER_SCALE, NEILER_HEIGHT * NEILER_SCALE)
        )

        x = self.display_panel.rect.x + 20
        y = self.display_panel.rect.y + 50

        # CRT-style border
        border_rect = pygame.Rect(x - 2, y - 2,
                                  NEILER_WIDTH * NEILER_SCALE + 4,
                                  NEILER_HEIGHT * NEILER_SCALE + 4)
        pygame.draw.rect(self.screen, (100, 100, 120), border_rect, 2)

        self.screen.blit(scaled, (x, y))

    def draw_cpu_panel(self):
        """Draw CPU state panel"""
        self.cpu_panel.draw_border(self.screen)

        x = self.cpu_panel.rect.x + PANEL_PADDING
        y = self.cpu_panel.rect.y + 50

        # Registers - styled boxes
        registers = [
            ('A', self.cpu.A), ('B', self.cpu.B),
            ('C', self.cpu.C), ('D', self.cpu.D),
            ('X', self.cpu.X), ('Y', self.cpu.Y),
        ]

        for i, (name, value) in enumerate(registers):
            row = i // 2
            col = i % 2

            reg_x = x + col * 180
            reg_y = y + row * 60

            # Box
            box_rect = pygame.Rect(reg_x, reg_y, 160, 45)
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, box_rect)
            pygame.draw.rect(self.screen, ACCENT_COLOR, box_rect, 2)

            # Label
            label = self.font_medium.render(name, True, TEXT_DIM)
            self.screen.blit(label, (reg_x + 10, reg_y + 5))

            # Value
            val_text = f"0x{value:02X} ({value:3d})"
            val_surf = self.font_mono.render(val_text, True, SUCCESS_COLOR)
            self.screen.blit(val_surf, (reg_x + 10, reg_y + 25))

        # PC and SP
        y += 200
        pc_text = f"PC: 0x{self.cpu.PC:04X}"
        sp_text = f"SP: 0x{self.cpu.SP:02X}"

        pc_surf = self.font_medium.render(pc_text, True, WARNING_COLOR)
        sp_surf = self.font_medium.render(sp_text, True, WARNING_COLOR)

        self.screen.blit(pc_surf, (x, y))
        self.screen.blit(sp_surf, (x + 180, y))

        # Flags
        y += 40
        flag_text = self.font_small.render("FLAGS:", True, TEXT_DIM)
        self.screen.blit(flag_text, (x, y))

        y += 25
        flags = [
            (f'Z:{self.cpu.FLAG_ZERO}', self.cpu.FLAG_ZERO),
            (f'C:{self.cpu.FLAG_CARRY}', self.cpu.FLAG_CARRY),
            (f'N:{self.cpu.FLAG_NEGATIVE}', self.cpu.FLAG_NEGATIVE),
            (f'O:{self.cpu.FLAG_OVERFLOW}', self.cpu.FLAG_OVERFLOW),
        ]

        for i, (text, active) in enumerate(flags):
            color = SUCCESS_COLOR if active else TEXT_DIM
            flag_surf = self.font_mono.render(text, True, color)
            self.screen.blit(flag_surf, (x + i * 80, y))

        # Status
        y += 60
        status = "HALTED" if self.cpu.halted else "PAUSED" if self.paused else "RUNNING"
        status_color = ERROR_COLOR if self.cpu.halted else WARNING_COLOR if self.paused else SUCCESS_COLOR
        status_surf = self.font_large.render(status, True, status_color)
        self.screen.blit(status_surf, (x, y))

    def draw_memory_panel(self):
        """Draw memory viewer"""
        self.memory_panel.draw_border(self.screen)

        x = self.memory_panel.rect.x + PANEL_PADDING
        y = self.memory_panel.rect.y + 50

        # Memory dump
        for row in range(20):
            addr = self.memory_offset + (row * 16)

            # Highlight PC row
            if self.cpu.PC >= addr and self.cpu.PC < addr + 16:
                highlight_rect = pygame.Rect(x, y + row * 20 - 2,
                                            self.memory_panel.rect.width - 30, 20)
                pygame.draw.rect(self.screen, (60, 60, 80), highlight_rect)

            # Address
            addr_text = self.font_mono.render(f"{addr:04X}:", True, ACCENT_COLOR)
            self.screen.blit(addr_text, (x, y + row * 20))

            # Bytes
            bytes_str = ""
            ascii_str = ""
            for col in range(16):
                byte_addr = addr + col
                if byte_addr < len(self.cpu.memory):
                    byte = self.cpu.memory[byte_addr]
                    bytes_str += f"{byte:02X} "

                    # ASCII
                    if 32 <= byte < 127:
                        ascii_str += chr(byte)
                    else:
                        ascii_str += '.'

            bytes_surf = self.font_mono.render(bytes_str, True, TEXT_COLOR)
            self.screen.blit(bytes_surf, (x + 60, y + row * 20))

            ascii_surf = self.font_mono.render(ascii_str, True, TEXT_DIM)
            self.screen.blit(ascii_surf, (x + 450, y + row * 20))

    def draw_stack_panel(self):
        """Draw stack viewer"""
        self.stack_panel.draw_border(self.screen)

        x = self.stack_panel.rect.x + PANEL_PADDING
        y = self.stack_panel.rect.y + 50

        # Stack grows down from 0x01FF
        for i in range(12):
            addr = 0x01FF - i
            byte = self.cpu.memory[addr] if addr < len(self.cpu.memory) else 0

            # Highlight SP
            if addr == 0x0100 + self.cpu.SP:
                highlight_rect = pygame.Rect(x, y + i * 20 - 2, 350, 20)
                pygame.draw.rect(self.screen, (60, 60, 80), highlight_rect)
                marker = self.font_mono.render("← SP", True, WARNING_COLOR)
                self.screen.blit(marker, (x + 250, y + i * 20))

            stack_text = f"{addr:04X}: 0x{byte:02X}"
            color = SUCCESS_COLOR if addr == 0x0100 + self.cpu.SP else TEXT_COLOR
            text_surf = self.font_mono.render(stack_text, True, color)
            self.screen.blit(text_surf, (x, y + i * 20))

    def draw_disasm_panel(self):
        """Draw disassembly view"""
        self.disasm_panel.draw_border(self.screen)

        x = self.disasm_panel.rect.x + PANEL_PADDING
        y = self.disasm_panel.rect.y + 50

        # Disassemble around PC
        start_addr = max(0, self.cpu.PC - 5)

        for i in range(12):
            addr = start_addr + i * 3  # Rough estimate

            if addr >= len(self.cpu.memory):
                break

            opcode = self.cpu.memory[addr]
            mnemonic = OPCODE_NAMES.get(opcode, f"DB 0x{opcode:02X}")

            # Highlight current PC
            if addr == self.cpu.PC:
                highlight_rect = pygame.Rect(x, y + i * 20 - 2, 550, 20)
                pygame.draw.rect(self.screen, (80, 80, 100), highlight_rect)
                marker = self.font_mono.render("►", True, WARNING_COLOR)
                self.screen.blit(marker, (x - 20, y + i * 20))

            # Address
            addr_surf = self.font_mono.render(f"{addr:04X}:", True, ACCENT_COLOR)
            self.screen.blit(addr_surf, (x, y + i * 20))

            # Opcode bytes
            bytes_str = f"{opcode:02X}"
            bytes_surf = self.font_mono.render(bytes_str, True, TEXT_DIM)
            self.screen.blit(bytes_surf, (x + 70, y + i * 20))

            # Mnemonic
            instr_surf = self.font_mono.render(mnemonic, True, SUCCESS_COLOR)
            self.screen.blit(instr_surf, (x + 120, y + i * 20))

    def draw_io_panel(self):
        """Draw I/O ports"""
        self.io_panel.draw_border(self.screen)

        x = self.io_panel.rect.x + PANEL_PADDING
        y = self.io_panel.rect.y + 50

        # Show first 16 I/O ports
        for i in range(16):
            port = i
            value = self.cpu.io_ports[port]

            port_text = f"Port 0x{port:02X}: 0x{value:02X} ({value:3d})"
            color = SUCCESS_COLOR if value != 0 else TEXT_DIM
            text_surf = self.font_mono.render(port_text, True, color)
            self.screen.blit(text_surf, (x, y + i * 18))

    def draw_perf_panel(self):
        """Draw performance graph"""
        self.perf_panel.draw_border(self.screen)

        x = self.perf_panel.rect.x + PANEL_PADDING
        y = self.perf_panel.rect.y + 50

        # Stats
        stats = [
            f"Total Cycles: {self.total_cycles:,}",
            f"Speed: {self.cycles_per_frame} cycles/frame",
            f"FPS: {self.fps:.1f}",
            f"IPS: {self.cycles_per_frame * self.fps:,.0f}",
        ]

        for i, stat in enumerate(stats):
            stat_surf = self.font_small.render(stat, True, TEXT_COLOR)
            self.screen.blit(stat_surf, (x, y + i * 25))

        # Simple performance graph
        graph_y = y + 120
        graph_width = 700
        graph_height = 80

        # Background
        graph_rect = pygame.Rect(x, graph_y, graph_width, graph_height)
        pygame.draw.rect(self.screen, (40, 40, 50), graph_rect)
        pygame.draw.rect(self.screen, PANEL_BORDER, graph_rect, 1)

        # Track FPS history
        self.fps_history.append(self.fps)

        # Draw graph
        if len(self.fps_history) > 1:
            points = []
            for i, fps_val in enumerate(self.fps_history):
                px = x + (i / len(self.fps_history)) * graph_width
                py = graph_y + graph_height - (fps_val / 60.0 * graph_height)
                points.append((px, py))

            if len(points) > 1:
                pygame.draw.lines(self.screen, SUCCESS_COLOR, False, points, 2)

    def draw_control_panel(self):
        """Draw controls info"""
        self.control_panel.draw_border(self.screen)

        x = self.control_panel.rect.x + PANEL_PADDING
        y = self.control_panel.rect.y + 50

        controls = [
            "SPACE - Pause/Resume",
            "S - Step Mode",
            "N - Next Instruction",
            "R - Reset",
            "+ / - - Speed Control",
            "↑ / ↓ - Scroll Memory",
            "ESC - Quit",
        ]

        for i, control in enumerate(controls):
            text_surf = self.font_small.render(control, True, TEXT_COLOR)
            self.screen.blit(text_surf, (x, y + i * 25))

    def draw(self):
        """Draw everything"""
        self.screen.fill(BG_COLOR)

        # Draw all panels
        self.draw_display_panel()
        self.draw_cpu_panel()
        self.draw_memory_panel()
        self.draw_stack_panel()
        self.draw_disasm_panel()
        self.draw_io_panel()
        self.draw_perf_panel()
        self.draw_control_panel()

        pygame.display.flip()

    def run(self):
        """Main loop"""
        print("\n" + "="*60)
        print("  NEILER-64 PROFESSIONAL EMULATOR")
        print("  Full System Visualization")
        print("="*60)
        print("\nStarting...\n")

        while self.running:
            self.handle_input()
            self.update_cpu()
            self.draw()

            self.fps = self.clock.get_fps() if self.clock.get_fps() > 0 else 60
            self.clock.tick(FPS)

        pygame.quit()
        print(f"\nTotal cycles: {self.total_cycles:,}")


def main():
    emulator = NeilerGUIPro()
    emulator.run()


if __name__ == "__main__":
    main()
