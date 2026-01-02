#!/usr/bin/env python3
"""
Neiler-64 Graphical Emulator
Complete emulator with visual display, CPU state, and memory viewer
"""

import sys
import os
import pygame
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'cpu'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'gpu'))

try:
    from neiler8 import Neiler8CPU
    from neilergpu import NeilerGPU
except ImportError:
    print("Error: Could not import Neiler CPU/GPU modules")
    print("Make sure neiler8.py and neilergpu.py exist in ../cpu and ../gpu")
    sys.exit(1)

# Display constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Neiler display size (320x200 or 640x480)
NEILER_WIDTH = 320
NEILER_HEIGHT = 200
NEILER_SCALE = 2  # Scale factor for visibility

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 100, 200)
RED = (200, 0, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)


class NeilerEmulator:
    """Complete Neiler-64 emulator with graphical interface"""

    def __init__(self):
        pygame.init()

        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neiler-64 Emulator")

        # Create Neiler CPU and GPU
        self.cpu = Neiler8CPU()
        self.gpu = NeilerGPU() if NeilerGPU else None

        # Create Neiler display surface
        self.neiler_display = pygame.Surface((NEILER_WIDTH, NEILER_HEIGHT))
        self.neiler_display.fill(BLACK)

        # Emulator state
        self.running = True
        self.paused = False
        self.step_mode = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Performance tracking
        self.cycles_per_frame = 1000  # CPU cycles per frame
        self.total_cycles = 0
        self.fps = 60

        # Memory viewer
        self.memory_offset = 0
        self.memory_view_size = 256

        # Load demo program
        self.load_demo_program()

    def load_demo_program(self):
        """Load a demo program"""
        # Demo: Draw colorful pixels across the screen
        program = [
            # Initialize
            0x01, 0x00,        # MOV A, 0      ; X coordinate
            0x02, 0x00,        # MOV B, 0      ; Y coordinate
            0x03, 0x01,        # MOV C, 1      ; Color

            # DRAW_LOOP:
            0x91, 0x80,        # OUT 0x80, A   ; Set X position (GPU port)
            0x91, 0x81,        # OUT 0x81, B   ; Set Y position
            0x91, 0x82,        # OUT 0x82, C   ; Draw pixel with color

            0x44,              # INC A         ; Next X
            0x44,              # INC C         ; Next color

            0x61, NEILER_WIDTH & 0xFF,  # CMP A, screen_width
            0x72, 0x02, 0x06,  # JNZ DRAW_LOOP (jump back to offset 0x0206)

            # Next line
            0x01, 0x00,        # MOV A, 0      ; Reset X
            0x45,              # INC B         ; Next Y
            0x61, NEILER_HEIGHT & 0xFF,  # CMP B, screen_height
            0x72, 0x02, 0x06,  # JNZ DRAW_LOOP

            # Loop forever
            0x70, 0x02, 0x00,  # JMP 0x0200 (start)
        ]

        self.cpu.load_program(program)
        print(f"Loaded demo program ({len(program)} bytes)")

    def load_program_from_file(self, filename):
        """Load program from binary file"""
        try:
            with open(filename, 'rb') as f:
                program = list(f.read())
            self.cpu.load_program(program)
            print(f"Loaded {filename} ({len(program)} bytes)")
        except Exception as e:
            print(f"Error loading program: {e}")

    def handle_input(self):
        """Handle keyboard and mouse input"""
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
                    # Single step
                    self.cpu.step()
                    self.total_cycles += 1
                elif event.key == pygame.K_r:
                    # Reset
                    self.cpu = Neiler8CPU()
                    self.load_demo_program()
                    self.total_cycles = 0
                elif event.key == pygame.K_UP:
                    self.memory_offset = max(0, self.memory_offset - 16)
                elif event.key == pygame.K_DOWN:
                    self.memory_offset = min(0xFF00, self.memory_offset + 16)
                elif event.key == pygame.K_PAGEUP:
                    self.memory_offset = max(0, self.memory_offset - 256)
                elif event.key == pygame.K_PAGEDOWN:
                    self.memory_offset = min(0xFF00, self.memory_offset + 256)
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.cycles_per_frame = min(10000, self.cycles_per_frame + 100)
                elif event.key == pygame.K_MINUS:
                    self.cycles_per_frame = max(1, self.cycles_per_frame - 100)

    def update_cpu(self):
        """Update CPU state"""
        if not self.paused and not self.step_mode and not self.cpu.halted:
            for _ in range(self.cycles_per_frame):
                if self.cpu.halted:
                    break
                self.cpu.step()
                self.total_cycles += 1

                # Handle GPU output
                self.handle_gpu_output()

    def handle_gpu_output(self):
        """Handle GPU I/O port writes from CPU"""
        # GPU ports: 0x80 = X, 0x81 = Y, 0x82 = Draw pixel
        if self.cpu.io_ports[0x82] != 0:  # Draw command
            x = self.cpu.io_ports[0x80] % NEILER_WIDTH
            y = self.cpu.io_ports[0x81] % NEILER_HEIGHT
            color_index = self.cpu.io_ports[0x82]

            # Generate color from index
            r = (color_index * 37) % 256
            g = (color_index * 73) % 256
            b = (color_index * 109) % 256

            # Draw pixel
            self.neiler_display.set_at((x, y), (r, g, b))

            # Clear draw command
            self.cpu.io_ports[0x82] = 0

    def draw_neiler_screen(self):
        """Draw the Neiler display"""
        # Scale and blit Neiler display
        scaled_display = pygame.transform.scale(
            self.neiler_display,
            (NEILER_WIDTH * NEILER_SCALE, NEILER_HEIGHT * NEILER_SCALE)
        )

        # Draw border
        border_rect = pygame.Rect(10, 10,
                                  NEILER_WIDTH * NEILER_SCALE + 4,
                                  NEILER_HEIGHT * NEILER_SCALE + 4)
        pygame.draw.rect(self.screen, GREEN, border_rect, 2)

        # Draw display
        self.screen.blit(scaled_display, (12, 12))

        # Label
        label = self.font.render("Neiler-64 Display", True, GREEN)
        self.screen.blit(label, (12, border_rect.bottom + 5))

    def draw_cpu_state(self):
        """Draw CPU register state"""
        x_offset = NEILER_WIDTH * NEILER_SCALE + 40
        y_offset = 20

        # Title
        title = self.font.render("CPU STATE", True, WHITE)
        self.screen.blit(title, (x_offset, y_offset))
        y_offset += 30

        # Registers
        registers = [
            f"A: 0x{self.cpu.A:02X} ({self.cpu.A:3d})",
            f"B: 0x{self.cpu.B:02X} ({self.cpu.B:3d})",
            f"C: 0x{self.cpu.C:02X} ({self.cpu.C:3d})",
            f"D: 0x{self.cpu.D:02X} ({self.cpu.D:3d})",
            f"X: 0x{self.cpu.X:02X} ({self.cpu.X:3d})",
            f"Y: 0x{self.cpu.Y:02X} ({self.cpu.Y:3d})",
            "",
            f"PC: 0x{self.cpu.PC:04X}",
            f"SP: 0x{self.cpu.SP:02X}",
            "",
            f"Flags:",
            f"  Z:{self.cpu.FLAG_ZERO} C:{self.cpu.FLAG_CARRY}",
            f"  N:{self.cpu.FLAG_NEGATIVE} O:{self.cpu.FLAG_OVERFLOW}",
        ]

        for i, line in enumerate(registers):
            color = LIGHT_GRAY if line else GRAY
            text = self.small_font.render(line, True, color)
            self.screen.blit(text, (x_offset, y_offset + i * 20))

    def draw_memory_viewer(self):
        """Draw memory viewer"""
        x_offset = NEILER_WIDTH * NEILER_SCALE + 40
        y_offset = 320

        # Title
        title = self.font.render("MEMORY VIEWER", True, WHITE)
        self.screen.blit(title, (x_offset, y_offset))
        y_offset += 30

        # Memory dump
        for row in range(16):
            addr = self.memory_offset + (row * 16)

            # Address
            addr_text = self.small_font.render(f"{addr:04X}:", True, BLUE)
            self.screen.blit(addr_text, (x_offset, y_offset + row * 18))

            # Bytes
            bytes_str = ""
            for col in range(16):
                byte_addr = addr + col
                if byte_addr < len(self.cpu.memory):
                    byte = self.cpu.memory[byte_addr]
                    bytes_str += f"{byte:02X} "

            bytes_text = self.small_font.render(bytes_str, True, LIGHT_GRAY)
            self.screen.blit(bytes_text, (x_offset + 50, y_offset + row * 18))

    def draw_status_bar(self):
        """Draw status bar with info"""
        y_offset = SCREEN_HEIGHT - 60

        # Background
        pygame.draw.rect(self.screen, GRAY, (0, y_offset, SCREEN_WIDTH, 60))

        # Status info
        status_lines = [
            f"Cycles: {self.total_cycles:,} | Speed: {self.cycles_per_frame} cyc/frame | FPS: {self.fps:.1f}",
            f"Status: {'PAUSED' if self.paused else 'HALTED' if self.cpu.halted else 'RUNNING'} | "
            f"[SPACE] Pause | [S] Step Mode | [N] Next | [R] Reset | [+/-] Speed | [ESC] Quit"
        ]

        for i, line in enumerate(status_lines):
            text = self.small_font.render(line, True, WHITE if i == 0 else LIGHT_GRAY)
            self.screen.blit(text, (10, y_offset + 10 + i * 20))

    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(BLACK)

        # Draw components
        self.draw_neiler_screen()
        self.draw_cpu_state()
        self.draw_memory_viewer()
        self.draw_status_bar()

        # Update display
        pygame.display.flip()

    def run(self):
        """Main emulator loop"""
        print("\n" + "="*60)
        print("  NEILER-64 EMULATOR")
        print("="*60)
        print("\nControls:")
        print("  SPACE     - Pause/Resume")
        print("  S         - Toggle step mode")
        print("  N         - Next instruction (when paused)")
        print("  R         - Reset")
        print("  +/-       - Adjust speed")
        print("  UP/DOWN   - Scroll memory")
        print("  ESC       - Quit")
        print("\nStarting emulator...\n")

        while self.running:
            # Handle input
            self.handle_input()

            # Update CPU
            self.update_cpu()

            # Draw
            self.draw()

            # Maintain FPS
            self.fps = self.clock.get_fps()
            self.clock.tick(FPS)

        pygame.quit()
        print("\nEmulator stopped.")
        print(f"Total cycles executed: {self.total_cycles:,}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Neiler-64 Graphical Emulator")
    parser.add_argument('program', nargs='?', help='Binary program file to load')
    parser.add_argument('--speed', type=int, default=1000,
                       help='CPU cycles per frame (default: 1000)')
    args = parser.parse_args()

    # Create emulator
    emulator = NeilerEmulator()

    # Load program if specified
    if args.program:
        emulator.load_program_from_file(args.program)

    # Set speed
    if args.speed:
        emulator.cycles_per_frame = args.speed

    # Run
    emulator.run()


if __name__ == "__main__":
    main()
