#!/bin/bash
# CHECK STATUS OF ALL SERVICES

echo "========================================="
echo "📊 SYSTEM STATUS"
echo "========================================="
echo ""

# Check backend
if pgrep -f "python.*server.py" > /dev/null; then
    echo "✅ Backend API: RUNNING"
else
    echo "❌ Backend API: STOPPED"
fi

# Check frontend
if pgrep -f "http.server.*8080" > /dev/null; then
    echo "✅ Store Frontend: RUNNING"
else
    echo "❌ Store Frontend: STOPPED"
fi

# Check AI inventory
if pgrep -f "python.*ai_inventory" > /dev/null; then
    echo "✅ AI Inventory Manager: RUNNING"
else
    echo "❌ AI Inventory Manager: STOPPED"
fi

echo ""
echo "========================================="
echo "📦 CURRENT INVENTORY"
echo "========================================="
echo ""

PRODUCT_COUNT=$(ls -1 campaigns/*.json 2>/dev/null | wc -l)
echo "Products in store: $PRODUCT_COUNT"

if [ -d "orders" ]; then
    ORDER_COUNT=$(ls -1 orders/order_*.json 2>/dev/null | wc -l)
    echo "Total orders: $ORDER_COUNT"
fi

echo ""
echo "========================================="
echo "💰 PROFIT TRACKING"
echo "========================================="
echo ""

curl -s http://localhost:8000/api/orders/list 2>/dev/null | python3 -m json.tool 2>/dev/null | grep -E "(total_orders|total_revenue|total_profit)" || echo "No orders yet"

echo ""
echo "========================================="
