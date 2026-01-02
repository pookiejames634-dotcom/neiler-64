#!/bin/bash

echo "========================================="
echo "  Starting Neiler-64 Server"
echo "========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "[ERROR] Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

# Build and start containers
echo "[*] Building Neiler-64 server image..."
docker-compose -f docker-compose.yml build

echo ""
echo "[*] Starting Neiler-64 server..."
docker-compose -f docker-compose.yml up -d

echo ""
echo "========================================="
echo "  Neiler-64 Server Started!"
echo "========================================="
echo ""
echo "Server Information:"
echo "  • Container: neiler-64"
echo "  • SSH Port: 2222"
echo "  • Web Port: 8080"
echo ""
echo "Connect via SSH:"
echo "  ssh neiler@localhost -p 2222"
echo "  Password: neiler123"
echo ""
echo "Or from another machine:"
echo "  ssh neiler@$(hostname -I | awk '{print $1}') -p 2222"
echo ""
echo "Other Services:"
echo "  • Monitoring: http://localhost:3001"
echo "  • Metrics: http://localhost:9090"
echo ""
echo "Useful Commands:"
echo "  • View logs:     docker-compose logs -f neiler-64-server"
echo "  • Stop server:   docker-compose down"
echo "  • Restart:       docker-compose restart"
echo "  • Shell access:  docker exec -it neiler-64 bash"
echo ""
echo "========================================="
