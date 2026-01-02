#!/usr/bin/env python3
"""
Neiler-64 Workload Simulator
Simulates realistic CPU and GPU workloads for the Neiler-64 system
"""

import time
import random
import threading
import sys
from datetime import datetime

class NeilerCPU:
    """Simulates Neiler-8 CPU workload"""

    def __init__(self):
        self.registers = {
            'A': 0, 'B': 0, 'C': 0, 'D': 0,
            'X': 0, 'Y': 0, 'PC': 0x0200, 'SP': 0xFF
        }
        self.cycles = 0
        self.instructions_executed = 0

    def execute_instruction(self):
        """Simulate executing a single instruction"""
        # Simulate various instruction types
        instruction_types = ['MOV', 'ADD', 'SUB', 'LOAD', 'STORE', 'JMP', 'CALL']
        instruction = random.choice(instruction_types)

        # Simulate different cycle counts
        cycles = {
            'MOV': 2, 'ADD': 3, 'SUB': 3,
            'LOAD': 4, 'STORE': 4, 'JMP': 2, 'CALL': 5
        }

        self.cycles += cycles.get(instruction, 2)
        self.instructions_executed += 1

        # Update random register
        reg = random.choice(['A', 'B', 'C', 'D'])
        self.registers[reg] = random.randint(0, 255)

    def get_stats(self):
        return {
            'cycles': self.cycles,
            'instructions': self.instructions_executed,
            'ips': self.instructions_executed / max(time.time() - start_time, 1)
        }

class NeilerGPU:
    """Simulates NeilerGPU workload"""

    def __init__(self):
        self.frame_count = 0
        self.sprite_count = 64
        self.resolution = (640, 480)
        self.fps = 0
        self.last_frame_time = time.time()

    def render_frame(self):
        """Simulate rendering a frame"""
        # Simulate sprite rendering
        for sprite in range(self.sprite_count):
            # Simulate sprite calculations
            x = random.randint(0, self.resolution[0])
            y = random.randint(0, self.resolution[1])

        # Simulate pixel fill
        pixels_drawn = random.randint(10000, 50000)

        self.frame_count += 1

        # Calculate FPS
        current_time = time.time()
        if current_time - self.last_frame_time > 0:
            self.fps = 1.0 / (current_time - self.last_frame_time)
        self.last_frame_time = current_time

    def get_stats(self):
        return {
            'frames': self.frame_count,
            'fps': self.fps,
            'sprites': self.sprite_count
        }

class WorkloadSimulator:
    """Main workload simulator"""

    def __init__(self):
        self.cpu = NeilerCPU()
        self.gpu = NeilerGPU()
        self.running = True
        self.start_time = time.time()

    def cpu_workload(self):
        """CPU workload thread"""
        while self.running:
            for _ in range(1000):
                self.cpu.execute_instruction()
            time.sleep(0.01)  # 10ms delay

    def gpu_workload(self):
        """GPU workload thread"""
        while self.running:
            self.gpu.render_frame()
            time.sleep(1/60)  # Target 60 FPS

    def print_stats(self):
        """Print workload statistics"""
        while self.running:
            time.sleep(5)  # Update every 5 seconds

            cpu_stats = self.cpu.get_stats()
            gpu_stats = self.gpu.get_stats()
            uptime = time.time() - self.start_time

            print(f"\n{'='*60}")
            print(f"Neiler-64 Workload Statistics - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*60}")
            print(f"Uptime: {int(uptime)}s")
            print(f"\nCPU (Neiler-8):")
            print(f"  • Instructions: {cpu_stats['instructions']:,}")
            print(f"  • Cycles: {cpu_stats['cycles']:,}")
            print(f"  • IPS: {cpu_stats['ips']:.2f}")
            print(f"  • Registers: A={self.cpu.registers['A']:02X} B={self.cpu.registers['B']:02X} C={self.cpu.registers['C']:02X}")
            print(f"\nGPU (NeilerGPU):")
            print(f"  • Frames: {gpu_stats['frames']:,}")
            print(f"  • FPS: {gpu_stats['fps']:.1f}")
            print(f"  • Sprites: {gpu_stats['sprites']}")
            print(f"  • Resolution: {self.gpu.resolution[0]}x{self.gpu.resolution[1]}")
            print(f"{'='*60}")

    def run(self):
        """Start the simulator"""
        print("Starting Neiler-64 Workload Simulator...")
        print("Press Ctrl+C to stop\n")

        # Start threads
        cpu_thread = threading.Thread(target=self.cpu_workload, daemon=True)
        gpu_thread = threading.Thread(target=self.gpu_workload, daemon=True)
        stats_thread = threading.Thread(target=self.print_stats, daemon=True)

        cpu_thread.start()
        gpu_thread.start()
        stats_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopping simulator...")
            self.running = False
            time.sleep(1)
            print("Simulator stopped.")

if __name__ == "__main__":
    start_time = time.time()
    simulator = WorkloadSimulator()
    simulator.run()
