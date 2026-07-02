#!/bin/bash
# Test script for Joe-Agent-Platform

set -e

source venv/bin/activate

echo "Running tests..."

pytest tests/ -v --cov=. --cov-report=html