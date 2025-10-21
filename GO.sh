#!/bin/bash
# One-command setup and run script

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         📚 STUDY TIMER - PROCRASTINATION DETECTOR 3000        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

cd ~/Documents/GitHub/Study-Timer

# Step 1: Make all scripts executable
echo "🔧 Step 1: Making scripts executable..."
chmod +x *.sh
echo "✅ Done!"
echo ""

# Step 2: Run setup
echo "🚀 Step 2: Running setup..."
./start.sh
echo ""

# Step 3: Instructions for running
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE!                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1️⃣  Grant Permissions (IMPORTANT!):"
echo "   → System Preferences → Security & Privacy → Privacy"
echo "   → Accessibility: Add Terminal and Python"
echo "   → Automation: Allow Terminal to control browsers"
echo ""
echo "2️⃣  Start the Tracker:"
echo "   Open a terminal and run:"
echo "   cd ~/Documents/GitHub/Study-Timer"
echo "   source venv/bin/activate"
echo "   python src/main.py"
echo ""
echo "3️⃣  Start the Dashboard:"
echo "   Open ANOTHER terminal and run:"
echo "   cd ~/Documents/GitHub/Study-Timer"
echo "   source venv/bin/activate"
echo "   python src/dashboard/app.py"
echo ""
echo "4️⃣  View Your Stats:"
echo "   Open your browser to: http://localhost:5000"
echo ""
echo "📚 Documentation:"
echo "   • README.md - Overview"
echo "   • QUICKSTART.md - Quick reference"
echo "   • INSTALL.md - Detailed guide"
echo ""
echo "🎓 Happy studying! (or procrastinating... we'll track it either way 😄)"
echo ""
