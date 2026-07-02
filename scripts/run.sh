#!/bin/bash
# Run script for Joe-Agent-Platform

set -e

source venv/bin/activate

# Run API server
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload