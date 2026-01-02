#!/usr/bin/env python3
"""
Neiler Init System (PID 1)
Fast, dependency-based init system for Neiler-OS

Features:
- Parallel service startup
- Dependency resolution
- Service supervision
- Socket activation
- Real-time logging
"""

import os
import sys
import time
import signal
import subprocess
import threading
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum

# Configuration
SERVICE_DIR = Path("/etc/neiler/services")
RUNTIME_DIR = Path("/run/neiler")
LOG_DIR = Path("/var/log/neiler")

# Ensure directories exist
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "init.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("neiler-init")


class ServiceState(Enum):
    """Service states"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


@dataclass
class Service:
    """Service definition"""
    name: str
    description: str = ""
    exec_start: str = ""
    exec_stop: Optional[str] = None
    restart: str = "no"  # no, always, on-failure
    restart_delay: int = 5
    user: str = "root"
    group: str = "root"
    after: List[str] = field(default_factory=list)
    requires: List[str] = field(default_factory=list)
    wants: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)

    state: ServiceState = ServiceState.STOPPED
    process: Optional[subprocess.Popen] = None
    start_time: float = 0
    restart_count: int = 0


class NeilerInit:
    """Neiler Init System (PID 1)"""

    def __init__(self):
        self.services: Dict[str, Service] = {}
        self.running = True
        self.shutdown_signal = None

        # Register signal handlers
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGCHLD, self.handle_sigchld)

        logger.info("Neiler Init System starting...")
        logger.info(f"PID: {os.getpid()}")

    def load_services(self):
        """Load all service definitions"""
        if not SERVICE_DIR.exists():
            logger.warning(f"Service directory {SERVICE_DIR} does not exist")
            return

        for service_file in SERVICE_DIR.glob("*.service"):
            try:
                service = self.parse_service(service_file)
                self.services[service.name] = service
                logger.info(f"Loaded service: {service.name}")
            except Exception as e:
                logger.error(f"Failed to load {service_file}: {e}")

    def parse_service(self, path: Path) -> Service:
        """Parse service definition file"""
        config = {}
        current_section = None

        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    continue

                if '=' in line and current_section == "Service":
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

        # Create Service object
        service = Service(
            name=config.get('Name', path.stem),
            description=config.get('Description', ''),
            exec_start=config.get('ExecStart', ''),
            exec_stop=config.get('ExecStop'),
            restart=config.get('Restart', 'no'),
            user=config.get('User', 'root'),
            group=config.get('Group', 'root'),
            after=config.get('After', '').split() if config.get('After') else [],
            requires=config.get('Requires', '').split() if config.get('Requires') else [],
            wants=config.get('Wants', '').split() if config.get('Wants') else []
        )

        return service

    def resolve_dependencies(self, service_name: str, visited: Set[str] = None) -> List[str]:
        """Resolve service dependencies (topological sort)"""
        if visited is None:
            visited = set()

        if service_name in visited:
            return []

        visited.add(service_name)
        service = self.services.get(service_name)
        if not service:
            return []

        order = []

        # Process dependencies
        for dep in service.after + service.requires:
            if dep in self.services:
                order.extend(self.resolve_dependencies(dep, visited))

        order.append(service_name)
        return order

    def start_service(self, service_name: str) -> bool:
        """Start a service"""
        service = self.services.get(service_name)
        if not service:
            logger.error(f"Service {service_name} not found")
            return False

        if service.state == ServiceState.RUNNING:
            logger.info(f"Service {service_name} already running")
            return True

        # Check dependencies
        for dep in service.requires:
            dep_service = self.services.get(dep)
            if not dep_service or dep_service.state != ServiceState.RUNNING:
                if not self.start_service(dep):
                    logger.error(f"Failed to start required dependency {dep}")
                    return False

        logger.info(f"Starting service: {service.description or service_name}")
        service.state = ServiceState.STARTING

        try:
            # Prepare environment
            env = os.environ.copy()
            env.update(service.environment)

            # Start process
            service.process = subprocess.Popen(
                service.exec_start,
                shell=True,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=self.drop_privileges(service.user, service.group)
            )

            service.state = ServiceState.RUNNING
            service.start_time = time.time()
            logger.info(f"Service {service_name} started (PID: {service.process.pid})")

            # Monitor output in background
            threading.Thread(
                target=self.monitor_service_output,
                args=(service,),
                daemon=True
            ).start()

            return True

        except Exception as e:
            logger.error(f"Failed to start {service_name}: {e}")
            service.state = ServiceState.FAILED
            return False

    def stop_service(self, service_name: str, timeout: int = 10) -> bool:
        """Stop a service"""
        service = self.services.get(service_name)
        if not service or service.state != ServiceState.RUNNING:
            return True

        logger.info(f"Stopping service: {service_name}")
        service.state = ServiceState.STOPPING

        try:
            if service.exec_stop:
                # Use custom stop command
                subprocess.run(service.exec_stop, shell=True, timeout=timeout)
            elif service.process:
                # Send SIGTERM
                service.process.terminate()

                try:
                    service.process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Service {service_name} did not stop, killing...")
                    service.process.kill()
                    service.process.wait()

            service.state = ServiceState.STOPPED
            service.process = None
            logger.info(f"Service {service_name} stopped")
            return True

        except Exception as e:
            logger.error(f"Failed to stop {service_name}: {e}")
            return False

    def monitor_service_output(self, service: Service):
        """Monitor service stdout/stderr"""
        if not service.process:
            return

        log_file = LOG_DIR / f"{service.name}.log"

        with open(log_file, 'a') as log:
            for line in service.process.stdout:
                log.write(line.decode('utf-8', errors='replace'))
                log.flush()

    def handle_sigchld(self, signum, frame):
        """Handle child process termination"""
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break

                # Find service by PID
                for service in self.services.values():
                    if service.process and service.process.pid == pid:
                        self.handle_service_exit(service, status)
                        break

            except ChildProcessError:
                break

    def handle_service_exit(self, service: Service, status: int):
        """Handle service process exit"""
        logger.info(f"Service {service.name} exited with status {status}")

        service.process = None

        if service.state == ServiceState.STOPPING:
            service.state = ServiceState.STOPPED
            return

        # Handle restart policy
        if service.restart == "always" or (service.restart == "on-failure" and status != 0):
            service.state = ServiceState.FAILED
            service.restart_count += 1

            logger.info(f"Restarting {service.name} in {service.restart_delay} seconds...")

            threading.Timer(
                service.restart_delay,
                self.start_service,
                args=(service.name,)
            ).start()
        else:
            service.state = ServiceState.FAILED if status != 0 else ServiceState.STOPPED

    def drop_privileges(self, user: str, group: str):
        """Return preexec_fn for dropping privileges"""
        def set_ids():
            if user != 'root':
                import pwd
                import grp
                pw_record = pwd.getpwnam(user)
                os.setgid(pw_record.pw_gid)
                os.setuid(pw_record.pw_uid)
        return set_ids

    def handle_signal(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.shutdown_signal = signum
        self.shutdown()

    def shutdown(self):
        """Shutdown system"""
        logger.info("Shutting down Neiler-OS...")

        # Stop all services in reverse order
        service_list = list(self.services.keys())
        for service_name in reversed(service_list):
            self.stop_service(service_name)

        logger.info("All services stopped")
        self.running = False

    def run(self):
        """Main init loop"""
        # Load services
        self.load_services()

        # Start default target services
        default_services = [
            "system-setup",
            "networking",
            "sshd",
            "neiler-monitor",
            "workload-sim"
        ]

        for service_name in default_services:
            if service_name in self.services:
                threading.Thread(
                    target=self.start_service,
                    args=(service_name,),
                    daemon=True
                ).start()

        logger.info("Neiler-OS boot complete")

        # Main loop (as PID 1, we must never exit)
        while self.running:
            time.sleep(1)

        logger.info("Neiler Init exiting")
        sys.exit(0)


if __name__ == "__main__":
    # Verify we're running as PID 1
    if os.getpid() != 1:
        logger.warning("Not running as PID 1, this is a test mode")

    init = NeilerInit()
    init.run()
