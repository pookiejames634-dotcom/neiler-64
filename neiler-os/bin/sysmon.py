#!/usr/bin/env python3
"""
Neiler-64 System Monitor
Real-time system monitoring for Neiler-OS
"""

import time
import psutil
import socket
import sys
from datetime import datetime, timedelta

def get_system_info():
    """Get comprehensive system information"""

    # CPU info
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    # Memory info
    memory = psutil.virtual_memory()

    # Disk info
    disk = psutil.disk_usage('/')

    # Network info
    net_io = psutil.net_io_counters()

    # System uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time

    return {
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count,
            'freq': cpu_freq.current if cpu_freq else 0
        },
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        },
        'network': {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        },
        'uptime': uptime
    }

def format_bytes(bytes_val):
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"

def print_system_stats():
    """Print formatted system statistics"""
    info = get_system_info()

    print("\n" + "="*70)
    print(f"Neiler-64 System Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # System info
    print(f"\nSystem Uptime: {str(info['uptime']).split('.')[0]}")
    print(f"Hostname: {socket.gethostname()}")

    # CPU
    print(f"\nCPU:")
    print(f"  • Cores: {info['cpu']['count']}")
    print(f"  • Frequency: {info['cpu']['freq']:.2f} MHz")
    print(f"  • Usage: {info['cpu']['percent']}%")
    cpu_bar = '█' * int(info['cpu']['percent'] / 2) + '░' * (50 - int(info['cpu']['percent'] / 2))
    print(f"  [{cpu_bar}]")

    # Memory
    print(f"\nMemory:")
    print(f"  • Total: {format_bytes(info['memory']['total'])}")
    print(f"  • Used: {format_bytes(info['memory']['used'])}")
    print(f"  • Available: {format_bytes(info['memory']['available'])}")
    print(f"  • Usage: {info['memory']['percent']}%")
    mem_bar = '█' * int(info['memory']['percent'] / 2) + '░' * (50 - int(info['memory']['percent'] / 2))
    print(f"  [{mem_bar}]")

    # Disk
    print(f"\nDisk:")
    print(f"  • Total: {format_bytes(info['disk']['total'])}")
    print(f"  • Used: {format_bytes(info['disk']['used'])}")
    print(f"  • Free: {format_bytes(info['disk']['free'])}")
    print(f"  • Usage: {info['disk']['percent']}%")
    disk_bar = '█' * int(info['disk']['percent'] / 2) + '░' * (50 - int(info['disk']['percent'] / 2))
    print(f"  [{disk_bar}]")

    # Network
    print(f"\nNetwork:")
    print(f"  • Sent: {format_bytes(info['network']['bytes_sent'])}")
    print(f"  • Received: {format_bytes(info['network']['bytes_recv'])}")

    # Processes
    print(f"\nTop Processes:")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top_procs = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:5]
    for proc in top_procs:
        print(f"  • PID {proc['pid']:5d}: {proc['name']:20s} ({proc['cpu_percent']:.1f}%)")

    print("="*70)

def monitor_loop(interval=10):
    """Continuous monitoring loop"""
    print("Neiler-64 System Monitor")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            print_system_stats()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        print_system_stats()
    else:
        monitor_loop()
