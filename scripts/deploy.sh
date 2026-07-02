#!/bin/bash
# Deployment script for Joe-Agent-Platform

set -e

echo "Deploying Joe-Agent-Platform..."

# Build Docker image
docker build -t joe-agent-platform:latest .

# Run with docker-compose
docker-compose up -d

echo "Deployment complete!"