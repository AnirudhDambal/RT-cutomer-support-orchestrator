#!/bin/bash

echo "🚀 Starting Customer Support Backend on Port 8888..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Kill any process on port 8888
echo "🔍 Checking if port 8888 is in use..."
PID=$(lsof -ti:8888)
if [ ! -z "$PID" ]; then
    echo "⚠️  Killing existing process on port 8888 (PID: $PID)"
    kill -9 $PID
    sleep 1
fi
echo "✅ Port 8888 is ready"
echo ""

# Clean cache
rm -rf __pycache__

# Activate virtual environment and run
./venv/bin/python main.py

