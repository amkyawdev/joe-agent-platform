#!/bin/bash
# Installation script for Joe-Agent-Platform

set -e

echo "Installing Joe-Agent-Platform..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps chromium

# Create storage directories
mkdir -p storage/{html,markdown,cache,outputs,vectors}

echo "Installation complete!"
echo "Run 'source venv/bin/activate' to activate the virtual environment."