#!/bin/bash
# Make all scripts executable

cd ~/Documents/GitHub/Study-Timer

echo "🔧 Making all shell scripts executable..."

chmod +x start.sh
chmod +x test.sh
chmod +x commit.sh
chmod +x status.sh
chmod +x make_executable.sh

echo "✅ All scripts are now executable!"
echo ""
echo "Available scripts:"
echo "  ./start.sh   - Setup and initialize"
echo "  ./test.sh    - Test components"
echo "  ./status.sh  - Check system status"
echo "  ./commit.sh  - Git commit helper"
