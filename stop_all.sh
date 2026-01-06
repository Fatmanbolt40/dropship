#!/bin/bash
# STOP ALL SERVICES

cd /home/Thalegendgamer/dropship

echo "⛔ Stopping all services..."

pkill -f "python.*server.py"
pkill -f "python.*ai_inventory"
pkill -f "http.server.*8080"

sleep 2

echo "✅ All services stopped"
