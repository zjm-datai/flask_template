#!/bin/bash

set -e

echo "=== Step 1: Create directories and set permissions ==="
mkdir -p ./volumes/app/storage/logs
sudo chown -R 1001:1001 ./volumes/app
sudo chmod -R 755 ./volumes/app

echo "=== Step 2: Generate docker-compose.yaml ==="
python3 generate_docker_compose.py

echo "=== Step 3: Start Docker Compose ==="
docker-compose up -d

echo "=== Deployment completed! ==="