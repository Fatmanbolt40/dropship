# DropShip AI - Windows PowerShell Startup Script
# Run this in PowerShell to start your dropshipping server

Write-Host "🚀 Starting DropShip AI Server..." -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "⚡ Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install/upgrade dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade fastapi uvicorn python-dotenv requests beautifulsoup4 pydantic

# Get local IP
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"}).IPAddress | Select-Object -First 1

# Start the server
Write-Host ""
Write-Host "✅ Server starting on port 8000" -ForegroundColor Green
Write-Host "📡 Local access: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🌐 Network access: http://$localIP:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python server.py
