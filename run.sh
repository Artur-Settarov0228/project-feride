#!/bin/bash

# Function to handle exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    kill $BOT_PID 2>/dev/null
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

echo "🚀 Starting Feride Project..."

# Kill existing processes on ports 8000 and 3000
echo "🧹 Cleaning up ports 8000 and 3000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# 1. Start Backend and Bot
echo "📦 Starting Backend (FastAPI) on http://localhost:8000..."
source venv/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!

echo "🤖 Starting Telegram Bot..."
python3 bot.py > ../bot.log 2>&1 &
BOT_PID=$!
cd ..

# 2. Start Frontend
echo "💻 Starting Frontend (Static) on http://localhost:3000..."
cd frontend
python3 -m http.server 3000 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Detect local IP address
IP_ADDR=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
[ -z "$IP_ADDR" ] && IP_ADDR="localhost"

echo "✅ Both servers are running!"
echo "🔗 Frontend: http://$IP_ADDR:3000"
echo "🔗 Backend Docs: http://$IP_ADDR:8000/docs"
echo "🔗 Local: http://localhost:3000"
echo "📝 Logs are being written to backend.log and frontend.log"
echo "⌨️ Press Ctrl+C to stop both servers."

# Keep the script running to catch the trap
wait
