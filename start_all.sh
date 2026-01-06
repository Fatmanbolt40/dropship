#!/bin/bash
# START ALL SERVICES - Make Money in Your Sleep!

cd /home/Thalegendgamer/dropship

echo "========================================="
echo "🚀 STARTING YOUR DROPSHIPPING EMPIRE"
echo "========================================="
echo ""

# Kill any existing services
pkill -f "python.*server.py" 2>/dev/null
pkill -f "python.*ai_inventory" 2>/dev/null
pkill -f "http.server.*8080" 2>/dev/null

sleep 2

# Start backend API
echo "1️⃣ Starting Backend API..."
./venv/bin/python server.py > logs/server.log 2>&1 &
SERVER_PID=$!
echo "   ✅ Backend running (PID: $SERVER_PID)"

sleep 2

# Start frontend
echo "2️⃣ Starting Store Frontend..."
python3 -m http.server 8080 > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   ✅ Store running (PID: $FRONTEND_PID)"

sleep 2

# Start AI Inventory Manager
echo "3️⃣ Starting AI Inventory Manager..."
./venv/bin/python ai_inventory_manager.py > logs/inventory.log 2>&1 &
INVENTORY_PID=$!
echo "   ✅ AI Manager running (PID: $INVENTORY_PID)"

echo ""
echo "========================================="
echo "✅ ALL SYSTEMS ONLINE!"
echo "========================================="
echo ""
echo "🛒 Your Store: http://localhost:8080/store_with_checkout.html"
echo "📊 API: http://localhost:8000"
echo "🤖 AI: Adding products every hour"
echo ""
echo "🔐 Admin Mode: Press Alt+Shift+M on store"
echo ""
echo "💰 MAKING MONEY 24/7!"
echo ""
echo "To stop: ./stop_all.sh"
echo "To check status: ./check_status.sh"
echo ""
echo "========================================="
