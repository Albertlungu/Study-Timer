#!/bin/bash
# Quick start script for Study Timer

echo "🎓 Study Timer - Quick Start"
echo "=============================="
echo ""

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the Study-Timer directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
if [ ! -f "data/study_data.db" ]; then
    echo "🗄️  Initializing database..."
    python src/init_db.py
else
    echo "✅ Database already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Grant Accessibility permissions:"
echo "      System Preferences → Security & Privacy → Privacy → Accessibility"
echo "      Add Terminal or Python to the list"
echo ""
echo "   2. Start the tracker:"
echo "      python src/main.py"
echo ""
echo "   3. View your dashboard (in a new terminal):"
echo "      python src/dashboard/app.py"
echo ""
echo "Happy studying! (or procrastinating... we'll track it either way 😄)"
