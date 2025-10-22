#!/bin/bash
# Study Timer Runtime Script
# Starts both the tracker and dashboard in a single command

echo "🚀 STUDYTIME RUNTIME"
echo "===================="
echo ""

# Check if we're in the right directory
if [ ! -f "src/main.py" ] || [ ! -f "src/dashboard/app.py" ]; then
    echo "Error: Please run this script from the Study-Timer root directory"
    echo "   cd /Users/albertlungu/Documents/GitHub/Study-Timer"
    exit 1
fi

echo "Checking system requirements..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if database exists, create if needed
if [ ! -d "data" ]; then
    mkdir -p data
fi

if [ ! -f "data/study_data.db" ]; then
    echo "Creating database..."
    python3 -c "
import sqlite3
conn = sqlite3.connect('data/study_data.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE sessions (id INTEGER PRIMARY KEY, app_name TEXT, window_title TEXT, file_path TEXT, website_url TEXT, start_time TEXT, end_time TEXT, duration INTEGER DEFAULT 0, is_study INTEGER DEFAULT 0, is_procrastination INTEGER DEFAULT 0)')
cursor.execute('CREATE TABLE activity_log (id INTEGER PRIMARY KEY, timestamp TEXT, app_name TEXT, window_title TEXT, file_path TEXT, website_url TEXT, is_active INTEGER DEFAULT 1)')
cursor.execute('CREATE TABLE daily_stats (date TEXT PRIMARY KEY, total_study_time INTEGER DEFAULT 0, total_procrastination_time INTEGER DEFAULT 0, total_sessions INTEGER DEFAULT 0, ib_quote TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)')
conn.commit()
conn.close()
"
    echo "Database created"
else
    echo "Database already exists"
fi

echo ""

# Kill any existing dashboard processes
echo "Killing any existing dashboard processes..."
chmod +x kill_dashboard.sh 2>/dev/null
./kill_dashboard.sh > /dev/null 2>&1

# Wait a moment for processes to die
sleep 2

echo ""
echo "Starting StudyTime components..."
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down StudyTime..."
    echo "   Press Ctrl+C again to force quit"

    # Kill any child processes
    if [ ! -z "$TRACKER_PID" ]; then
        echo "   Stopping tracker (PID: $TRACKER_PID)..."
        kill $TRACKER_PID 2>/dev/null
    fi

    if [ ! -z "$DASHBOARD_PID" ]; then
        echo "   Stopping dashboard (PID: $DASHBOARD_PID)..."
        kill $DASHBOARD_PID 2>/dev/null
    fi

    # Kill any remaining processes on port 5000
    echo "   Cleaning up port 5000..."
    ./kill_dashboard.sh > /dev/null 2>&1

    echo "StudyTime stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the tracker in background
echo "Starting tracker..."
LOG_LEVEL=DEBUG python3 src/main.py &
TRACKER_PID=$!
echo "   Tracker PID: $TRACKER_PID"

# Wait a moment for tracker to initialize
sleep 3

# Start the dashboard in background
echo "Starting dashboard..."
python3 src/dashboard/app.py &
DASHBOARD_PID=$!
echo "   Dashboard PID: $DASHBOARD_PID"

# Wait a moment for dashboard to start
sleep 2

echo ""
echo "StudyTime is now running!"
echo "==========================="
echo ""
echo "Dashboard: http://localhost:5000"
echo "Tracker logs: Check terminal output above"
echo ""
echo "Tips:"
echo "   Switch between iTerm2 and Comet to test cross-app tracking"
echo "   Sessions should continue across app switches"
echo "   Check logs for classification messages:"
echo "     [CLASSIFY] Comet is STUDY_APP"
echo "     [SESSION] Continuing session X with app switch: Comet"
echo ""
echo "To stop: Press Ctrl+C"
echo ""

# Wait for user to stop the script
wait
