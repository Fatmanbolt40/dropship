#!/bin/bash

echo "🚀 TRENDHUB - Professional Dropshipping Platform Setup"
echo "=================================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Installing ngrok..."
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar -xzf ngrok-v3-stable-linux-amd64.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    echo "✅ ngrok installed!"
fi

echo ""
echo "🔧 Setting up ngrok authtoken..."
echo "Go to https://dashboard.ngrok.com/get-started/your-authtoken"
echo "Copy your authtoken and run: ngrok config add-authtoken YOUR_TOKEN"
echo ""

echo "📊 Current Status:"
echo "-----------------"

# Check if backend is running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend API: Running (http://localhost:8000)"
else
    echo "❌ Backend API: Not running"
    echo "   Start with: ./venv/bin/python server.py"
fi

# Check if auto-finder is running
if pgrep -f "auto_finder_24_7" > /dev/null; then
    PID=$(pgrep -f "auto_finder_24_7")
    echo "✅ Auto-Finder: Running (PID: $PID)"
else
    echo "❌ Auto-Finder: Not running"
    echo "   Start with: bash service.sh start"
fi

# Check HTTP server for frontend
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Frontend: Running (http://localhost:8080)"
else
    echo "❌ Frontend: Not running"
    echo "   Start with: python3 -m http.server 8080"
fi

echo ""
echo "🌐 To Make Your Store PUBLIC:"
echo "-----------------------------"
echo "1. Get ngrok token: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "2. Add token: ngrok config add-authtoken YOUR_TOKEN"
echo "3. Run: ngrok http 8080"
echo "4. Share the https://xxx.ngrok.io URL - anyone can visit!"
echo ""

echo "💰 To Accept Real Payments:"
echo "---------------------------"
echo "1. Sign up: https://stripe.com"
echo "2. Get test keys: https://dashboard.stripe.com/test/apikeys"
echo "3. Add to .env: STRIPE_SECRET_KEY=sk_test_..."
echo "4. Install: ./venv/bin/pip install stripe"
echo ""

echo "📱 AI Marketing Team Status:"
echo "----------------------------"
CAMPAIGNS=$(ls marketing_campaigns/*.json 2>/dev/null | wc -l)
echo "✅ Marketing campaigns generated: $CAMPAIGNS"
echo "   Located in: ./marketing_campaigns/"
echo ""

echo "🎯 Quick Start Commands:"
echo "------------------------"
echo "Start everything:  bash service.sh start && python3 -m http.server 8080 &"
echo "Go public:         ngrok http 8080"
echo "View store:        http://localhost:8080/store_professional.html"
echo "View marketing:    ls -la marketing_campaigns/"
echo ""

echo "✨ Your Amazon Affiliate Tag: legend0ee-20"
echo "📊 Dashboard: http://localhost:8080/dashboard_pro.html"
echo "🛍️  Professional Store: http://localhost:8080/store_professional.html"
echo ""
