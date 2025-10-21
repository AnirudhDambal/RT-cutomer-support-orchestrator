#!/bin/bash

echo "🚀 Starting Customer Support Backend on Port 8888..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Clean cache
rm -rf __pycache__

# Activate virtual environment and run
./venv/bin/python main.py

