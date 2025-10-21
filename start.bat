@echo off
REM Customer Support Orchestrator - Quick Start Script for Windows

echo.
echo 🚀 Starting Customer Support Orchestrator...
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo ❌ Error: backend\.env file not found!
    echo Please create backend\.env with your OpenAI API key:
    echo   OPENAI_API_KEY=your_key_here
    pause
    exit /b 1
)

REM Start backend
echo 📦 Starting Backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Start backend in new window
start "Backend Server" cmd /k "venv\Scripts\activate.bat && python main.py"
cd ..

echo ✅ Backend started
echo.

REM Wait for backend to be ready
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Start frontend
echo 🎨 Starting Frontend...
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend in new window
start "Frontend Server" cmd /k "npm run dev"
cd ..

echo ✅ Frontend started
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🎉 Application is ready!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the services
echo.
pause

