#!/bin/bash

echo "Starting LeadSquatch Pro..."
echo ""

echo "Step 1: Installing Backend Dependencies..."
cd backend
pip install -r requirements.txt

echo ""
echo "Step 2: Starting Backend Server (Flask)..."
python app.py &
BACKEND_PID=$!

cd ..

echo ""
echo "Step 3: Starting Frontend Development Server (Vite)..."
echo ""
echo "=================================="
echo "LeadSquatch Pro is running!"
echo "=================================="
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

npm run dev

kill $BACKEND_PID
