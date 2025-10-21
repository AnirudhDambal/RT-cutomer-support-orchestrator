#!/bin/bash
# Kill any process using port 8888

echo "🔍 Checking port 8888..."

PID=$(lsof -ti:8888)

if [ -z "$PID" ]; then
    echo "✅ Port 8888 is already free"
else
    echo "⚠️  Found process $PID using port 8888"
    kill -9 $PID
    echo "✅ Killed process $PID - Port 8888 is now free"
fi

