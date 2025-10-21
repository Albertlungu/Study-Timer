#!/bin/bash
# Test the Study Timer components

cd ~/Documents/GitHub/Study-Timer

echo "🧪 Testing Study Timer Components"
echo "=================================="
echo ""

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  No virtual environment found. Run ./start.sh first!"
    exit 1
fi

echo ""
echo "1️⃣ Testing App Tracker..."
python src/trackers/app_tracker.py
echo ""

echo "2️⃣ Testing Browser Tracker..."
echo "   (Make sure Chrome or Safari is open!)"
python src/trackers/browser_tracker.py
echo ""

echo "3️⃣ Testing File Tracker..."
python src/trackers/file_tracker.py
echo ""

echo "✅ All component tests complete!"
echo ""
echo "📝 To test the full system:"
echo "   Terminal 1: python src/main.py"
echo "   Terminal 2: python src/dashboard/app.py"
