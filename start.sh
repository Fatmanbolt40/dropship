#!/bin/bash

# Quick Start Script for DropShip AI

echo "🚀 Starting DropShip AI Platform..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "⚙️  Please configure .env file with your API keys"
    echo "   Press Enter to continue with defaults..."
    read
fi

# Option to use Docker or local
echo "Choose startup method:"
echo "1) Docker (Recommended - includes PostgreSQL & Redis)"
echo "2) Local (Requires PostgreSQL & Redis running separately)"
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo "🐳 Starting with Docker..."
        docker-compose up -d
        echo ""
        echo "✅ Services started!"
        echo "📖 API Docs: http://localhost:8000/docs"
        echo "🎨 Dashboard: http://localhost:3000"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
        ;;
    2)
        echo "🔧 Starting locally..."
        
        # Start backend
        echo "Starting backend API..."
        source venv/bin/activate
        uvicorn backend.main:app --reload &
        BACKEND_PID=$!
        
        # Wait a bit for backend to start
        sleep 3
        
        # Start frontend
        echo "Starting frontend dashboard..."
        npm run dev &
        FRONTEND_PID=$!
        
        echo ""
        echo "✅ Services started!"
        echo "📖 API Docs: http://localhost:8000/docs"
        echo "🎨 Dashboard: http://localhost:3000"
        echo ""
        echo "Backend PID: $BACKEND_PID"
        echo "Frontend PID: $FRONTEND_PID"
        echo ""
        echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
        
        # Wait for user interrupt
        wait
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
