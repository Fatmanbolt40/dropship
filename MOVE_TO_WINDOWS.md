# Move DropShip Project to Windows

## Quick Setup (PowerShell as Admin)

### Step 1: Copy Project to Windows
```powershell
# Navigate to your user folder
cd C:\Users\$env:USERNAME

# Copy entire project from WSL to Windows
xcopy \\wsl$\kali-linux\home\Thalegendgamer\dropship dropship /E /I /H /Y

# Go to project directory
cd dropship
```

### Step 2: Allow PowerShell Scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Run the Server
```powershell
.\start_server.ps1
```

## Manual Setup (if needed)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn python-dotenv requests beautifulsoup4 pydantic stripe openai anthropic

# Start server
python server.py
```

## Firewall Configuration

The script automatically uses port 8000. If your client can't connect:

```powershell
# Add firewall rule (run as Admin)
netsh advfirewall firewall add rule name="DropShip Server" dir=in action=allow protocol=TCP localport=8000
```

## Router Port Forwarding

For clients in other states to access:
1. Login to your router (usually 192.168.1.1 or 192.168.0.1)
2. Find "Port Forwarding" or "Virtual Server"
3. Add rule:
   - External Port: 8000
   - Internal IP: Your PC's local IP
   - Internal Port: 8000
   - Protocol: TCP

## Getting Your Public IP

```powershell
(Invoke-WebRequest -Uri "http://ifconfig.me/ip").Content.Trim()
```

Share this with your client: `http://YOUR_PUBLIC_IP:8000`

## Local Testing

- Same computer: `http://localhost:8000`
- Same network: `http://YOUR_LOCAL_IP:8000`
- Internet/Other states: `http://YOUR_PUBLIC_IP:8000` (requires router forwarding)

## Troubleshooting

**Can't access from another computer?**
1. Check Windows Firewall (add rule for port 8000)
2. Check router port forwarding
3. Make sure server is running: `netstat -an | findstr :8000`

**Script won't run?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

**Missing Python?**
Download from: https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation
