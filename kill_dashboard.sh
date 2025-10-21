#!/bin/bash
# Kill any processes running on port 5000

echo "🔍 Checking for processes on port 5000..."

# Find process on port 5000
PID=$(lsof -ti:5000)

if [ -z "$PID" ]; then
    echo "✅ No process running on port 5000"
else
    echo "⚠️  Found process(es): $PID"
    echo "🔪 Killing process(es)..."
    kill -9 $PID
    echo "✅ Port 5000 is now free"
fi

echo ""
echo "🚀 You can now run:"
echo "   python src/dashboard/app.py"
