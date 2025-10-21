#!/bin/bash

echo "🚀 Starting Customer Support System (Fixed Version)"
echo "=================================================="

# Kill any existing processes
echo "🧹 Cleaning up..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "vite" 2>/dev/null
lsof -ti:8888 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo "✅ Cleanup complete"
echo ""

# Start backend
echo "🔧 Starting Backend (Port 8888)..."
cd backend
rm -rf __pycache__ 2>/dev/null
./venv/bin/python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 8

# Check if backend is running
if curl -s http://localhost:8888/ > /dev/null 2>&1; then
    echo "✅ Backend is running on port 8888"
else
    echo "❌ Backend failed to start"
    echo "📋 Backend logs:"
    cat ../backend.log | tail -20
    exit 1
fi

# Start frontend
echo ""
echo "🎨 Starting Frontend (Port 3000)..."
cd ../frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 5

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Application is ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8888"
echo "📚 API Docs: http://localhost:8888/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait
