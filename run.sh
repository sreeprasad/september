#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    # Kill all child processes in the current process group
    kill $(jobs -p) 2>/dev/null
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# Get the absolute path to the project root
PROJECT_ROOT=$(pwd)

echo "🚀 Starting Orchestrator..."

# Start Backend
echo "📦 Starting Backend Server..."
cd "$PROJECT_ROOT/backend"

# Check if venv exists
if [ -d "venv" ]; then
    source venv/bin/activate
    # Run the server in the background
    python api_server.py &
    BACKEND_PID=$!
    echo "✅ Backend started (PID: $BACKEND_PID)"
else
    echo "❌ Error: backend/venv not found. Please set up the python environment."
    exit 1
fi

# Start Frontend
echo "🎨 Starting Frontend..."
cd "$PROJECT_ROOT/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Installing dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo "--------------------------------------------------"
echo "🎉 Project is running!"
echo "📡 Backend: http://localhost:8000"
echo "💻 Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop all services."
echo "--------------------------------------------------"

# Wait for both processes to keep the script running
wait
