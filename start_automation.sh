#!/bin/bash
# Quick Start - Full Automation

cd /home/Thalegendgamer/dropship

echo "════════════════════════════════════════════════════════════"
echo "  🤖 DROPSHIPPING AUTOMATION SYSTEM"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "What this does:"
echo "  ✓ Finds trending products 24/7"
echo "  ✓ Lists them on Amazon at markup"
echo "  ✓ Auto-fulfills orders when customers buy"
echo "  ✓ Makes you money in your sleep"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "⚙️  Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install rich requests beautifulsoup4 httpx python-dotenv fastapi uvicorn sqlalchemy stripe lxml --quiet
    echo "✅ Environment ready"
else
    source venv/bin/activate
fi

echo ""
echo "Starting automation services..."
echo ""

# Start backend API
echo "1️⃣  Backend API..."
python3 server.py > logs/server.log 2>&1 &
SERVER_PID=$!
echo "   ✅ Running (PID: $SERVER_PID)"
sleep 2

# Start product finder
echo "2️⃣  AI Product Finder (24/7)..."
python3 auto_finder_24_7.py > logs/finder.log 2>&1 &
FINDER_PID=$!
echo "   ✅ Running (PID: $FINDER_PID)"
sleep 1

# Start order processor
echo "3️⃣  Order Fulfillment..."
python3 order_fulfillment.py > logs/orders.log 2>&1 &
ORDERS_PID=$!
echo "   ✅ Running (PID: $ORDERS_PID)"
sleep 1

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ AUTOMATION IS NOW RUNNING 24/7!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Services Running:"
echo "   • Backend API: http://localhost:8000"
echo "   • Product Finder: Scanning suppliers every hour"
echo "   • Order Processor: Ready to fulfill orders"
echo ""
echo "💰 What's Happening:"
echo "   1. AI finds profitable products every hour"
echo "   2. Lists them on Amazon at 2-3x markup"
echo "   3. When customer buys → auto-orders from supplier"
echo "   4. Supplier ships → you keep the profit!"
echo ""
echo "📁 Check Results:"
echo "   • Found products: ls campaigns/"
echo "   • View logs: tail -f logs/*.log"
echo "   • Check status: ./check_status.sh"
echo ""
echo "🛑 To Stop: ./stop_all.sh or press Ctrl+C"
echo ""
echo "⏳ Note: Amazon Seller approval pending - products will"
echo "   list automatically once approved!"
echo ""
echo "════════════════════════════════════════════════════════════"

# Save PIDs
echo "$SERVER_PID,$FINDER_PID,$ORDERS_PID" > .automation_pids

# Keep script running
echo ""
echo "Press Ctrl+C to stop all services..."
wait
