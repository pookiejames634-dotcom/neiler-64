#!/bin/bash
#
# Neiler-OS Server Startup Script
# Builds and launches the Neiler-64 development server
#

set -e

echo "================================================"
echo "   Neiler-OS Server - Startup Script"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed"
    echo "Please install docker-compose"
    exit 1
fi

# Navigate to server directory
cd "$(dirname "$0")"

echo "[1/4] Building Neiler-OS Docker image..."
docker-compose build

echo ""
echo "[2/4] Creating necessary directories..."
mkdir -p neiler-os/workload-sim
mkdir -p neiler-os/monitor
mkdir -p services
mkdir -p config

# Create placeholder files if they don't exist
touch neiler-os/workload-sim/.keep
touch neiler-os/monitor/.keep
touch services/.keep
touch config/.keep

echo ""
echo "[3/4] Starting Neiler-OS server..."
docker-compose up -d

echo ""
echo "[4/4] Waiting for services to start..."
sleep 5

echo ""
echo "================================================"
echo "   Neiler-OS Server is RUNNING!"
echo "================================================"
echo ""
echo "Access Information:"
echo "  SSH:            ssh dev@localhost -p 2222"
echo "  Password:       neiler64"
echo "  Web Dashboard:  http://localhost:8080"
echo "  Monitor:        http://localhost:8081"
echo ""
echo "Useful Commands:"
echo "  View logs:      docker-compose logs -f"
echo "  Stop server:    docker-compose down"
echo "  Restart:        docker-compose restart"
echo "  Shell access:   docker exec -it neiler-os-server /usr/bin/nsh"
echo ""
echo "Quick Test:"
echo "  ssh dev@localhost -p 2222"
echo "  (then run: neiler-help)"
echo ""
echo "================================================"
