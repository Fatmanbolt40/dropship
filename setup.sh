#!/bin/bash

echo "🚀 Setting up DropShip AI Platform..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✏️  Please edit .env with your API keys"
fi

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Database setup (optional - requires PostgreSQL running)
echo "🗄️  Database setup..."
read -p "Do you want to run database migrations? (PostgreSQL must be running) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    alembic upgrade head
    echo "✅ Database migrations complete"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start PostgreSQL and Redis (or run: docker-compose up -d)"
echo "3. Backend: uvicorn backend.main:app --reload"
echo "4. Frontend: npm run dev"
echo ""
echo "📖 Documentation: http://localhost:8000/docs (when backend is running)"
echo "🎨 Dashboard: http://localhost:3000 (when frontend is running)"
