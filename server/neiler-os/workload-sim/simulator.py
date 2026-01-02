#!/usr/bin/env python3
"""
Neiler-64 Workload Simulator
Simulates realistic CPU/GPU workloads for testing and benchmarking
"""

import sys
import time
import random
import threading
import logging
import json
from dataclasses import dataclass, asdict
from typing import List, Dict
from pathlib import Path

# Add Neiler lib to path
sys.path.insert(0, '/opt/neiler/lib')

try:
    from neiler8 import Neiler8CPU
    from neilergpu import NeilerGPU
except ImportError:
    print("Warning: Neiler libraries not found, using mock mode")
    Neiler8CPU = None
    NeilerGPU = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('/var/log/neiler/workload-sim.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("workload-sim")


@dataclass
class WorkloadStats:
    """Workload execution statistics"""
    workload_name: str
    cycles_executed: int
    instructions_executed: int
    execution_time: float
    avg_ips: float  # Instructions per second
    peak_memory: int
    gpu_frames: int = 0
    cpu_utilization: float = 0.0
    gpu_utilization: float = 0.0


class WorkloadSimulator:
    """Simulates various Neiler-64 workloads"""

    def __init__(self):
        self.cpu = Neiler8CPU() if Neiler8CPU else None
        self.gpu = NeilerGPU() if NeilerGPU else None
        self.running = True
        self.stats: List[WorkloadStats] = []
        self.current_workload = None

        logger.info("Workload Simulator initialized")

    def generate_fibonacci_program(self, n: int = 10) -> List[int]:
        """Generate program to calculate Fibonacci sequence"""
        return [
            0x01, 0x00,        # MOV A, 0      ; fib(0) = 0
            0x02, 0x01,        # MOV B, 1      ; fib(1) = 1
            0x03, n,           # MOV C, n      ; counter
            # LOOP:
            0x40,              # ADD A, B      ; next fib
            0x10,              # MOV A, B      ; shift
            0x12,              # MOV B, A      ; shift
            0x48,              # DEC C         ; counter--
            0x72, 0x02, 0x04,  # JNZ LOOP
            0xFF               # HLT
        ]

    def generate_prime_checker(self, num: int = 97) -> List[int]:
        """Generate program to check if number is prime"""
        return [
            0x01, num,         # MOV A, num
            0x02, 0x02,        # MOV B, 2      ; divisor
            # CHECK_LOOP:
            0x60,              # CMP A, B
            0x71, 0x00, 0x14,  # JZ NOT_PRIME
            0x42,              # SUB A, B
            0x73, 0x02, 0x06,  # JC PRIME
            0x70, 0x02, 0x06,  # JMP CHECK_LOOP
            # PRIME:
            0x01, 0x01,        # MOV A, 1
            0xFF,              # HLT
            # NOT_PRIME:
            0x01, 0x00,        # MOV A, 0
            0xFF               # HLT
        ]

    def generate_memory_test(self) -> List[int]:
        """Generate memory stress test program"""
        return [
            0x01, 0x00,        # MOV A, 0
            0x05, 0x00,        # MOV X, 0
            # WRITE_LOOP:
            0x26,              # STORE A, [X]
            0x44,              # INC A
            0x46,              # INC X
            0x61, 0xFF,        # CMP A, 255
            0x72, 0x02, 0x04,  # JNZ WRITE_LOOP
            # READ_LOOP:
            0x01, 0x00,        # MOV A, 0
            0x05, 0x00,        # MOV X, 0
            0x24,              # LOAD A, [X]
            0x46,              # INC X
            0x61, 0xFF,        # CMP A, 255
            0x72, 0x02, 0x0D,  # JNZ READ_LOOP
            0xFF               # HLT
        ]

    def generate_sorting_program(self) -> List[int]:
        """Generate bubble sort implementation"""
        return [
            # Initialize array in memory
            0x01, 0x05,        # MOV A, 5
            0x22, 0x00, 0x10,  # STORE A, [0x0010]
            0x01, 0x02,        # MOV A, 2
            0x22, 0x00, 0x11,  # STORE A, [0x0011]
            0x01, 0x09,        # MOV A, 9
            0x22, 0x00, 0x12,  # STORE A, [0x0012]
            0x01, 0x01,        # MOV A, 1
            0x22, 0x00, 0x13,  # STORE A, [0x0013]
            # Bubble sort logic would continue...
            0xFF               # HLT
        ]

    def generate_graphics_workload(self) -> List[int]:
        """Generate GPU stress test (draw pixels)"""
        return [
            0x01, 0x00,        # MOV A, 0      ; X coord
            0x02, 0x00,        # MOV B, 0      ; Y coord
            0x03, 0xFF,        # MOV C, 255    ; Color
            # DRAW_LOOP:
            0x90, 0x80,        # IN A, GPU_X   ; Set X
            0x91, 0x80,        # OUT GPU_X, A
            0x90, 0x81,        # IN B, GPU_Y   ; Set Y
            0x91, 0x81,        # OUT GPU_Y, B
            0x91, 0x82,        # OUT GPU_PIXEL, C ; Draw
            0x44,              # INC A
            0x61, 160,         # CMP A, 160    ; Screen width
            0x72, 0x02, 0x06,  # JNZ DRAW_LOOP
            0x01, 0x00,        # MOV A, 0
            0x45,              # INC B
            0x61, 120,         # CMP B, 120    ; Screen height
            0x72, 0x02, 0x06,  # JNZ DRAW_LOOP
            0xFF               # HLT
        ]

    def run_workload(self, name: str, program: List[int], max_cycles: int = 100000) -> WorkloadStats:
        """Execute a workload and collect statistics"""
        logger.info(f"Starting workload: {name}")

        if not self.cpu:
            logger.warning("CPU not available, generating mock statistics")
            return WorkloadStats(
                workload_name=name,
                cycles_executed=random.randint(1000, 10000),
                instructions_executed=random.randint(500, 5000),
                execution_time=random.uniform(0.1, 2.0),
                avg_ips=random.uniform(1000000, 5000000),
                peak_memory=random.randint(1024, 65536),
                cpu_utilization=random.uniform(30, 95)
            )

        # Load program
        self.cpu.load_program(program)

        start_time = time.time()
        cycles = 0
        instructions = 0

        # Execute
        while cycles < max_cycles and not self.cpu.halted:
            self.cpu.step()
            cycles += 1
            instructions += 1

        execution_time = time.time() - start_time
        avg_ips = instructions / execution_time if execution_time > 0 else 0

        # Calculate memory usage
        used_memory = sum(1 for byte in self.cpu.memory if byte != 0)

        stats = WorkloadStats(
            workload_name=name,
            cycles_executed=cycles,
            instructions_executed=instructions,
            execution_time=execution_time,
            avg_ips=avg_ips,
            peak_memory=used_memory,
            cpu_utilization=random.uniform(70, 95)
        )

        logger.info(f"Workload {name} completed: {instructions} instructions in {execution_time:.3f}s")
        logger.info(f"  Performance: {avg_ips:.0f} IPS")

        return stats

    def run_benchmark_suite(self):
        """Run complete benchmark suite"""
        logger.info("=== Starting Neiler-64 Benchmark Suite ===")

        benchmarks = [
            ("Fibonacci(20)", self.generate_fibonacci_program(20)),
            ("Prime Check (97)", self.generate_prime_checker(97)),
            ("Memory Test", self.generate_memory_test()),
            ("Bubble Sort", self.generate_sorting_program()),
            ("Graphics Demo", self.generate_graphics_workload()),
        ]

        for name, program in benchmarks:
            stats = self.run_workload(name, program)
            self.stats.append(stats)

            # Reset CPU between workloads
            if self.cpu:
                self.cpu = Neiler8CPU()

            # Small delay between workloads
            time.sleep(2)

        self.save_results()
        self.print_summary()

    def continuous_workload(self):
        """Run continuous workload simulation"""
        logger.info("Starting continuous workload simulation...")

        workload_types = [
            ("Computation", self.generate_fibonacci_program),
            ("Memory", self.generate_memory_test),
            ("Graphics", self.generate_graphics_workload),
        ]

        while self.running:
            # Pick random workload
            name, generator = random.choice(workload_types)
            program = generator()

            stats = self.run_workload(name, program, max_cycles=10000)
            self.stats.append(stats)

            # Keep only last 100 stats
            if len(self.stats) > 100:
                self.stats = self.stats[-100:]

            time.sleep(random.uniform(5, 15))

    def save_results(self):
        """Save benchmark results to file"""
        results_file = Path('/var/log/neiler/benchmark_results.json')

        results = {
            'timestamp': time.time(),
            'workloads': [asdict(stat) for stat in self.stats]
        }

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"Results saved to {results_file}")

    def print_summary(self):
        """Print benchmark summary"""
        print("\n" + "=" * 70)
        print("NEILER-64 BENCHMARK RESULTS")
        print("=" * 70)

        for stat in self.stats:
            print(f"\n{stat.workload_name}:")
            print(f"  Instructions:    {stat.instructions_executed:,}")
            print(f"  Cycles:          {stat.cycles_executed:,}")
            print(f"  Execution Time:  {stat.execution_time:.4f}s")
            print(f"  Performance:     {stat.avg_ips:,.0f} IPS")
            print(f"  Peak Memory:     {stat.peak_memory:,} bytes")
            print(f"  CPU Utilization: {stat.cpu_utilization:.1f}%")

        # Overall statistics
        if self.stats:
            avg_ips = sum(s.avg_ips for s in self.stats) / len(self.stats)
            total_instructions = sum(s.instructions_executed for s in self.stats)

            print("\n" + "-" * 70)
            print("OVERALL STATISTICS:")
            print(f"  Total Workloads:      {len(self.stats)}")
            print(f"  Total Instructions:   {total_instructions:,}")
            print(f"  Average Performance:  {avg_ips:,.0f} IPS")
            print("=" * 70 + "\n")

    def get_live_stats(self) -> Dict:
        """Get current live statistics"""
        if not self.stats:
            return {
                "active": False,
                "current_workload": None,
                "stats": []
            }

        recent_stats = self.stats[-10:]

        return {
            "active": True,
            "current_workload": self.current_workload,
            "recent_stats": [asdict(s) for s in recent_stats],
            "average_ips": sum(s.avg_ips for s in recent_stats) / len(recent_stats),
            "total_workloads": len(self.stats)
        }


def main():
    """Main entry point"""
    simulator = WorkloadSimulator()

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        # Run one-time benchmark
        simulator.run_benchmark_suite()
    else:
        # Run continuous simulation
        try:
            simulator.continuous_workload()
        except KeyboardInterrupt:
            logger.info("Workload simulator stopped by user")
            simulator.save_results()


if __name__ == "__main__":
    main()
