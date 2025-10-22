#!/bin/bash
# Check the status of Study Timer

cd ~/Documents/GitHub/Study-Timer

echo "🔍 Study Timer Status Check"
echo "============================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Virtual environment: EXISTS"
else
    echo "❌ Virtual environment: NOT FOUND"
    echo "   Run: ./start.sh to create it"
fi

# Check if database exists
if [ -f "data/study_data.db" ]; then
    echo "Database: EXISTS"
    
    # Get database stats
    if [ -d "venv" ]; then
        source venv/bin/activate
        python -c "
import sqlite3
conn = sqlite3.connect('data/study_data.db')
cursor = conn.cursor()

# Count sessions
cursor.execute('SELECT COUNT(*) FROM sessions')
session_count = cursor.fetchone()[0]

# Count activity logs
cursor.execute('SELECT COUNT(*) FROM activity_log')
activity_count = cursor.fetchone()[0]

# Count days tracked
cursor.execute('SELECT COUNT(*) FROM daily_stats')
days_count = cursor.fetchone()[0]

print(f'   📊 Sessions logged: {session_count}')
print(f'   📝 Activity entries: {activity_count}')
print(f'   📅 Days tracked: {days_count}')

conn.close()
"
    fi
else
    echo "❌ Database: NOT FOUND"
    echo "   Run: python src/init_db.py to create it"
fi

echo ""

# Check if tracker is running
if pgrep -f "python.*src/main.py" > /dev/null; then
    echo "Tracker: RUNNING"
    PID=$(pgrep -f "python.*src/main.py")
    echo "   PID: $PID"
else
    echo "⚠️  Tracker: NOT RUNNING"
    echo "   Start with: python src/main.py"
fi

# Check if dashboard is running
if pgrep -f "python.*dashboard/app.py" > /dev/null; then
    echo "Dashboard: RUNNING"
    PID=$(pgrep -f "python.*dashboard/app.py")
    echo "   PID: $PID"
    echo "   URL: http://localhost:5000"
else
    echo "⚠️  Dashboard: NOT RUNNING"
    echo "   Start with: python src/dashboard/app.py"
fi

echo ""

# Check permissions
echo "🔐 System Permissions:"
echo "   Check manually in System Preferences:"
echo "   • Security & Privacy → Privacy → Accessibility"
echo "   • Security & Privacy → Privacy → Automation"

echo ""

# Check dependencies
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "📦 Installed Packages:"
    pip list | grep -E "Flask|pyobjc"
else
    echo "⚠️  Cannot check packages (no venv)"
fi

echo ""
echo "🎯 Quick Commands:"
echo "   Setup:     ./start.sh"
echo "   Test:      ./test.sh"
echo "   Track:     python src/main.py"
echo "   Dashboard: python src/dashboard/app.py"
echo "   Status:    ./status.sh"
echo ""
echo "📚 Documentation:"
echo "   README.md - Overview and features"
echo "   INSTALL.md - Detailed installation"
echo "   QUICKSTART.md - Quick reference"
echo "   FEATURES.md - Feature showcase"
