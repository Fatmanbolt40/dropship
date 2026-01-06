#!/bin/bash

# DropShip AI - 24/7 Background Service Runner
# Keeps the auto-finder running continuously in the background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"
AUTO_FINDER="$SCRIPT_DIR/auto_finder_24_7.py"
LOG_FILE="$SCRIPT_DIR/logs/auto_finder.log"
PID_FILE="$SCRIPT_DIR/auto_finder.pid"

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/campaigns"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "❌ Auto-finder is already running (PID: $PID)"
                exit 1
            fi
        fi
        
        echo "🚀 Starting 24/7 Auto Product Finder..."
        nohup "$VENV_PYTHON" "$AUTO_FINDER" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ Auto-finder started (PID: $(cat $PID_FILE))"
        echo "📋 Logs: $LOG_FILE"
        echo "💾 Campaigns: $SCRIPT_DIR/campaigns/"
        ;;
        
    stop)
        if [ ! -f "$PID_FILE" ]; then
            echo "❌ Auto-finder is not running"
            exit 1
        fi
        
        PID=$(cat "$PID_FILE")
        echo "⏸️  Stopping auto-finder (PID: $PID)..."
        kill "$PID" 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ Auto-finder stopped"
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "✅ Auto-finder is running (PID: $PID)"
                echo ""
                echo "📊 Statistics:"
                ls -1 "$SCRIPT_DIR/campaigns/" 2>/dev/null | wc -l | xargs echo "   Campaigns created:"
                echo ""
                echo "📋 Recent activity (last 10 lines):"
                tail -n 10 "$LOG_FILE" 2>/dev/null || echo "   No logs yet"
            else
                echo "❌ Auto-finder is not running (stale PID file)"
                rm -f "$PID_FILE"
            fi
        else
            echo "❌ Auto-finder is not running"
        fi
        ;;
        
    logs)
        echo "📋 Tailing logs (Ctrl+C to stop)..."
        tail -f "$LOG_FILE"
        ;;
        
    *)
        echo "DropShip AI - 24/7 Auto Product Finder & Marketer"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the auto-finder in background"
        echo "  stop    - Stop the auto-finder"
        echo "  restart - Restart the auto-finder"
        echo "  status  - Check if auto-finder is running"
        echo "  logs    - View live logs"
        exit 1
        ;;
esac
