FROM ubuntu:22.04

LABEL maintainer="Neiler Project <neiler@example.com>"
LABEL description="Neiler-OS - Developer-focused OS for Neiler-64"
LABEL version="1.0.0"

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color

# System timezone
ENV TZ=UTC

# Neiler-OS environment
ENV NEILER_OS_VERSION=1.0.0
ENV NEILER_HOME=/opt/neiler
ENV PATH="/opt/neiler/bin:${PATH}"

# Install base system packages
RUN apt-get update && apt-get install -y \
    # Core utilities
    bash \
    coreutils \
    util-linux \
    procps \
    systemd \
    # Networking
    openssh-server \
    net-tools \
    iputils-ping \
    iproute2 \
    dnsutils \
    curl \
    wget \
    # Development tools
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    gdb \
    git \
    vim \
    nano \
    # Python (for Neiler tools)
    python3 \
    python3-pip \
    python3-dev \
    # Additional utilities
    htop \
    tmux \
    screen \
    sudo \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages for Neiler tools
RUN pip3 install --no-cache-dir \
    numpy \
    pygame \
    pyyaml \
    click \
    rich \
    fastapi \
    uvicorn \
    websockets

# Create Neiler directory structure
RUN mkdir -p \
    /opt/neiler/bin \
    /opt/neiler/lib \
    /opt/neiler/share \
    /opt/neiler/emulator \
    /etc/neiler/services \
    /etc/neiler/config \
    /var/log/neiler \
    /run/neiler \
    /home/dev/.neiler

# Configure SSH
RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Create users
RUN useradd -m -s /bin/bash -G sudo dev && \
    echo 'dev:neiler64' | chpasswd && \
    echo 'root:neiler64' | chpasswd && \
    echo 'dev ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Copy Neiler-OS files
COPY server/neiler-os/ /opt/neiler/
COPY server/services/ /etc/neiler/services/
COPY server/config/ /etc/neiler/config/

# Copy Neiler computer system (CPU, GPU, assembler)
COPY computer/cpu/*.py /opt/neiler/lib/
COPY computer/gpu/*.py /opt/neiler/lib/
COPY computer/assembler/*.py /opt/neiler/bin/

# Install Neiler tools
RUN if [ -f /opt/neiler/init-system/neiler-init.py ]; then \
      ln -sf /opt/neiler/init-system/neiler-init.py /sbin/neiler-init && \
      chmod +x /sbin/neiler-init; \
    else \
      echo "WARNING: neiler-init.py not found, skipping init symlink"; \
    fi && \
    chmod +x /opt/neiler/bin/* || true && \
    chmod +x /opt/neiler/toolchain/* || true && \
    ln -sf /opt/neiler/bin/neiler-status /usr/local/bin/neiler-status && \
    ln -sf /opt/neiler/bin/neiler-benchmark /usr/local/bin/neiler-benchmark && \
    ln -sf /opt/neiler/bin/neiler-monitor /usr/local/bin/neiler-monitor && \
    ln -sf /opt/neiler/bin/neiler-examples /usr/local/bin/neiler-examples && \
    ln -sf /opt/neiler/bin/asm.py /usr/local/bin/nasm


# Create Neiler shell wrapper
RUN echo '#!/bin/bash' > /usr/bin/nsh && \
    echo 'export PS1="\[\e[1;36m\]neiler-os\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ "' >> /usr/bin/nsh && \
    echo 'export NEILER_MODE=1' >> /usr/bin/nsh && \
    echo 'bash --rcfile /opt/neiler/share/nshrc "$@"' >> /usr/bin/nsh && \
    chmod +x /usr/bin/nsh

# Create Neiler shell RC file
RUN echo '# Neiler Shell Configuration' > /opt/neiler/share/nshrc && \
    echo 'alias nasm="/opt/neiler/bin/asm.py"' >> /opt/neiler/share/nshrc && \
    echo 'alias neiler-emu="/opt/neiler/emulator/emulator.py"' >> /opt/neiler/share/nshrc && \
    echo 'alias ndb="/opt/neiler/bin/debugger.py"' >> /opt/neiler/share/nshrc && \
    echo 'alias neiler-status="/opt/neiler/bin/status.py"' >> /opt/neiler/share/nshrc && \
    echo 'export NEILER_CPU=neiler8' >> /opt/neiler/share/nshrc && \
    echo 'echo "Welcome to Neiler-OS v${NEILER_OS_VERSION}"' >> /opt/neiler/share/nshrc && \
    echo 'echo "Type '\''neiler-help'\'' for available commands"' >> /opt/neiler/share/nshrc

# Create MOTD (Message of the Day)
RUN echo '#!/bin/bash' > /etc/update-motd.d/00-neiler && \
    echo 'cat << "EOF"' >> /etc/update-motd.d/00-neiler && \
    echo '    _   __     _ __          ____  _____' >> /etc/update-motd.d/00-neiler && \
    echo '   / | / /__  (_) /__  _____/ __ \/ ___/' >> /etc/update-motd.d/00-neiler && \
    echo '  /  |/ / _ \/ / / _ \/ ___/ / / /\__ \ ' >> /etc/update-motd.d/00-neiler && \
    echo ' / /|  /  __/ / /  __/ /  / /_/ /___/ / ' >> /etc/update-motd.d/00-neiler && \
    echo '/_/ |_/\___/_/_/\___/_/   \____//____/  ' >> /etc/update-motd.d/00-neiler && \
    echo '' >> /etc/update-motd.d/00-neiler && \
    echo 'Developer Edition v1.0.0' >> /etc/update-motd.d/00-neiler && \
    echo '' >> /etc/update-motd.d/00-neiler && \
    echo 'EOF' >> /etc/update-motd.d/00-neiler && \
    chmod +x /etc/update-motd.d/00-neiler

# Create startup script
RUN echo '#!/bin/bash' > /usr/local/bin/neiler-startup && \
    echo 'set -e' >> /usr/local/bin/neiler-startup && \
    echo 'echo "Starting Neiler-OS services..."' >> /usr/local/bin/neiler-startup && \
    echo 'mkdir -p /var/log/neiler' >> /usr/local/bin/neiler-startup && \
    echo 'touch /var/log/neiler/system.log' >> /usr/local/bin/neiler-startup && \
    echo '/usr/sbin/sshd -D &' >> /usr/local/bin/neiler-startup && \
    echo 'echo "SSH server started on port 22"' >> /usr/local/bin/neiler-startup && \
    echo 'if [ -f /opt/neiler/workload-sim/simulator.py ]; then' >> /usr/local/bin/neiler-startup && \
    echo '  python3 /opt/neiler/workload-sim/simulator.py >> /var/log/neiler/workload.log 2>&1 &' >> /usr/local/bin/neiler-startup && \
    echo '  echo "Workload simulator started"' >> /usr/local/bin/neiler-startup && \
    echo 'fi' >> /usr/local/bin/neiler-startup && \
    echo 'echo ""' >> /usr/local/bin/neiler-startup && \
    echo 'echo "==================================="' >> /usr/local/bin/neiler-startup && \
    echo 'echo "  Neiler-OS Server Running"' >> /usr/local/bin/neiler-startup && \
    echo 'echo "==================================="' >> /usr/local/bin/neiler-startup && \
    echo 'echo ""' >> /usr/local/bin/neiler-startup && \
    echo 'echo "SSH Access:"' >> /usr/local/bin/neiler-startup && \
    echo 'echo "  ssh dev@localhost -p 6767"' >> /usr/local/bin/neiler-startup && \
    echo 'echo "  Password: neiler64"' >> /usr/local/bin/neiler-startup && \
    echo 'echo ""' >> /usr/local/bin/neiler-startup && \
    echo 'tail -f /var/log/neiler/system.log' >> /usr/local/bin/neiler-startup && \
    chmod +x /usr/local/bin/neiler-startup

# Create neiler-help command
RUN echo '#!/bin/bash' > /usr/bin/neiler-help && \
    echo 'cat << "EOF"' >> /usr/bin/neiler-help && \
    echo 'Neiler-OS Commands:' >> /usr/bin/neiler-help && \
    echo '' >> /usr/bin/neiler-help && \
    echo '  Assembly & Emulation:' >> /usr/bin/neiler-help && \
    echo '    nasm <file>          - Assemble Neiler code' >> /usr/bin/neiler-help && \
    echo '    neiler-emu <binary>  - Run in emulator' >> /usr/bin/neiler-help && \
    echo '    ndb <binary>         - Debug program' >> /usr/bin/neiler-help && \
    echo '' >> /usr/bin/neiler-help && \
    echo '  System:' >> /usr/bin/neiler-help && \
    echo '    neiler-status        - Show system status' >> /usr/bin/neiler-help && \
    echo '    neiler-benchmark     - Run benchmarks' >> /usr/bin/neiler-help && \
    echo '    neiler-monitor       - System monitor' >> /usr/bin/neiler-help && \
    echo '' >> /usr/bin/neiler-help && \
    echo '  Development:' >> /usr/bin/neiler-help && \
    echo '    neiler-examples      - List example programs' >> /usr/bin/neiler-help && \
    echo '    neiler-docs          - Open documentation' >> /usr/bin/neiler-help && \
    echo 'EOF' >> /usr/bin/neiler-help && \
    chmod +x /usr/bin/neiler-help

# Expose ports
EXPOSE 22 8080 8081

# Set working directory
WORKDIR /home/dev

# Create default user files
RUN chown -R dev:dev /home/dev && \
    chown -R dev:dev /opt/neiler

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep sshd || exit 1

# Default command
CMD ["/usr/local/bin/neiler-startup"]
